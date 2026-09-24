from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import secrets
from http import HTTPStatus
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs


CHALLENGE_TITLE = "Hidden in Plain Sight"
LOGIN_EMAIL = os.environ.get("SENTCTF_WEB_EMAIL", "legacy.admin@ntu.edu.sg")
LOGIN_PASSWORD = os.environ.get("SENTCTF_WEB_PASSWORD", "nanyang0017")
PASSWORD_HASH = hashlib.md5(LOGIN_PASSWORD.encode("utf-8")).hexdigest()
FLAG = "sentctf{source_before_force}"
SESSION_COOKIE_NAME = "hips_session"
SESSION_TOKEN = secrets.token_urlsafe(32)


def check_credentials(email: str, password: str) -> bool:
    """Return True only for the configured challenge credentials."""
    return hmac.compare_digest(email, LOGIN_EMAIL) and hmac.compare_digest(
        password, LOGIN_PASSWORD
    )


def render_homepage() -> str:
    hidden_email = json.dumps(LOGIN_EMAIL)
    password_hash = json.dumps(PASSWORD_HASH)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{CHALLENGE_TITLE} | NTU Legacy Staff Portal</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      background: #eef2f7;
      color: #182230;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      min-height: 100vh;
      margin: 0;
      display: grid;
      place-items: center;
      padding: 24px;
      background:
        radial-gradient(circle at top right, #d9e7ff 0, transparent 32rem),
        #eef2f7;
    }}
    main {{
      width: min(100%, 430px);
      padding: 34px;
      border: 1px solid #d7dee8;
      border-radius: 18px;
      background: #fff;
      box-shadow: 0 24px 70px rgba(37, 55, 80, .14);
    }}
    .eyebrow {{
      margin: 0 0 8px;
      color: #315fbb;
      font-size: .78rem;
      font-weight: 800;
      letter-spacing: .12em;
      text-transform: uppercase;
    }}
    h1 {{ margin: 0 0 8px; font-size: 1.65rem; }}
    .notice {{ margin: 0 0 26px; color: #617086; line-height: 1.55; }}
    label {{ display: block; margin: 15px 0 7px; font-weight: 700; }}
    input {{
      width: 100%;
      padding: 12px 13px;
      border: 1px solid #b8c2d0;
      border-radius: 8px;
      font: inherit;
    }}
    input:focus {{
      outline: 3px solid rgba(49, 95, 187, .18);
      border-color: #315fbb;
    }}
    button {{
      width: 100%;
      margin-top: 22px;
      padding: 12px;
      border: 0;
      border-radius: 8px;
      background: #244f9e;
      color: #fff;
      font: inherit;
      font-weight: 800;
      cursor: pointer;
    }}
    button:hover {{ background: #183d80; }}
    #result {{
      min-height: 1.5rem;
      margin: 18px 0 0;
      padding: 0;
      color: #a12626;
      line-height: 1.45;
      overflow-wrap: anywhere;
    }}
    #result.success {{ color: #137042; font-weight: 800; }}
    footer {{
      margin-top: 24px;
      border-top: 1px solid #e5e9ef;
      padding-top: 18px;
      color: #7b8798;
      font-size: .82rem;
    }}
  </style>
</head>
<body>
  <main>
    <p class="eyebrow">Archived system</p>
    <h1>NTU Legacy Staff Portal</h1>
    <p class="notice">
      This service is no longer maintained. Authorised staff may still sign in
      to retrieve archived migration records.
    </p>

    <form id="login-form">
      <label for="email">Staff email</label>
      <input id="email" name="email" type="email" autocomplete="username"
             placeholder="name@ntu.edu.sg" required>

      <label for="password">Password</label>
      <input id="password" name="password" type="password"
             autocomplete="current-password" required>

      <button type="submit">Open archive</button>
    </form>
    <p id="result" role="status" aria-live="polite"></p>
    <footer>Legacy Portal build 1.4.2 · Internal use only</footer>
  </main>

  <script>
    // TODO before retirement: remove the recovery record from this old build.
    const legacyRecoveryContact = {hidden_email};
    const legacyCredentialDigest = {{
      algorithm: "MD5",
      digest: {password_hash}
    }};

    const form = document.querySelector("#login-form");
    const result = document.querySelector("#result");

    form.addEventListener("submit", async (event) => {{
      event.preventDefault();
      result.className = "";
      result.textContent = "Checking credentials…";

      try {{
        const response = await fetch("/api/login", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            email: form.email.value,
            password: form.password.value
          }})
        }});
        const data = await response.json();
        if (response.ok && data.redirect) {{
          window.location.assign(data.redirect);
          return;
        }}
        result.textContent = data.message;
      }} catch (_) {{
        result.textContent = "The legacy service did not respond.";
      }}
    }});
  </script>
