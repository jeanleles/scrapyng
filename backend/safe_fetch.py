import http.client
import ipaddress
import math
import os
import socket
import ssl
from email.message import Message
from urllib.parse import urljoin, urlsplit


MAX_URL_BYTES = 2 * 1024
MAX_RESPONSE_BYTES = 3 * 1024 * 1024
MAX_REDIRECTS = 3


def _timeout_from_env(name, default, maximum):
    try:
        timeout = float(os.getenv(name, str(default)))
    except ValueError:
        return default
    if not math.isfinite(timeout):
        return default
    return min(max(timeout, 0.1), maximum)


CONNECT_TIMEOUT = _timeout_from_env("SCRAPE_CONNECT_TIMEOUT", 5, 10)
READ_TIMEOUT = _timeout_from_env("SCRAPE_READ_TIMEOUT", 15, 30)
HTML_CONTENT_TYPES = {"text/html", "application/xhtml+xml"}
REDIRECT_STATUSES = {301, 302, 303, 307, 308}


class SafeFetchError(Exception):
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.status_code = status_code


def _validate_and_resolve(url):
    if not isinstance(url, str) or not url:
        raise SafeFetchError("URL inválida ou maior que 2 KB.", 400)
    try:
        url_length = len(url.encode("utf-8"))
    except UnicodeEncodeError as error:
        raise SafeFetchError("URL inválida.", 400) from error
    if url_length > MAX_URL_BYTES:
        raise SafeFetchError("URL inválida ou maior que 2 KB.", 400)
    if any(character.isspace() or ord(character) < 32 for character in url):
        raise SafeFetchError("URL inválida.", 400)

    try:
        parts = urlsplit(url)
        scheme = parts.scheme.lower()
        hostname = parts.hostname
        port = parts.port
    except ValueError as error:
        raise SafeFetchError("URL inválida.", 400) from error

    if scheme not in {"http", "https"} or not hostname or parts.username or parts.password:
        raise SafeFetchError("A URL deve usar HTTP ou HTTPS e não pode conter credenciais.", 400)
    port = port if port is not None else (443 if scheme == "https" else 80)
    if port == 0:
        raise SafeFetchError("A porta informada não é válida.", 400)

    normalized_hostname = hostname.rstrip(".").lower()
    if normalized_hostname == "localhost" or normalized_hostname.endswith(
        (".localhost", ".local", ".internal", ".home.arpa")
    ):
        raise SafeFetchError("Destinos locais não são permitidos.", 400)

    try:
        literal_ip = ipaddress.ip_address(normalized_hostname)
    except ValueError:
        literal_ip = None

    if literal_ip is not None:
        addresses = [str(literal_ip)]
    else:
        try:
            addresses = list(
                dict.fromkeys(
                    result[4][0].split("%")[0]
                    for result in socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
                )
            )
        except (OSError, UnicodeError) as error:
            raise SafeFetchError("Não foi possível resolver o host informado.") from error

    if not addresses:
        raise SafeFetchError("O host informado não possui endereços válidos.")

    try:
        if any(not ipaddress.ip_address(address).is_global for address in addresses):
            raise SafeFetchError("Destinos privados ou reservados não são permitidos.", 400)
    except ValueError as error:
        raise SafeFetchError("O host informou um endereço IP inválido.", 400) from error

    return parts, addresses


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host, port, address):
        super().__init__(host, port, timeout=CONNECT_TIMEOUT)
        self._pinned_address = address

    def connect(self):
        self.sock = socket.create_connection(
            (self._pinned_address, self.port), self.timeout, self.source_address
        )


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, port, address):
        super().__init__(host, port, timeout=CONNECT_TIMEOUT, context=ssl.create_default_context())
        self._pinned_address = address

    def connect(self):
        raw_socket = socket.create_connection(
            (self._pinned_address, self.port), self.timeout, self.source_address
        )
        try:
            self.sock = self._context.wrap_socket(raw_socket, server_hostname=self.host)
        except Exception:
            raw_socket.close()
            raise


def fetch_html(url):
    current_url = url

    for redirect_count in range(MAX_REDIRECTS + 1):
        parts, addresses = _validate_and_resolve(current_url)
        hostname = parts.hostname
        port = parts.port if parts.port is not None else (443 if parts.scheme.lower() == "https" else 80)
        connection_type = _PinnedHTTPSConnection if parts.scheme.lower() == "https" else _PinnedHTTPConnection
        connection = connection_type(hostname, port, addresses[0])
        path = parts.path or "/"
        if parts.query:
            path = f"{path}?{parts.query}"

        try:
            connection.connect()
            connection.sock.settimeout(READ_TIMEOUT)
            connection.request(
                "GET",
                path,
                headers={
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Encoding": "identity",
                    "User-Agent": "Scrapyng/1.0",
                    "Connection": "close",
                },
            )
            response = connection.getresponse()

            if response.status in REDIRECT_STATUSES:
                location = response.getheader("Location")
                if not location or redirect_count == MAX_REDIRECTS:
                    raise SafeFetchError("Redirecionamento ausente ou limite de redirects excedido.")
                current_url = urljoin(current_url, location)
                continue

            if response.status < 200 or response.status >= 300:
                raise SafeFetchError(f"O servidor remoto respondeu com HTTP {response.status}.")

            content_encoding = response.getheader("Content-Encoding", "identity").lower()
            if content_encoding not in {"", "identity"}:
                raise SafeFetchError("Respostas comprimidas não são permitidas.")

            content_type = Message()
            content_type["content-type"] = response.getheader("Content-Type", "")
            if content_type.get_content_type().lower() not in HTML_CONTENT_TYPES:
                raise SafeFetchError("O endereço não retornou conteúdo HTML.")

            content_length = response.getheader("Content-Length")
            if content_length:
                try:
                    if int(content_length) > MAX_RESPONSE_BYTES:
                        raise SafeFetchError("A resposta da página excede o limite permitido.", 413)
                except ValueError as error:
                    raise SafeFetchError("O servidor remoto retornou um tamanho inválido.") from error

            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise SafeFetchError("A resposta da página excede o limite permitido.", 413)

            charset = content_type.get_content_charset() or "utf-8"
            try:
                return body.decode(charset, errors="replace")
            except LookupError:
                return body.decode("utf-8", errors="replace")
        except SafeFetchError:
            raise
        except (OSError, http.client.HTTPException, ssl.SSLError) as error:
            raise SafeFetchError("Falha ao acessar a página remota.") from error
        finally:
            connection.close()

    raise SafeFetchError("Limite de redirects excedido.")