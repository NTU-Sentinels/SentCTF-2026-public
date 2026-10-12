# Solution: Prime Suspects

## Challenge Details

- **Category:** Crypto
- **Author:** Mujabeast
- **Difficulty:** 1/5
- **Value:** 100 points

## Key Concepts

- RSA key construction
- Calculating `n` and Euler's totient
- Modular inverses
- Text-to-integer and integer-to-text conversion

## Intended Solve Path

1. Read `p`, `q`, `e`, and `c` from `rsa_parameters.txt`.
2. Calculate `n = p * q`.
3. Calculate `phi = (p - 1) * (q - 1)`.
4. Recover the private exponent with `d = e^-1 mod phi`.
5. Decrypt with `m = c^d mod n`.
6. Convert the plaintext integer to bytes and read the flag.

## Detailed Walkthrough

### Step 1: Open A Terminal In The Download Folder

```bash
cd ~/Downloads
ls
```

Confirm that `rsa_parameters.txt` appears in the output.

### Step 2: Read The Supplied Values

```bash
cat rsa_parameters.txt
```

The file provides the two primes `p` and `q`, the public exponent `e`, and the ciphertext `c`.

### Step 3: Reconstruct The Private Key And Decrypt

Enter the following command exactly. After typing the final `PY`, press Enter.

```bash
python3 - <<'PY'
p = 13183170791428551076382706417537366308741690296103920563975563247628528203949239179272907935356437685040523167590380773443662574661274253458398359053427379
q = 12418370253593242931532006421397235974001548936438336138224060713087604932537142560347957297239106462590216666093419895637049907879062360304531808200189871
e = 65537
c = 31525575701843101904939811044328758455413182327797362922342145639394587024188114135317804237295217037469301044421212839782194269543198226887339403542557623658921214418402711240251579898625589711937787205092440409495150242322762600571561578371014873145584050645207767542671628300043572302047431804173424130681

n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)

plaintext = m.to_bytes((m.bit_length() + 7) // 8, "big")
print(plaintext.decode())
PY
```

Expected output:

```text
RSA RECOVERY COMPLETE
Flag: sentctf{f4ct0r5_bu1ld_th3_k3y}
Next case: PRIME_SUSPECTS_PART_2
```

`pow(e, -1, phi)` calculates the modular inverse of `e`, producing the private exponent `d`. `pow(c, d, n)` then performs RSA decryption efficiently.

### Step 4: Submit The Flag

```text
sentctf{f4ct0r5_bu1ld_th3_k3y}
```

The recovered `PRIME_SUSPECTS_PART_2` case name connects this challenge to the follow-up RSA challenge.

## Hints

1. Use `n = p * q` and `phi = (p - 1) * (q - 1)`.
2. Python can calculate `d` with `pow(e, -1, phi)`, then decrypt with `pow(c, d, n)`.

## Notes For Reviewers

This beginner challenge teaches the normal RSA private-key construction process. Supplying `p` and `q` keeps the focus on RSA mathematics rather than integer factorisation.