</body>
</html>
"""


def render_flag_page() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Archive</title>
</head>
<body>
  <p>{FLAG}</p>
</body>
</html>
"""


class ChallengeHandler(BaseHTTPRequestHandler):
    """HTTP routes for the challenge."""

    server_version = "SentCTFLegacyPortal/1.0"

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path in {"/", "/index.html"}:
            self._send_html(render_homepage())
            return
        if self.path == "/flag":
            if self._has_valid_session():
                self._send_html(render_flag_page())
            else:
                self._send_json(
                    HTTPStatus.FORBIDDEN,
                    {"message": "Sign in before opening the archive."},
                )
            return
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"message": "Not found."})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path != "/api/login":
            self._send_json(HTTPStatus.NOT_FOUND, {"message": "Not found."})
            return

        try:
            email, password = self._read_credentials()
        except (ValueError, json.JSONDecodeError):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"message": "Send an email and password."},
            )
            return

        if check_credentials(email, password):
            self._send_json(
                HTTPStatus.OK,
                {
                    "message": "Archive unlocked.",
                    "redirect": "/flag",
                },
                headers={
                    "Set-Cookie": (
                        f"{SESSION_COOKIE_NAME}={SESSION_TOKEN}; "
                        "HttpOnly; SameSite=Strict; Path=/"
                    )
                },
            )
            return

        self._send_json(
            HTTPStatus.UNAUTHORIZED,
            {"message": "Invalid staff email or password."},
        )

    def _read_credentials(self) -> tuple[str, str]:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > 16_384:
            raise ValueError("Invalid request size")

        raw_body = self.rfile.read(content_length).decode("utf-8")
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0]

        if content_type == "application/json":
            data = json.loads(raw_body)
            if not isinstance(data, dict):
                raise ValueError("Expected an object")
            email = data.get("email", "")
            password = data.get("password", "")
        else:
            data = parse_qs(raw_body, keep_blank_values=True)
            email = data.get("email", [""])[0]
            password = data.get("password", [""])[0]

        if not isinstance(email, str) or not isinstance(password, str):
            raise ValueError("Credentials must be text")
        return email.strip(), password

    def _has_valid_session(self) -> bool:
        raw_cookie = self.headers.get("Cookie", "")
        cookie = SimpleCookie()
        try:
            cookie.load(raw_cookie)
        except CookieError:
            return False
        session = cookie.get(SESSION_COOKIE_NAME)
        return session is not None and hmac.compare_digest(
            session.value,
            SESSION_TOKEN,
        )

    def _send_html(self, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(
        self,
        status: HTTPStatus,
        payload: dict[str, str],
        headers: dict[str, str] | None = None,
    ) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format_string: str, *args: object) -> None:
        # Retain useful request logs without ever printing request bodies/passwords.
        print(f"[web-easy] {self.address_string()} - {format_string % args}")


def self_test() -> None:
    """Run fast checks without starting a listener."""
    page = render_homepage()
    assert LOGIN_EMAIL in page, "The intended email clue is missing from source"
    assert PASSWORD_HASH in page, "The intended password digest is missing"
    assert LOGIN_PASSWORD not in page, "Password leaked into the client"
    assert FLAG not in page, "Flag leaked into the client"
    assert FLAG in render_flag_page(), "Flag page does not contain the flag"
    assert check_credentials(LOGIN_EMAIL, LOGIN_PASSWORD)
    assert not check_credentials(LOGIN_EMAIL, "definitely-wrong")
    print("Web challenge self-test passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="check the challenge logic without starting the server",
    )
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    host = os.environ.get("SENTCTF_HOST", "0.0.0.0")
    port = int(os.environ.get("SENTCTF_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), ChallengeHandler)
    print(f"{CHALLENGE_TITLE} is running at http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping challenge.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
