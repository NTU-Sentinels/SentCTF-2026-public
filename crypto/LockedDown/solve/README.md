# Solution: LockedDown

## Challenge Details

- **Category:** Crypto
- **Author:** Rush
- **Difficulty:** 3/5

## Key Concepts

- RSA Cryptography
- Public-key encryption
- RSA key generation
- Fermat Factorisation
- Close-prime vulnerability
- RSA decryption
- Python scripting
- Cryptographic misconfiguration

## Intended Solve Path

1. Participants are provided only with the remote challenge service.
2. Connect to the challenge instance using Netcat.

```bash
nc <host> <port>
```

Upon connecting, participants are presented with an interactive escape room where they must investigate various rooms and recover evidence.

No downloadable files are provided beforehand.

---

## Step 1: Explore the Archive

Participants should freely explore each room and interact with the environment.

Available actions include:

- Moving between rooms
- Searching for evidence
- Viewing previously collected evidence
- Unlocking certain areas

Evidence collected remains within the game session and is **not** automatically downloaded to the participant's machine. Players are encouraged to either take notes or repeatedly use the in-game **Read Evidence** option whenever necessary.

Throughout the investigation, numerous documents provide hints regarding the encryption scheme and its weakness.

---

## Step 2: Locate the Critical Evidence

Among the recovered evidence, two files are essential.

```text
public.txt
encrypted_token.txt
```

These can be found in:

- The Server Room
- The Server Room locker

The files contain the RSA public parameters.

Example:

```text
public.txt
------------
n = ...
e = ...
```

```text
encrypted_token.txt
-------------------
ciphertext = ...
```

Participants now possess everything required to recover the emergency access token.

---

## Step 3: Identify the RSA Weakness

The remaining evidence scattered throughout the archive provides clues regarding the implementation of RSA.

Participants should conclude that the modulus was generated using **two very close prime numbers**, making it vulnerable to **Fermat Factorisation**.

The intended cryptographic weakness is therefore:

```text
Close Prime Vulnerability
```

rather than brute-forcing or attacking the public exponent.

---

## Step 4: Recover the Private Key

Participants are expected to implement (or use) Fermat Factorisation to recover the RSA prime factors.

Once the modulus has been factored:

1. Recover **p** and **q**
2. Compute:

```text
φ(n) = (p − 1)(q − 1)
```

3. Calculate the private exponent:

```text
d = e⁻¹ mod φ(n)
```

Participants are free to use any programming language or cryptographic library of their choice.

Writing a short Python script is the intended approach.

---

## Step 5: Decrypt the Access Token

Using the recovered private key, decrypt the ciphertext contained in:

```text
encrypted_token.txt
```

This reveals the emergency access token required to unlock the archive exit.

---

## Step 6: Escape the Archive

Return to the Exit Door within the game.

Enter the recovered access token when prompted.

If the decrypted value is correct, Lockdown Mode is lifted and the archive door opens.

The flag is then displayed.

---

## Final Flag

```text
SentCTF{esc4p3d_fr0m_rsa_h3ll}
```

## Hints

1. Every recovered document serves a purpose.
2. The public key alone is not always secure if generated incorrectly.
3. Consider how the modulus may have been constructed.
4. Sometimes factoring becomes much easier than expected.

## Notes For Reviewers

This challenge is designed as an interactive cryptography-themed escape room rather than a traditional static RSA problem. Participants must first explore the environment, gather evidence, and infer the cryptographic weakness before performing any mathematical attack. The intended solution is **Fermat Factorisation**, exploiting an RSA modulus generated from two unusually close prime numbers. After recovering the private key and decrypting the emergency access token, participants return to the game to unlock the archive and complete the challenge. The challenge reinforces both practical RSA concepts and the importance of secure key generation, while encouraging participants to combine investigation with cryptanalysis.
