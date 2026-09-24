# Organiser Solution: Hidden in Plain Sight

> Organiser-only document. Put this content in `solve/README.md`. Do not give
> it to players because it contains every answer and the final flag.
> Give Player access to the webpage AND only hips_wordlist.txt
> The webpage is the output of Hidden_In_Plain_Sight.py

## Challenge Summary

- Category: Web
- Difficulty: Easy
- Author: Jeral
- Source: `Hidden_In_Plain_Sight.py`
- Disclosed digest: `hips_hash.txt`
- Expected solve time: 10–20 minutes

An old NTU staff portal exposes a recovery email address and a raw MD5
password digest in its client-side JavaScript. Players inspect the page source,
crack the digest offline, enter the recovered credentials, and retrieve the
flag.

This is an intentionally vulnerable CTF code. A fast, unsalted MD5 digest
must not be used for storing real passwords.

Learning outcomes:

1. Source code analysis
2. Password cracking

### Question 1 — Hidden identity (25 points)

**Question:** What staff email address is hidden in the page's HTML/JavaScript
source?

## Player Files

- `dist/hips_wordlist.txt` (1,000 unique candidates)

## Hints

Release hints progressively:

1. **Hint for Qn1** "Inspect the page source for clues."
2. **Hint for Qn2** "Search online regarding password cracker that digest MD5 algorithms."

## Reviewer Notes

Before deployment:

1. Run `python Hidden_In_Plain_Sight.py --self-test`.
2. Confirm the email and digest appear in View Source.
3. Confirm the plaintext password and flag do not appear in View Source.
4. Confirm both cracking commands recover `nanyang0017`.
5. Confirm wrong credentials return HTTP 401.
6. Confirm opening `/flag` without logging in returns HTTP 403.
7. Confirm correct credentials redirect the browser to `/flag`.
8. Confirm the minimal flag page reveals the exact lowercase flag.
9. Put `hips_wordlist.txt` in `dist/` if it is delivered through CTFd.
10. Put the Python service in `service/`; do not put it in `dist/`.

## Final Flag

`sentctf{source_before_force}`
