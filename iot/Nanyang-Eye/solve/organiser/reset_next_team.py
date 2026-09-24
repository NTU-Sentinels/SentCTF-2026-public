#!/usr/bin/env python3
"""Return NANYANG-EYE-03 home and restore a clean player workspace.

Run this only from the organiser-controlled Camera Bay workstation.  It is not
a player file and must never be copied into dist/.
"""
from __future__ import annotations

import argparse
import base64
import os
import shutil
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


def post_home(gateway_url: str, username: str, password: str) -> str:
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    request = urllib.request.Request(
        gateway_url.rstrip("/") + "/home",
        data=b"",
        headers={"Authorization": "Basic " + token, "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.read().decode(errors="replace").strip() or f"HTTP {response.status}"


def restore_workspace(template: Path, workspace: Path) -> None:
    if not template.is_file():
        raise FileNotFoundError(f"clean template is missing: {template}")
    workspace.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=workspace.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        shutil.copy2(template, temporary_path)
        temporary_path.replace(workspace)
    finally:
        temporary_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gateway-url", default=os.environ.get("ORION_GATEWAY_URL", "http://gateway"))
    parser.add_argument("--username", default=os.environ.get("ORION_GATEWAY_USER"))
    parser.add_argument("--password", default=os.environ.get("ORION_GATEWAY_PASS"))
    parser.add_argument("--template", type=Path, default=Path("/opt/orion-console/templates/camera_control.py"))
    parser.add_argument("--workspace", type=Path, default=Path("/workspace/camera_control.py"))
    arguments = parser.parse_args()
    if not arguments.username or not arguments.password:
        parser.error("set ORION_GATEWAY_USER and ORION_GATEWAY_PASS in the organiser service environment")
    try:
        result = post_home(arguments.gateway_url, arguments.username, arguments.password)
    except urllib.error.URLError as error:
        raise SystemExit(f"camera reset failed; workspace was not changed: {error}") from error
    restore_workspace(arguments.template, arguments.workspace)
    print(f"camera returned home ({result}); clean player workspace restored")


if __name__ == "__main__":
    main()
