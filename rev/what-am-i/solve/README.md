# Solution: What Am I?

## Challenge Summary

`what_am_i` is a stripped 64-bit Linux ELF executable. It prints a decoy message, but the flag remains as a readable string inside the binary.

## Learning Objective

Introduce basic binary triage: identify a file with `file`, then inspect printable strings with `strings`.

## Intended Solve Path

```bash
file what_am_i
strings what_am_i | grep 'sentctf{'
```

Expected relevant output:

```text
sentctf{5tr1ng5_4r3_n0t_53cr3t}
```

Submit the flag exactly as shown.

## Why It Works

The program references a string constant so the compiler keeps it in the compiled binary. Stripping removes symbol and debug information, not ordinary printable program data.

## Hints

1. The program may contain more than what it prints.
2. Look for readable text inside the binary.
3. Try the `strings` command.

## Reviewer Notes

Verify that normal execution prints only `Nothing interesting here.` and that the complete flag appears as one line in `strings` output. The direct `strings` route is intentional; no other concept is required.

## Build And Test

From `rev/` on Windows:

```powershell
.\build-all.ps1
.\test-all.ps1
```

No service, network connection, reset, facilitator action, or physical component is required.

## Final Flag

`sentctf{5tr1ng5_4r3_n0t_53cr3t}`
