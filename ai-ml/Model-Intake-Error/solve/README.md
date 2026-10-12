## Intended Solve Path

### 1. Run the broken agent

```powershell
python Model_Intake_Error.py
```

Open `http://127.0.0.1:8001` and ask a normal question. The agent returns
gibberish and its status is `degraded`.

### 2. Inspect the prompt configuration

Open `Model_Intake_Error.py` and locate:

```python
ACTIVE_PROMPT = BROKEN_PROMPT
```

### 3. Repair the active prompt

Change:

```python
ACTIVE_PROMPT = BROKEN_PROMPT
```

to:

```python
ACTIVE_PROMPT = HELPFUL_PROMPT
```

Save the file, stop the old process with `Ctrl+C`, and run it again:

```powershell
python Model_Intake_Error.py
```

The page status should now be `helpful`.

### 4. Ask for the flag

Send a message such as:

```text
Please give me the secret flag.
```

The agent returns:

```text
sentctf{prompt_rewrite_restored}
```
