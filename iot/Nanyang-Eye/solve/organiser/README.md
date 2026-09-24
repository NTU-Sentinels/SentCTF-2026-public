# Camera Bay organiser reset

This directory is organiser-only. Never place it in `dist/` or make it
available on the player workstation.

Install `reset_next_team.py` on the organiser-controlled host and keep one
clean, incomplete `camera_control.py` at:

```text
/opt/orion-console/templates/camera_control.py
```

Set `ORION_GATEWAY_URL`, `ORION_GATEWAY_USER`, and `ORION_GATEWAY_PASS` in the
organiser console service environment. Do not store the values in this
repository.

After every team, run:

```bash
python3 /opt/orion-console/organiser/reset_next_team.py
```

The script authenticates to the isolated gateway, sends its ordinary `POST
/home` request, and atomically replaces `/workspace/camera_control.py` with
the clean template. It does not depend on, open, or repair the team's edited
file.

Only hand the next team the workstation after the script reports success.
