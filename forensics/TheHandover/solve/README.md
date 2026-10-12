# Solution: [The Handover]

## Challenge Details

- **Category:** Forensics
- **Author:** [Rushaidy]
- **Difficulty:** 3/5

## Key Concepts

- AD1 forensic image analysis
- QR code investigation
- Open-source intelligence (OSINT)
- Hieroglyph deciphering
- Password cracking using clues
- Pigpen cipher
- Image metadata analysis
- ROT18 decoding
- Caesar cipher
- Morse code
- Audio steganography (Steghide)
- Spectrogram analysis

## Intended Solve Path

1. Open the forensic image `CSONTU.ad1` using a forensic tool such as FTK Imager, Arsenal Image Mounter, or another AD1-compatible tool.
2. Browse to `PUZZLE/NTU/L` and extract the available evidence.
3. Two files should be recovered:
   - A QR code image
   - A password-protected archive named `nothing.zip`
4. Scan the QR code. It redirects participants to an Instagram profile containing multiple clues.
5. Decipher the hieroglyphics found on the Instagram page. The translation reveals:

```text
scarab
```

This forms the first part of the ZIP password.

6. Read the Instagram bio:

```text
d i m e n s i o n +
```

7. Determine the dimensions of the QR image and add both values together.

```text
Width + Height = 899
```

8. Combine both clues to obtain the ZIP password.

```text
scarab899
```

9. Extract `nothing.zip`.

10. Two folders are revealed:

- `NOISE`
- `SIA`

Participants may solve either branch first.

---

## Branch 1 — SIA Folder

### Step 1: Decode the Pigpen Cipher

Open the provided JPEG image.

A Pigpen cipher is embedded inside the image.

After decoding it, participants obtain a hint directing them to inspect the image further.

### Step 2: Inspect Image Metadata

Use ExifTool or another metadata viewer.

```bash
exiftool image.jpg
```

Near the bottom of the metadata is another encoded string.

The string is encoded using ROT18.

After decoding, it reveals the rendezvous location:

```text
Pulau Satumu
1°09'35.9"N 103°44'27.0"E
```

This is the first portion of the final flag.

---

## Branch 2 — NOISE Folder

### Step 1: Read the README

The folder contains:

- README.txt
- Audio file

The README contents are encrypted using a Caesar cipher.

After decoding, it reads:

```text
Your passphrase is Vanessa
```

This is the password required later.

### Step 2: Decode the Morse Code

Play the supplied audio file.

The audio is Morse code.

It decodes to:

```text
Investigate this file with steghide to carry on with your mission
```

### Step 3: Extract Hidden Data

Use Steghide together with the recovered password.

```bash
steghide extract -sf audio.wav
```

Password:

```text
Vanessa
```

A second audio file is extracted:

```text
RiddleMETHISV2.wav
```

### Step 4: Analyse the Spectrogram

Open the extracted audio using software capable of displaying spectrograms (e.g. Sonic Visualiser, Audacity, Spek).

A hidden riddle appears in the spectrogram.

Solving it reveals the rendezvous date and time:

```text
07/02/2026 @ 0000hrs
```

This forms the second portion of the final flag.

---

## Final Flag

Participants combine:

- Rendezvous location
- Rendezvous date and time

to construct the final flag.

Example:

```text
sentctf{pulau_satumu_07022026_0000hrs}
```

## Hints

1. Every clue has a purpose. Don't stop after finding the ZIP archive.
2. The QR code contains more than just a link.
3. There may be information hidden in files that cannot be seen normally.
4. Not all audio is meant to be listened to.

## Notes For Reviewers

This challenge is designed as a multi-stage forensic investigation combining digital forensics, OSINT, classical ciphers, steganography, metadata analysis, and audio forensics. Participants are expected to pivot between multiple evidence sources while recognising hints that guide them to the next stage. The challenge intentionally allows the two extracted folders (`SIA` and `NOISE`) to be solved independently before combining both discoveries to recover the complete flag.
