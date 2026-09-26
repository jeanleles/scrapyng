import unittest
from unittest.mock import patch

import app as backend_app
from bs4 import BeautifulSoup
from safe_fetch import SafeFetchError


class ApiSecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = backend_app.app.test_client()

    def test_api_does_not_enable_cross_origin_access(self):
        response = self.client.get("/health")

        self.assertNotIn("Access-Control-Allow-Origin", response.headers)

    def test_rejects_request_bodies_over_the_configured_limit(self):
        response = self.client.post(
            "/scrape",
            data=b"{" + b" " * (16 * 1024),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.json["error"], "O corpo da requisição excede o limite permitido.")

    def test_summary_extraction_stops_at_the_gemini_character_limit(self):
        body = BeautifulSoup(
            f"<body><p>{'a' * (backend_app.MAX_GEMINI_CHARS + 100)}</p></body>",
            "html.parser",
        ).body

        text = backend_app.extract_summary_text(body)

        self.assertEqual(len(text), backend_app.MAX_GEMINI_CHARS)

    @patch.object(backend_app, "fetch_html", side_effect=SafeFetchError("blocked", 400))
    def test_scrape_limit_is_ten_requests_per_client_per_minute(self, _fetch_html):
        client_ip = "198.51.100.20"
        responses = [
            self.client.post(
                "/scrape",
                json={"url": "https://example.com/"},
                environ_overrides={"REMOTE_ADDR": client_ip},
            )
            for _ in range(11)
        ]

        self.assertEqual([response.status_code for response in responses[:10]], [400] * 10)
        self.assertEqual(responses[10].status_code, 429)

    @patch.object(backend_app, "fetch_html", side_effect=SafeFetchError("blocked", 400))
    def test_summarize_limit_is_three_requests_per_client_per_minute(self, _fetch_html):
        client_ip = "198.51.100.21"
        responses = [
            self.client.post(
                "/summarize",
                json={"url": "https://example.com/"},
                environ_overrides={"REMOTE_ADDR": client_ip},
            )
            for _ in range(4)
        ]

        self.assertEqual([response.status_code for response in responses[:3]], [400] * 3)
        self.assertEqual(responses[3].status_code, 429)


if __name__ == "__main__":
    unittest.main()