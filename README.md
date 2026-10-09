# Recovery Companion 🩺

A mobile-friendly healthcare web app that converts hospital discharge summaries and prescriptions into a simple, patient-friendly home recovery plan in **English**, **Hindi (हिन्दी)**, and **Kannada (ಕನ್ನಡ)**.

Built with a **Python FastAPI** backend and a lightweight **HTML/CSS/JS** frontend.

---

## ✨ Features (Step 1)

1. **Document Upload & Mobile Camera Capture**:
   - Take a photo directly on mobile or upload prescription / discharge summary images (`JPEG`, `PNG`, `WEBP`).
   - Drag-and-drop support and instant image preview.
   - Quick one-tap **"Try with Sample Discharge Summary"** button for instant testing.

2. **Multilingual Patient Language Support**:
   - Select between **English**, **हिन्दी (Hindi)**, or **ಕನ್ನಡ (Kannada)**.
   - Automatically injects the selected language into `prompts/01_extraction_prompt.md`.

3. **Gemini Vision API Extraction & Robust Retries**:
   - Sends document images with the specialized medical extraction prompt.
   - Requests structured JSON output.
   - **Automatic Retry**: If the model output is malformed or invalid JSON, it retries once. If it still fails, it displays: *"Please retake the photo"* alongside practical photo-taking tips.

4. **Structured Patient Recovery Plan**:
   - 📋 **Summary**: Diagnosis, procedure, patient details, and simple 3-sentence summary with doctor disclaimer.
   - 💊 **Medicine Schedule**: Visual schedule with dosages, clock times (08:00, 20:00), food instructions (before/after meals), purpose in plain language, critical medicine warnings, and time-of-day filters (Morning, Afternoon, Night, As Needed).
   - 🗓️ **Follow-ups & Next Steps**: Upcoming appointments, clinic locations, and what to bring.
   - 🚨 **Warning Signs (Red Flags)**: Urgency indicators (Emergency vs. Call Doctor), symptoms to watch for, and exact actions to take.
   - 🔍 **"Things We're Not Sure About" Card**: Highlights unclear handwriting, faint notes, and missing information with advice to confirm with doctor/pharmacist.
   - 🩺 **Home Monitoring & Emergency Contacts**: Temperature, blood pressure, wound checks, and clickable hospital phone numbers.

5. **Audio "Read Aloud" Button**:
   - Uses the browser's built-in **Web Speech API** (`window.speechSynthesis`).
   - Automatically adapts voice and speech accents to the selected language (`en-IN`, `hi-IN`, `kn-IN`).
   - Interactive Play / Stop controls with animated audio waveform status.

6. **Zero-API-Key DEMO_MODE**:
   - Reads the Gemini API key securely from `.env` (never hardcoded).
   - Automatically switches to `DEMO_MODE` if no API key is provided, or if `DEMO_MODE=true` is set.
   - Toggle switch in header allows users to switch to Demo Mode anytime.
   - Complete realistic sample recovery plans provided in English, Hindi, and Kannada.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Modern web browser (Chrome, Safari, Edge, Firefox)

### 2. Installation

Clone or open the repository:
```bash
cd ghar-care-companion
```

Install the minimal dependencies:
```bash
pip install -r requirements.txt
```

*(Dependencies: `fastapi`, `uvicorn`, `python-multipart`, `python-dotenv`, `httpx`)*

---

### 3. Environment Configuration (`.env`)

Create or edit the `.env` file in the project root:

```env
# Gemini API Key (get one from Google AI Studio: https://aistudio.google.com/)
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Optional: set to true to force demo mode without calling Gemini API
DEMO_MODE=false

# Optional: customize model (default: gemini-2.5-flash with fallback to gemini-1.5-flash)
GEMINI_MODEL=gemini-2.5-flash
```

> **Note:** If `GEMINI_API_KEY` is not set or left empty, the application will automatically run in **DEMO_MODE**, returning rich sample data in your chosen language!

---

### 4. Running the Application

Start the FastAPI backend with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser at:
```
http://localhost:8000
```
*(On mobile devices connected to the same Wi-Fi, open `http://<your-computer-ip>:8000`)*

---

## 📂 Project Structure

```
ghar-care-companion/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI server, endpoints, and static file routing
│   ├── gemini_client.py     # Gemini Vision API integration, prompt formatting & retry logic
│   └── sample_data.py       # Realistic sample plans in English, Hindi, and Kannada
├── prompts/
│   └── 01_extraction_prompt.md  # Core extraction prompt with {LANGUAGE} parameter
├── static/
│   ├── css/
│   │   └── style.css        # Mobile-friendly, accessible CSS design
│   ├── js/
│   │   └── app.js           # Client UI interactions, API requests, Speech Synthesis
│   └── index.html           # Main Single Page Application interface
├── .env                     # Local environment variables
├── .gitignore
├── requirements.txt         # Minimal dependency list
└── README.md                # Documentation and run instructions
```

---

## 📡 API Endpoints

- `GET /` — Serves the mobile-friendly web app.
- `GET /api/config` — Checks if API key is configured and returns demo mode status.
- `GET /api/sample/{language}` — Fetches pre-computed sample recovery plan (`English`, `Hindi`, `Kannada`).
- `POST /api/extract` — Accepts `file` (photo) and `language`. Processes through Gemini or Demo Mode. Returns structured recovery JSON.
  - Returns `422 Unprocessable Entity` with `"Please retake the photo"` if image text cannot be parsed into valid JSON after retry.
