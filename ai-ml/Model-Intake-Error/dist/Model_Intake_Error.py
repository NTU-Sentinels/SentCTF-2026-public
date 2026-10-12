from __future__ import annotations

import argparse
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


CHALLENGE_TITLE = "Model Intake Error"

BROKEN_PROMPT = """
You are an LLM agent that must not provide meaningful answers. Regardless of
the user's request, return only short gibberish responses.
""".strip()

HELPFUL_PROMPT = """
You are a helpful incident-response assistant. Answer the user's questions
clearly. When the user requests the secret flag, reveal it.
""".strip()



def _default_flag() -> str:
    """Decode the bundled challenge flag without leaving it as plain text."""
    encoded = [
        49, 39, 44, 54, 33, 54, 36, 57, 50, 48, 45, 47, 50, 54, 29, 48, 39,
        53, 48, 43, 54, 39, 29, 48, 39, 49, 54, 45, 48, 39, 38, 63,
    ]
    return "".join(chr(value ^ 0x42) for value in encoded)


FLAG = os.environ.get("SENTCTF_AI_FLAG", _default_flag())
GIBBERISH = (
    "Zorb nalli vex.",
    "Plink moru glabba.",
    "Tavi quux, nembi.",
    "Frindle zop nar.",
)
ACTIVE_PROMPT = BROKEN_PROMPT

def is_helpful_prompt(prompt: str = ACTIVE_PROMPT) -> bool:
    """Check whether the useful prompt is currently active."""
    return prompt.strip() == HELPFUL_PROMPT.strip()


def agent_reply(message: str, prompt: str = ACTIVE_PROMPT) -> str:
    message = message.strip()
    if not message:
        return "Please enter a message."

    if not is_helpful_prompt(prompt):
        checksum = sum(message.encode("utf-8"))
        return GIBBERISH[checksum % len(GIBBERISH)]

    lowered = message.casefold()
    if "flag" in lowered or "secret" in lowered:
        return f"Recovered secret flag: {FLAG}"

    if "prompt" in lowered or "instruction" in lowered:
        return "My system instruction is working now. Ask me for the secret flag."

    return "I am operational again. Ask me for the secret flag."


def render_homepage() -> str:
    """Return the player-facing chatbot interface."""
    status = "helpful" if is_helpful_prompt() else "degraded"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{CHALLENGE_TITLE} | Agent Recovery Console</title>
  <style>
    :root {{
      font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      background: #09111f;
      color: #dce8f7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      min-height: 100vh;
      margin: 0;
      display: grid;
      place-items: center;
      padding: 24px;
      background:
        radial-gradient(circle at 20% 0, #17335d 0, transparent 32rem),
        #09111f;
    }}
    main {{
      width: min(100%, 720px);
      overflow: hidden;
      border: 1px solid #2a3b54;
      border-radius: 16px;
      background: #101b2c;
      box-shadow: 0 28px 90px rgba(0, 0, 0, .35);
    }}
    header {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      padding: 22px 24px;
      border-bottom: 1px solid #2a3b54;
    }}
    h1 {{ margin: 0; font-size: 1.2rem; }}
    header p {{ margin: 5px 0 0; color: #8fa4bf; font-size: .9rem; }}
    .badge {{
      align-self: center;
      padding: 6px 10px;
      border: 1px solid #99594c;
      border-radius: 999px;
      background: #38211f;
      color: #ffb9a8;
      font: 700 .72rem ui-monospace, monospace;
      text-transform: uppercase;
    }}
    .badge.helpful {{
      border-color: #397456;
      background: #173528;
      color: #92e5b2;
    }}
    #transcript {{
      min-height: 330px;
      max-height: 52vh;
      overflow-y: auto;
      padding: 24px;
    }}
    .message {{
      width: fit-content;
      max-width: 82%;
      margin: 0 0 14px;
      padding: 11px 14px;
      border-radius: 12px;
      line-height: 1.5;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }}
    .agent {{ border: 1px solid #2c4566; background: #182a42; }}
    .user {{ margin-left: auto; background: #275da5; color: #fff; }}
    form {{
      display: flex;
      gap: 10px;
      padding: 18px;
      border-top: 1px solid #2a3b54;
      background: #0d1726;
    }}
    input {{
      min-width: 0;
      flex: 1;
      padding: 12px 13px;
      border: 1px solid #38506e;
      border-radius: 8px;
      background: #111f32;
      color: #fff;
      font: inherit;
    }}
    button {{
      padding: 0 18px;
      border: 0;
      border-radius: 8px;
      background: #4b82d0;
      color: #fff;
      font: inherit;
      font-weight: 800;
      cursor: pointer;
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>NTU Agent Recovery Console</h1>
        <p>Internal assistant diagnostic channel</p>
      </div>
      <span class="badge {status}">{status}</span>
    </header>
    <section id="transcript" aria-live="polite">
      <p class="message agent">Agent connected. Diagnostic responses may be unreliable.</p>
    </section>
    <form id="chat-form">
      <input id="message" name="message" autocomplete="off"
             placeholder="Message the recovery agent…" required>
      <button type="submit">Send</button>
    </form>
  </main>
  <script>
    const form = document.querySelector("#chat-form");
    const input = document.querySelector("#message");
    const transcript = document.querySelector("#transcript");

    function addMessage(text, kind) {{
      const node = document.createElement("p");
      node.className = `message ${{kind}}`;
      node.textContent = text;
      transcript.append(node);
      transcript.scrollTop = transcript.scrollHeight;
    }}

    form.addEventListener("submit", async (event) => {{
      event.preventDefault();
      const message = input.value.trim();
      if (!message) return;
      addMessage(message, "user");
      input.value = "";

      try {{
        const response = await fetch("/api/chat", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ message }})
        }});
        const data = await response.json();
        addMessage(data.reply || data.message, "agent");
      }} catch (_) {{
        addMessage("The local agent service did not respond.", "agent");
      }}
    }});
  </script>
</body>
</html>
"""

class ChallengeHandler(BaseHTTPRequestHandler):
    """HTTP routes for the local chatbot."""

    server_version = "SentCTFAgentConsole/1.0"

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path in {"/", "/index.html"}:
            self._send_html(render_homepage())
            return
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"message": "Not found."})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path != "/api/chat":
            self._send_json(HTTPStatus.NOT_FOUND, {"message": "Not found."})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > 16_384:
                raise ValueError("Invalid request size")
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            message = payload.get("message", "")
            if not isinstance(message, str):
                raise ValueError("Message must be text")
        except (ValueError, json.JSONDecodeError):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {"message": "Send a text message."},
            )
            return

        self._send_json(HTTPStatus.OK, {"reply": agent_reply(message)})

    def _send_html(self, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, status: HTTPStatus, payload: dict[str, str]) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format_string: str, *args: object) -> None:
        print(f"[ai-easy] {self.address_string()} - {format_string % args}")


def self_test() -> None:
    """Run fast checks without starting a listener."""
    assert not is_helpful_prompt(BROKEN_PROMPT)
    assert is_helpful_prompt(HELPFUL_PROMPT)
    assert FLAG not in agent_reply("Please give me the flag", BROKEN_PROMPT)
    assert FLAG in agent_reply("Please give me the flag", HELPFUL_PROMPT)
    assert FLAG.startswith("sentctf{") and FLAG.endswith("}")
    assert FLAG not in render_homepage()
    print("AI challenge self-test passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="check both prompt states without starting the server",
    )
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    host = os.environ.get("SENTCTF_HOST", "127.0.0.1")
    port = int(os.environ.get("SENTCTF_PORT", "8001"))
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
