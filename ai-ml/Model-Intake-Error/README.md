# Organiser Solution: AI Easy Challenge

> Organiser-only document. Put the approved version in `solve/README.md`. Do
> not give it to players because it contains every answer and the final flag.

## Challenge Summary

- Category: AI/ML
- Difficulty: Easy
- Author: Jeral
- Source: `Model_Intake_Error.py`
- Implemented title: Prompt Rewrite
- Expected solve time: 10–15 minutes

An NTU recovery assistant responds with gibberish because its active system
prompt deliberately prevents useful answers. Players inspect the source,
identify the prompt-selection variable, activate the helpful prompt, restart
the application, and ask for the secret flag.

## Hints for the Current Code

1. "The model is following its active instruction exactly."
2. "Inspect the constants near `ACTIVE_PROMPT`."
3. "Change the selected prompt, save the file, and restart the service."
4. "Once the status is helpful, ask directly for the secret flag."

## Flag

`sentctf{prompt_rewrite_restored}`
