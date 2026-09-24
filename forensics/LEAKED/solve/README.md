# Solution: LEAKED

## Challenge Details

- **Category:** Forensics
- **Author:** Mujabeast
- **Difficulty:** 1/5

## Key Concepts

- Image metadata
- EXIF inspection
- Base64 decoding

## Intended Solve Path

1. Open `recovered_midterm_leak.jpg` and observe that there is no obvious visible flag.
2. Inspect the image metadata using a tool such as ExifTool.
3. Find the suspicious `User Comment` value.
4. Recognise the value as Base64 and decode it.
5. Wrap the decoded value in the required flag format.

## Step 1: Inspect The File

The image appears normal when opened visually. There is no visible flag.

## Step 2: Check Metadata

Use ExifTool or another metadata viewer.

```bash
exiftool recovered_midterm_leak.jpg
```

The important field is:

```text
User Comment : c3c0Z21hNXQzcjY3
```

## Step 3: Decode Base64

The value is Base64-encoded.

```text
sw4gma5t3r67
```

## Step 4: Submit The Flag

```text
sentctf{sw4gma5t3r67}
```

## Hints

1. The visible image is not the only part of the file worth checking.
2. Inspect the image metadata.

## Notes For Reviewers

This is a beginner-friendly metadata challenge. The image should look ordinary; the intended evidence is stored in its metadata.
