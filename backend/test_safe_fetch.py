import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlsplit

import safe_fetch
from safe_fetch import SafeFetchError


def dns_result(address):
    return (2, 1, 6, "", (address, 80))


class FakeResponse:
    def __init__(self, status=200, headers=None, body=b"<html></html>"):
        self.status = status
        self.headers = headers or {"Content-Type": "text/html; charset=utf-8"}
        self.body = body

    def getheader(self, name, default=None):
        return self.headers.get(name, default)

    def read(self, limit):
        return self.body[:limit]


class SafeFetchTests(unittest.TestCase):
    def test_rejects_unsupported_schemes_and_local_destinations(self):
        for url in (
            "file:///etc/passwd",
            "ftp://example.com/page",
            "http://localhost/",
            "http://127.0.0.1/",
            "http://169.254.169.254/latest/meta-data/",
            "http://example.com:0/",
            "http://example.com/a b",
        ):
            with self.subTest(url=url), self.assertRaises(SafeFetchError) as error:
                safe_fetch._validate_and_resolve(url)
            self.assertEqual(error.exception.status_code, 400)

    @patch("safe_fetch.socket.getaddrinfo")
    def test_rejects_dns_answers_containing_private_addresses(self, getaddrinfo):
        getaddrinfo.return_value = [dns_result("93.184.216.34"), dns_result("10.0.0.4")]

        with self.assertRaises(SafeFetchError) as error:
            safe_fetch._validate_and_resolve("https://example.com/")

        self.assertEqual(error.exception.status_code, 400)

    @patch("safe_fetch.socket.create_connection")
    def test_socket_connects_to_the_validated_ip_not_the_hostname(self, create_connection):
        connection = safe_fetch._PinnedHTTPConnection("example.com", 80, "93.184.216.34")

        connection.connect()

        self.assertEqual(create_connection.call_args.args[0], ("93.184.216.34", 80))
        self.assertIs(connection.sock, create_connection.return_value)

    @patch("safe_fetch._PinnedHTTPConnection")
    @patch("safe_fetch.socket.getaddrinfo")
    def test_revalidates_redirect_before_connecting(self, getaddrinfo, connection_class):
        getaddrinfo.return_value = [dns_result("93.184.216.34")]
        connection = connection_class.return_value
        connection.sock = Mock()
        connection.getresponse.return_value = FakeResponse(
            status=302, headers={"Location": "http://127.0.0.1:5555/"}
        )

        with self.assertRaises(SafeFetchError) as error:
            safe_fetch.fetch_html("http://example.com/")

        self.assertEqual(error.exception.status_code, 400)
        connection_class.assert_called_once()
        getaddrinfo.assert_called_once()
        connection.close.assert_called_once()

    @patch("safe_fetch._PinnedHTTPConnection")
    @patch("safe_fetch._validate_and_resolve")
    def test_rejects_oversized_response_before_reading_body(self, validate, connection_class):
        validate.return_value = (urlsplit("http://example.com/"), ["93.184.216.34"])
        connection = connection_class.return_value
        connection.sock = Mock()
        response = Mock()
        response.status = 200
        response.getheader.side_effect = lambda name, default=None: {
            "Content-Type": "text/html",
            "Content-Length": str(safe_fetch.MAX_RESPONSE_BYTES + 1),
        }.get(name, default)
        connection.getresponse.return_value = response

        with self.assertRaises(SafeFetchError) as error:
            safe_fetch.fetch_html("http://example.com/")

        self.assertEqual(error.exception.status_code, 413)
        response.read.assert_not_called()

    @patch("safe_fetch._PinnedHTTPConnection")
    @patch("safe_fetch._validate_and_resolve")
    def test_rejects_non_html_content_type(self, validate, connection_class):
        validate.return_value = (urlsplit("http://example.com/"), ["93.184.216.34"])
        connection = connection_class.return_value
        connection.sock = Mock()
        connection.getresponse.return_value = FakeResponse(
            headers={"Content-Type": "application/json"}
        )

        with self.assertRaises(SafeFetchError):
            safe_fetch.fetch_html("http://example.com/")

    def test_rejects_url_larger_than_two_kibibytes(self):
        with self.assertRaises(SafeFetchError) as error:
            safe_fetch._validate_and_resolve("https://example.com/" + "a" * 2048)

        self.assertEqual(error.exception.status_code, 400)

    def test_rejects_url_with_invalid_unicode(self):
        with self.assertRaises(SafeFetchError) as error:
            safe_fetch._validate_and_resolve("https://example.com/\ud800")

        self.assertEqual(error.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()