# Solution: Prime Suspects: Part 2

## Challenge Details

- **Category:** Crypto
- **Author:** Mujabeast
- **Difficulty:** 2/5
- **Value:** 200 points
- **Recommended predecessor:** Prime Suspects

## Key Concepts

- RSA moduli are products of two primes
- Reusing a prime across RSA keys breaks both keys
- Greatest common divisor attacks
- Reconstructing an RSA private key

## Intended Solve Path

1. Read `e`, `n_a`, `n_b`, and `c` from `captured_keys.txt`.
2. Calculate `gcd(n_a, n_b)`.
3. Recognise the non-trivial result as the shared prime `p`.
4. Factor the target modulus with `q_b = n_b // p`.
5. Reconstruct the private exponent for `n_b`.
6. Decrypt the ciphertext and convert the plaintext integer to text.

## Detailed Walkthrough

### Step 1: Open A Terminal In The Download Folder

```bash
cd ~/Downloads
ls
```

Confirm that `captured_keys.txt` appears in the output.

### Step 2: Read The Captured Values

```bash
cat captured_keys.txt
```

The protected message was encrypted for `n_b`. The second modulus, `n_a`, is included because the two keys may not be independent.

### Step 3: Find The Shared Prime And Decrypt

Enter the following command exactly. After typing the final `PY`, press Enter.

```bash
python3 - <<'PY'
from math import gcd

e = 65537
n_a = 115843987949903940858608738201725413773126539230955492783137526771590030284432400664484034216965237504237709220424808787692762997129717429501422955589000748635896049682942954147398490695139114126482649441588234675774744618641155461283924879546167501274287120620454641106461464996165095163308994454893197272243
n_b = 110200146262800327789768357610549761990723182959363142956402355898764965878735254216683726255901114692318912934445677421073542014252221280333858807754415519323158144453423511079113123663003871693939083247399149762504402985070573934860662672461789197297109872964866329699644129809587357586968188807672508628663
c = 29802716995151187760636869916107965358375249565594715211567426596493200899907481569159904906462235939668966185864500632803029431707587829469788599873439288676811922905516007335067830666457527758975253098887043229904958303056575120814608156785069543451527402520209722395646241605790780743432839495867025741287

p = gcd(n_a, n_b)
q_b = n_b // p
phi_b = (p - 1) * (q_b - 1)
d_b = pow(e, -1, phi_b)
m = pow(c, d_b, n_b)

print(f"shared prime = {p}")
plaintext = m.to_bytes((m.bit_length() + 7) // 8, "big")
print(plaintext.decode())
PY
```

Expected output:

```text
shared prime = 12969878687210734169725370852702107963291791205879981534969246073051690806981060949573821700986993519709785477293123384307472011966540705954444091494986193
RSA AUDIT COMPLETE
Flag: sentctf{gcd_br34k5_r3u53d_r54}
```

If two RSA moduli share a prime, their greatest common divisor is that prime. Once `p` is known, the target modulus can be divided to recover `q_b`, allowing the private key to be rebuilt exactly as in Prime Suspects.

### Step 4: Submit The Flag

```text
sentctf{gcd_br34k5_r3u53d_r54}
```

## Hints

1. Compare the two RSA moduli with `math.gcd(n_a, n_b)`.
2. A non-trivial GCD is a shared prime. Use it to factor the target modulus and reconstruct its private key.

## Notes For Reviewers

This challenge extends Prime Suspects by removing the supplied primes. Players instead exploit a realistic RSA key-generation failure, recover a factor with GCD, and reuse the private-key reconstruction process learned in the first challenge.
