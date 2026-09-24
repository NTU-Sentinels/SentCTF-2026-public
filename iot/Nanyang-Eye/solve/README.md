# Solution: Nanyang Eye

## Challenge Details

- **Category:** IoT
- **Author:** Mujabeast
- **Difficulty:** 2/5
- **Format:** Offline packet analysis followed by a controlled physical-camera action

## Key Concepts

- Separating camera control traffic from video traffic in a PCAP
- Wireshark display filters and following an HTTP stream
- HTTP Basic authentication and Base64 decoding
- D-Link-style relative pan/tilt CGI form fields
- Reconstructing a small Python HTTP client from captured protocol evidence

## Intended Solve Path

```text
project_orion.zip
  -> separate the busy HTTP control traffic from RTSP/RTP video traffic
  -> filter the HTTP POST requests and find /setControlPanTilt
  -> decode the HTTP Basic value
  -> infer the missing right-direction code and form body
  -> complete camera_control.py locally
  -> confirm with --dry-run
  -> reproduce the completed TODO block at Camera Bay
  -> start the CCTV session and pan right to the sign
  -> submit the physical flag
```

## Player Files

`project_orion.zip` contains only:

- `incident_report.txt`
- `nanyang_eye_capture.pcapng`
- `camera_control.py`

The archive intentionally does not contain the flag, real camera address, real
camera administrator account, or organiser-side gateway configuration.

## Step 1: Find The Control Request

Open `nanyang_eye_capture.pcapng` in Wireshark. The capture deliberately
contains routine ARP, DNS, NTP, HTTP, RTSP and RTP traffic. Do not scan it by
eye. A sensible starting filter is:

```text
http
```

The capture contains a POST to:

```text
/setControlPanTilt
```

Players should then narrow this to:

```text
http.request.method == "POST"
```

This returns five POST requests. Inspect the request URI and follow the stream
for the one directed to `/setControlPanTilt`. It reveals a D-Link-style
relative PTZ request:

```text
POST /setControlPanTilt HTTP/1.1
Authorization: Basic b3BzLXN2Yzp0dW5lX3RoZV9sZW5z
Content-Type: application/x-www-form-urlencoded

PanSingleMoveDegree=10&TiltSingleMoveDegree=0&PanTiltSingleMove=5
```

The RTSP traffic is evidence of the separate video-streaming function. It is
not the control interface players need to reproduce.

## Step 2: Recover The Challenge Account

Decode the HTTP Basic blob:

```bash
printf 'b3BzLXN2Yzp0dW5lX3RoZV9sZW5z' | base64 -d
```

It yields:

```text
ops-svc:tune_the_lens
```

This is an intentionally public challenge account accepted only by the isolated
gateway. It is not the real D-Link administrator account.

## Step 3: Complete The Local Client

In `camera_control.py`, complete the three TODOs:

```python
GATEWAY_USER = "ops-svc"
GATEWAY_PASS = "tune_the_lens"

DIRECTION_CODES["right"] = 5

def build_move(direction, degrees):
    return {
        "PanSingleMoveDegree": degrees if direction in HORIZONTAL else 0,
        "TiltSingleMoveDegree": degrees if direction in VERTICAL else 0,
        "PanTiltSingleMove": DIRECTION_CODES[direction],
    }
```

Verify the request without contacting any device:

```bash
python3 camera_control.py --dry-run right 10
```

The printed form body must match the captured field layout and right-direction
code. The team cannot reach the real camera from its own laptop.

## Step 4: Execute At Camera Bay

The facilitator opens the CCTV Operations Console only when the team reaches
the physical station. Teams must complete `camera_control.py` on their own
laptop before reaching the station. The console starts at a normal Linux shell
prompt in `/workspace`, where a fresh incomplete `camera_control.py` is
available. It does not open an editor automatically. Teams may use `nano` or
another normal terminal editor themselves if they need to reproduce their
completed local work.

1. If needed, open the supplied file manually and reproduce the completed
   TODOs from the team's local work:

   ```bash
   cd /workspace
   nano camera_control.py
   ```

   Save with `Ctrl+O`, press `Enter`, then exit with `Ctrl+X`.

2. Start the controlled CCTV session:

   ```bash
   python3 camera_control.py start
   ```

3. The preview changes from `NO RECORDING` to the live feed. The camera starts
   at its straight-ahead home view; the sign is approximately 170 degrees to
   the right.
4. Pan right in bounded relative moves while watching the live preview. A fast
   first pass is:

   ```bash
   python3 camera_control.py right 20
   ```

   Run that eight times, then use `right 10` and `right 5` for final alignment.

5. Read the flag from the physical sign and submit it.

## Hints And Release Timing

1. **Immediately / free:** The PCAP has video and maintenance traffic. Ask
   players to compare protocols, not to guess a filter.
2. **After basic PCAP exploration:** Direct players toward the HTTP POST and
   explain that HTTP Basic is Base64-encoded, not encrypted.
3. **At the physical-station queue:** Remind players that the form is a
   relative D-Link PTZ command; they should finish their client before using
   Camera Bay time.

## Reviewer And Testing Notes

- Confirm `dist/project_orion.zip` extracts to exactly the three intended
  player files.
- Confirm the PCAP has substantial non-control traffic, exactly five HTTP POST
  requests, and exactly one request to `/setControlPanTilt`. Its body must
  contain the three documented fields and `PanTiltSingleMove=5`.
- Run the incomplete client first: it must refuse to operate until the account
  TODOs are completed.
- Apply the intended TODO block and run:

  ```bash
  python3 camera_control.py --dry-run right 10
  ```

  It must print the expected Basic header and form body without network access.

- At Camera Bay, verify the terminal opens at an ordinary `/workspace` prompt
  with a fresh incomplete client but no automatic editor, `start` enables the
  preview, valid movement commands move the camera, and invalid credentials
  are rejected.
- After each team, run `solve/organiser/reset_next_team.py` from the protected
  organiser path. It sends `/home` independently of the team file and restores
  the clean, incomplete workspace template. Do not use a browser reload as a
  reset.
- Keep the real camera IP address, administrator credentials, Docker settings,
  and organiser gateway outside this challenge repository.

## Final Flag

```text
sentctf{0r10n_4l1gn3d}
```
