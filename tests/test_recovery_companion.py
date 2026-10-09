"""Regression tests for Recovery Companion.

Run from the repository root:
    python -m unittest discover -s tests -v

These tests mock Gemini/Telegram network calls; they do not need API keys.
"""
import asyncio
import json
import os
import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app import main
from app.gemini_client import clean_and_parse_json, is_demo_mode, extract_recovery_plan


class JsonParsingTests(unittest.TestCase):
    def test_parses_plain_json_object(self):
        self.assertEqual(clean_and_parse_json('{"summary_plain":"OK"}'), {"summary_plain": "OK"})

    def test_parses_json_inside_markdown_fence(self):
        raw = '```json\n{"summary_plain":"OK"}\n```'
        self.assertEqual(clean_and_parse_json(raw), {"summary_plain": "OK"})

    def test_parses_json_surrounded_by_commentary(self):
        raw = 'Here is the result:\n{"summary_plain":"OK"}\nDone.'
        self.assertEqual(clean_and_parse_json(raw), {"summary_plain": "OK"})

    def test_rejects_invalid_json(self):
        with self.assertRaises(ValueError):
            clean_and_parse_json("not json at all")

    def test_rejects_json_array_not_object(self):
        with self.assertRaises(ValueError):
            clean_and_parse_json('[{"summary_plain":"OK"}]')


class DemoModeTests(unittest.TestCase):
    def test_demo_mode_when_env_enabled(self):
        with patch.dict(os.environ, {"DEMO_MODE": "true", "GEMINI_API_KEY": "fake-key"}):
            self.assertTrue(is_demo_mode())

    def test_live_mode_when_key_exists_and_demo_disabled(self):
        with patch.dict(os.environ, {"DEMO_MODE": "false", "GEMINI_API_KEY": "fake-key"}):
            self.assertFalse(is_demo_mode())

    def test_demo_mode_when_api_key_missing(self):
        with patch.dict(os.environ, {"DEMO_MODE": "false"}, clear=True):
            self.assertTrue(is_demo_mode())

    def test_explicit_true_override_enables_demo(self):
        with patch.dict(os.environ, {"DEMO_MODE": "false", "GEMINI_API_KEY": "fake-key"}):
            self.assertTrue(is_demo_mode(True))

    def test_explicit_false_override_does_not_override_env_demo_flag(self):
        with patch.dict(os.environ, {"DEMO_MODE": "true", "GEMINI_API_KEY": "fake-key"}):
            self.assertTrue(is_demo_mode(False))


class ApiEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_config_reports_languages(self):
        response = self.client.get("/api/config")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["supported_languages"], ["English", "Hindi", "Kannada"])
        self.assertIn("demo_mode", body)
        self.assertIn("has_api_key", body)

    def test_sample_rejects_unsupported_language(self):
        response = self.client.get("/api/sample/french")
        self.assertEqual(response.status_code, 400)

    def test_sample_returns_demo_plan_for_supported_language(self):
        response = self.client.get("/api/sample/English")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "success")
        self.assertTrue(body["demo_mode"])
        self.assertIn("summary_plain", body["data"])

    def test_extract_rejects_missing_file_in_live_mode(self):
        with patch.object(main, "is_demo_mode", return_value=False):
            response = self.client.post("/api/extract", data={"language": "English"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("select a photo", response.json()["detail"].lower())

    def test_extract_rejects_empty_upload(self):
        with patch.object(main, "is_demo_mode", return_value=False):
            response = self.client.post(
                "/api/extract",
                data={"language": "English"},
                files={"file": ("empty.jpg", b"", "image/jpeg")},
            )
        self.assertEqual(response.status_code, 400)
        self.assertIn("empty", response.json()["detail"].lower())

    def test_extract_calls_pipeline_and_returns_live_result(self):
        plan = {"summary_plain": "Test plan", "medicines": []}
        async def fake_extract(**kwargs):
            return plan, False

        with patch.object(main, "is_demo_mode", return_value=False), \
             patch.object(main, "_cache_path") as cache_path, \
             patch.object(main, "extract_recovery_plan", side_effect=fake_extract):
            cache_path.return_value.exists.return_value = False
            response = self.client.post(
                "/api/extract",
                data={"language": "English", "demo_mode": "false"},
                files={"file": ("discharge.jpg", b"fake-image-bytes", "image/jpeg")},
            )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "success")
        self.assertFalse(body["demo_mode"])
        self.assertEqual(body["data"], plan)

    def test_extract_maps_gemini_runtime_error_to_503(self):
        async def fail_extract(**kwargs):
            raise RuntimeError("Daily AI limit reached. Please try again later or switch on Demo Mode.")

        with patch.object(main, "is_demo_mode", return_value=False), \
             patch.object(main, "_cache_path") as cache_path, \
             patch.object(main, "extract_recovery_plan", side_effect=fail_extract):
            cache_path.return_value.exists.return_value = False
            response = self.client.post(
                "/api/extract",
                data={"language": "English", "demo_mode": "false"},
                files={"file": ("discharge.jpg", b"fake-image-bytes", "image/jpeg")},
            )
        self.assertEqual(response.status_code, 503)
        self.assertIn("Daily AI limit", response.json()["message"])

    def test_extract_maps_invalid_model_output_to_422(self):
        async def fail_extract(**kwargs):
            raise ValueError("Please retake the photo")

        with patch.object(main, "is_demo_mode", return_value=False), \
             patch.object(main, "_cache_path") as cache_path, \
             patch.object(main, "extract_recovery_plan", side_effect=fail_extract):
            cache_path.return_value.exists.return_value = False
            response = self.client.post(
                "/api/extract",
                data={"language": "English", "demo_mode": "false"},
                files={"file": ("discharge.jpg", b"fake-image-bytes", "image/jpeg")},
            )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["message"], "Please retake the photo")


class ExtractionPipelineTests(unittest.TestCase):
    def test_demo_pipeline_returns_sample_without_calling_gemini(self):
        with patch("app.gemini_client.is_demo_mode", return_value=True), \
             patch("app.gemini_client.call_gemini_api", new_callable=AsyncMock) as gemini:
            result, used_demo = asyncio.run(
                extract_recovery_plan(b"image", "image/jpeg", "English", demo_mode_override=True)
            )
        self.assertTrue(used_demo)
        self.assertIn("summary_plain", result)
        gemini.assert_not_awaited()

    def test_live_pipeline_parses_gemini_json(self):
        with patch("app.gemini_client.is_demo_mode", return_value=False), \
             patch("app.gemini_client.load_system_prompt", return_value="Prompt"), \
             patch("app.gemini_client.call_gemini_api", new_callable=AsyncMock,
                   return_value='{"summary_plain":"Live result"}') as gemini:
            result, used_demo = asyncio.run(
                extract_recovery_plan(b"image", "image/jpeg", "English", demo_mode_override=False)
            )
        self.assertFalse(used_demo)
        self.assertEqual(result["summary_plain"], "Live result")
        gemini.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
