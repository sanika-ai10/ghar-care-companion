# Recovery Companion

An AI recovery companion that helps patients understand their hospital discharge papers in their own language, and keeps their family informed when a dose is taken or missed.

Built for PromptWars x Error Zero (Theme: AI for Healthcare Accessibility).

## The problem

Patients leave hospital with a dense, jargon-filled discharge summary and a few minutes of verbal instructions. Many, especially elderly patients and people who do not read English comfortably, misunderstand their medicines, miss warning signs, or forget follow-ups. This is a common cause of avoidable readmissions.

## What it does

1. **Understand:** upload a photo of a discharge summary or prescription. Gemini turns it into a simple plan in English, Hindi or Kannada: summary, medicine schedule with clock times, follow-ups, warning signs, diet and activity, and hospital contacts.
2. **Read aloud:** the plan can be spoken using the browser's speech synthesis.
3. **Be honest about uncertainty:** unclear lines and missing information (for example no follow-up date) go into a "Things we're not sure about" card instead of being guessed.
4. **Track doses:** each scheduled dose has a "Taken" button.
5. **Keep family informed (with consent):** when the patient ticks "Tell my family", taking a dose sends a message to a family member's Telegram. A demo button simulates a missed-dose alert.

## Safety and privacy by design

- The extraction prompt (`prompts/01_extraction_prompt.md`) tells the model to use only what is in the document, never to diagnose, never to invent doses or dates, and to flag anything unclear.
- Missed-dose messages tell the family to call the patient and ask the doctor or pharmacist. They never suggest taking extra doses.
- Family alerts are opt-in through a checkbox the patient controls.
- API keys and the Telegram token live only on the server in `.env`. They are never sent to the browser or committed.
- The app does not store uploaded documents. The image is sent to the Gemini API for analysis only. Dose taps are stored in the user's own browser.
- This is an informational tool, not medical advice.

## What works today, and what does not

Working:
- Photo to plan with Gemini, in three languages, with read-aloud
- Model fallback when a Gemini model is busy
- "Taken" buttons and Telegram family alerts
- Demo mode with a saved sample plan, so the app runs without any API key

Demo or not built yet:
- The missed-dose alert is triggered by a demo button, not an automatic timer
- Phone push reminders, a blood-pressure log, grounded Q&A chat and a weekly doctor summary are planned, not built
- Doses are saved per browser, not in an account

## Tech

Python FastAPI backend, plain HTML/CSS/JavaScript frontend, Google Gemini API, Telegram Bot API.

## Run it

```
pip install -r requirements.txt
cp .env.example .env
python3 -m uvicorn app.main:app --reload --port 8000
```

Open http://127.0.0.1:8000

- With `DEMO_MODE=true` (the default in `.env.example`) the app shows a saved sample plan and needs no keys.
- For real analysis, set `GEMINI_API_KEY` and `DEMO_MODE=false` in `.env`.
- For family alerts, create a bot with @BotFather, put its token in `TELEGRAM_BOT_TOKEN`, press Start on the bot from the family member's phone, and set `TELEGRAM_CHAT_ID` to that chat's ID.

Sample test documents (fake data) are in `sample_docs/`.

## How it was built

Built with AI-assisted prompting. The extraction prompt is in `prompts/`.

All patient names, documents and numbers in this repository are fictional.
