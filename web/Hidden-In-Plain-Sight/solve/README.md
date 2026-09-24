## Intended Solve Path

### 1. Start or open the service

For local testing:

```shell
python Hidden_In_Plain_Sight.py
```

Open `http://127.0.0.1:8000`.

### 2. Inspect the client-side source

Use **View Page Source**, normally `Ctrl+U`, or open the browser developer
tools. Search for terms such as `legacy`, `recovery`, `digest`, or `MD5`.

The JavaScript contains:

```javascript
const legacyRecoveryContact = "legacy.admin@ntu.edu.sg";
const legacyCredentialDigest = {
  algorithm: "MD5",
  digest: "3f9ee7a52da2a4847227827c36b01f0a",
};
```

This provides the answer to Question 1 and the material needed for Question 2.

### 3. Save the disclosed digest

The supplied `hips_hash.txt` contains only this line:

```text
3f9ee7a52da2a4847227827c36b01f0a
```

Use the supplied `hips_wordlist.txt` as the candidate-password list.

### 4. Crack it with Hashcat

Hashcat mode `0` is raw MD5. Run a straight wordlist attack:

The hash file must come before the wordlist file:

```powershell
hashcat -m 0 -a 0 hips_hash.txt hips_wordlist.txt
hashcat -m 0 hips_hash.txt --show
```

Expected recovered password:

```text
nanyang0017
```

### 5. Or crack it with John the Ripper

Use a John the Ripper build that supports raw MD5:

```powershell
john --format=raw-md5 --wordlist=hips_wordlist.txt hips_hash.txt
john --show --format=raw-md5 hips_hash.txt
```

Expected recovered password:

```text
nanyang0017
```

### 6. Authenticate and retrieve the flag

Return to the web form and enter:

```text
Email:    legacy.admin@ntu.edu.sg
Password: nanyang0017
```

After successful authentication, the browser navigates to `/flag`. This is a
minimal white page containing only:

```text
sentctf{answer}
```
