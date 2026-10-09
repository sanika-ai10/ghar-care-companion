import base64
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import httpx
from dotenv import load_dotenv

from app.sample_data import get_sample_response

# Load environment variables from .env
load_dotenv(override=True)

logger = logging.getLogger("recovery_companion")
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "01_extraction_prompt.md"

CANDIDATE_MODELS = [
    os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
]


def is_demo_mode(override: Optional[bool] = None) -> bool:
    """
    Check if demo mode is enabled.
    Returns True if override is True, or DEMO_MODE env is true,
    or if GEMINI_API_KEY is not configured or empty.
    """
    if override is True:
        return True
    env_demo = os.getenv("DEMO_MODE", "").strip().lower() in ("true", "1", "yes")
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    return env_demo or not api_key


def load_system_prompt(language: str = "English") -> str:
    """
    Load system prompt from prompts/01_extraction_prompt.md and replace {LANGUAGE}
    with the user's selected language.
    """
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"Extraction prompt file not found at {PROMPT_FILE}")

    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")
    return prompt_text.replace("{LANGUAGE}", language)



def clean_and_parse_json(raw_text: str) -> Dict[str, Any]:
    """
    Parse a JSON object from the model response.
    Supports Markdown fences and commentary around an object.
    Rejects valid JSON arrays and other non-object JSON values.
    """
    cleaned = raw_text.strip()

    # Strip Markdown code fences if present.
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) > 2 and lines[-1].strip().startswith("```"):
            cleaned = "\n".join(lines[1:-1]).strip()
        else:
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)

    # If the entire response is valid JSON, it must be an object.
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        data = None
    else:
        if isinstance(data, dict):
            return data
        raise ValueError("Model response must be a JSON object")

    # Otherwise, look for an object surrounded by commentary.
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")

    if first_brace != -1 and last_brace > first_brace:
        candidate = cleaned[first_brace:last_brace + 1]
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON output received from model") from exc

        if isinstance(data, dict):
            return data

    raise ValueError("Invalid JSON output received from model")

async def call_gemini_api(
    image_bytes: bytes,
    mime_type: str,
    system_prompt: str,
    language: str,
    is_retry: bool = False,
) -> str:
    """
    Call Gemini generateContent endpoint with the document image and prompt.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment or .env file.")

    base64_data = base64.b64encode(image_bytes).decode("utf-8")

    user_text = (
        f"Extract all medical recovery details from this medical document according to the system instructions. "
        f"Write all patient-facing fields in {language}. Return strictly valid JSON conforming to the schema."
    )
    if is_retry:
        user_text += " IMPORTANT: Ensure your entire response is strictly valid JSON without any truncation or formatting syntax errors."

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": base64_data,
                        }
                    },
                    {"text": user_text},
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1,
        },
    }

    last_error: Optional[Exception] = None

    # Try preferred model and fallbacks if needed
    for model_name in CANDIDATE_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        logger.info(f"Calling Gemini API with model: {model_name} (retry={is_retry})")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)

            if response.status_code == 200:
                result = response.json()
                candidates = result.get("candidates", [])
                if not candidates:
                    raise ValueError("No generation candidate returned by Gemini API")
                parts = candidates[0].get("content", {}).get("parts", [])
                if not parts:
                    raise ValueError("Empty candidate content received from Gemini API")
                return parts[0].get("text", "")
            elif response.status_code == 404:
                logger.warning(f"Model {model_name} returned 404, attempting fallback model.")
                last_error = ValueError(f"Model {model_name} not found: {response.text}")
                continue
            elif response.status_code in (429, 503):
                logger.warning(f"Model {model_name} returned {response.status_code}, attempting fallback model.")
                last_error = RuntimeError(f"Gemini API error ({response.status_code}): {response.text}")
                continue
            else:
                logger.error(f"Gemini API returned HTTP {response.status_code}: {response.text}")
                raise RuntimeError(f"Gemini API error ({response.status_code}): {response.text}")

        except httpx.RequestError as exc:
            logger.error(f"Network error calling Gemini API: {exc}")
            last_error = exc
            break

    if last_error:
        raise last_error
    raise RuntimeError("Failed to obtain response from Gemini API")


async def extract_recovery_plan(
    image_bytes: bytes,
    mime_type: str,
    language: str = "English",
    demo_mode_override: Optional[bool] = None,
) -> Tuple[Dict[str, Any], bool]:
    """
    Main extraction pipeline:
    1. If in demo mode, returns pre-computed realistic plan.
    2. Formats system prompt with chosen language.
    3. Calls Gemini API.
    4. If JSON is invalid, retries once.
    5. If still invalid after retry, raises ValueError("Please retake the photo").
    Returns (result_dict, is_demo).
    """
    # Normalize language string
    valid_languages = {"english": "English", "hindi": "Hindi", "kannada": "Kannada"}
    lang_normalized = valid_languages.get(language.strip().lower(), "English")

    if is_demo_mode(demo_mode_override):
        logger.info(f"Running in DEMO_MODE for language: {lang_normalized}")
        return get_sample_response(lang_normalized), True

    system_prompt = load_system_prompt(lang_normalized)

    # Attempt 1
    raw_response = ""
    try:
        logger.info(f"Attempt 1: Calling Gemini API for language '{lang_normalized}'")
        raw_response = await call_gemini_api(
            image_bytes=image_bytes,
            mime_type=mime_type,
            system_prompt=system_prompt,
            language=lang_normalized,
            is_retry=False,
        )
        data = clean_and_parse_json(raw_response)
        return data, False
    except Exception as err:
        logger.warning(f"Attempt 1 JSON parsing/calling failed: {err}. Retrying once...")
        if "429" in str(err) or "RESOURCE_EXHAUSTED" in str(err):
            raise RuntimeError("Daily AI limit reached. Please try again later or switch on Demo Mode.")

    # Attempt 2 (Retry once as per requirement 6)
    try:
        logger.info(f"Attempt 2: Retrying Gemini API call for language '{lang_normalized}'")
        raw_response = await call_gemini_api(
            image_bytes=image_bytes,
            mime_type=mime_type,
            system_prompt=system_prompt,
            language=lang_normalized,
            is_retry=True,
        )
        data = clean_and_parse_json(raw_response)
        return data, False
    except Exception as retry_err:
        logger.error(f"Attempt 2 failed: {retry_err}")
        err_msg = str(retry_err)
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            raise RuntimeError("Daily AI limit reached. Please try again later or switch on Demo Mode.")
        if "503" in err_msg or "UNAVAILABLE" in err_msg or "temporarily unavailable" in err_msg.lower():
            raise RuntimeError("Gemini service is temporarily unavailable. Please try again later.")
        # As per requirement 6: "If the JSON is invalid, retry once, then show 'Please retake the photo'."
        raise ValueError("Please retake the photo")
