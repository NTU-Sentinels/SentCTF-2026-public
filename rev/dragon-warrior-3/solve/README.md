# Solution: Dragon Warrior 3

## Challenge Summary

`dragon_warrior_3` is a stripped 64-bit Linux ELF program. It expects a 16-character phrase. The real validator transforms every byte, compares the transformed bytes using a shuffled index order, and has a couple of redundant relationship checks. A small Python program reverses the transformation.

## Find The Real Validator In Ghidra

1. Download `dragon_warrior_3`.
2. In Ghidra, create a **Non-Shared Project** with **File** -> **New Project**.
3. Import the binary. Double-click it, click **Yes** to analyse it, leave the default settings selected, then wait until the analysis completes.
4. In the **Defined Strings** window, search for `The Dragon Scroll opens.`. Double-click the string.
5. Right-click the string and choose **References** -> **Show References To**. Open the code reference. This is the real success path.
6. In the Decompiler, trace backwards to the function that decides whether the input is valid. This function checks that the input has length `0x10` (16).
7. Ignore the unused decoy routines: they have no call path from `main` and no reference from the real success branch.

## Read The Validation Data

The real validator contains these byte arrays:

```text
order  = [5, 2, 14, 1, 9, 7, 0, 12, 4, 15, 6, 3, 10, 8, 13, 11]
target = [104, 92, 124, 72, 116, 115, 83, 140, 100, 134, 122, 89, 112, 113, 116, 102]
```

It builds a transformed array with:

```text
transformed[i] = ((input[i] ^ 0x37) + i * 3) & 0xff
```

It then compares the arrays as:

```text
transformed[order[i]] == target[i]
```

The other checks are sanity checks. In the decompiler they are equivalent to:

```text
input[0] + input[15] == 210
input[3] ^ input[10] == 2
input[6] - input[2] == -2
```

## Reverse The Transformation

Create a file named `solve.py` and paste this exact code:

```python
order = [5, 2, 14, 1, 9, 7, 0, 12, 4, 15, 6, 3, 10, 8, 13, 11]
target = [104, 92, 124, 72, 116, 115, 83, 140, 100, 134, 122, 89, 112, 113, 116, 102]

# Put each shuffled target byte back in its original transformed position.
transformed = [0] * 16
for i in range(16):
    transformed[order[i]] = target[i]

# Undo + i*3 first, then undo XOR 0x37.
answer = []
for i in range(16):
    original = ((transformed[i] - (i * 3)) & 0xff) ^ 0x37
    answer.append(chr(original))

print(''.join(answer))
```

Run it in the same terminal:

```bash
python3 solve.py
```

Output:

```text
dragon_inner_zen
```

## Run The Challenge

```bash
chmod +x dragon_warrior_3
./dragon_warrior_3
```

When asked for the Dragon Scroll phrase, enter `dragon_inner_zen`.

The program prints `The Dragon Scroll opens.` followed by `sentctf{1nn3r_p34c3_4ch13v3d}`.

## Reviewer Notes

- Correct phrase: `dragon_inner_zen` (exactly 16 characters)
- The decoy routines are deliberately unreachable from `main`.
- The distributed binary contains no plaintext copy of the correct phrase or real flag.
