# Hidden Gem - Solution

## Key Concepts

- Identifying data embedded inside a JPEG image
- Extracting a hidden file with `steghide`
- Using open-source information to identify a location and derive a passphrase

## Intended Solve Path

### 1. Inspect the supplied image

Download `hidden_gem.jpg`, open a terminal in the download directory, and confirm that it is a JPEG image:

```bash
file hidden_gem.jpg
```

The picture does not visibly contain the flag. Check whether `steghide` detects embedded data:

```bash
steghide info hidden_gem.jpg
```

When prompted to display information about the embedded data, enter `y`. Steghide then requests a passphrase.

### 2. Identify the passphrase

The challenge states that the photograph was taken at an NTU food spot inside the School of Biological Sciences. Search the web for terms such as:

```text
NTU School of Biological Sciences cafeteria
```

The location is **Quad Cafe**. Following the usual lowercase, no-space passphrase format gives:

```text
quadcafe
```

### 3. Extract the hidden file

Run:

```bash
steghide extract -sf hidden_gem.jpg
```

Enter the following passphrase when prompted:

```text
quadcafe
```

Steghide extracts `flag.txt` into the current directory.

### 4. Read and submit the flag

```bash
cat flag.txt
```

The file contains:

```text
sentctf{why_a1way5_cr0wd3d}
```

Submit that exact value to CTFd.

## Hint

`Use steghide.`

## Notes for Reviewers

The visible photograph is a JPEG cover file. `flag.txt` is embedded with `steghide` and protected by the passphrase `quadcafe`. The passphrase is intentionally derived from the stated NTU location through a short OSINT lookup.
