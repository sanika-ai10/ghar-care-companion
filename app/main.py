import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.gemini_client import extract_recovery_plan, is_demo_mode
from app.sample_data import get_sample_response

app = FastAPI(
    title="Recovery Companion",
    description="Mobile-friendly medical document reader and recovery plan companion",
    version="1.0.0",
)

# Enable CORS for local development flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


@app.get("/api/config")
async def get_config():
    """Returns app configuration status (e.g. whether demo mode is default)."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    return {
        "demo_mode": is_demo_mode(),
        "has_api_key": bool(api_key),
        "supported_languages": ["English", "Hindi", "Kannada"],
        "default_language": "English",
    }


@app.get("/api/sample/{language}")
async def get_sample(language: str):
    """Returns sample recovery plan for given language."""
    valid = {"english", "hindi", "kannada"}
    if language.lower() not in valid:
        raise HTTPException(
            status_code=400,
            detail="Language must be English, Hindi, or Kannada",
        )
    return {
        "status": "success",
        "demo_mode": True,
        "language": language.capitalize(),
        "data": get_sample_response(language),
    }


@app.post("/api/extract")
async def extract_document(
    file: Optional[UploadFile] = File(None),
    language: str = Form("English"),
    demo_mode: Optional[bool] = Form(None),
):
    """
    Endpoint that receives an uploaded medical document photo, sends it to Gemini API
    with the extraction system prompt formatted for the chosen language, and returns JSON.
    If the model output is invalid JSON, retries once; if still invalid, returns
    'Please retake the photo'.
    """
    # Validate language
    lang_normalized = language.strip().capitalize()
    if lang_normalized not in ["English", "Hindi", "Kannada"]:
        lang_normalized = "English"

    # If demo mode is active or requested, or no file provided
    demo_active = is_demo_mode(demo_mode)

    if demo_active and (file is None or file.filename == ""):
        sample_plan = get_sample_response(lang_normalized)
        return {
            "status": "success",
            "demo_mode": True,
            "language": lang_normalized,
            "data": sample_plan,
        }

    if not file or not file.filename:
        # If not demo mode and no file
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select a photo of your medical document.",
        )

    # Read image contents
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    mime_type = file.content_type or "image/jpeg"
    if not mime_type.startswith("image/"):
        mime_type = "image/jpeg"

    try:
        plan, used_demo = await extract_recovery_plan(
            image_bytes=image_bytes,
            mime_type=mime_type,
            language=lang_normalized,
            demo_mode_override=demo_mode,
        )

        return {
            "status": "success",
            "demo_mode": used_demo,
            "language": lang_normalized,
            "data": plan,
        }

    except ValueError as val_err:
        # Handles requirement 6: "Please retake the photo"
        error_msg = str(val_err)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": error_msg,
                "detail": error_msg,
            },
        )
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": str(exc),
                "detail": "Failed to process document. Please try again.",
            },
        )


# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def serve_index():
    """Serves the main single-page web app."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Recovery Companion API is running. static/index.html not found."}
