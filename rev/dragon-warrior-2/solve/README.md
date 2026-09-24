# Solution: Dragon Warrior 2

## Challenge Summary

`dragon_warrior_2` is a stripped 64-bit Linux ELF program. Unlike Dragon Warrior 1, its own function names are removed, so Ghidra displays names such as `FUN_00401186`. The password is checked across several small functions.

## Intended Solve

1. Download `dragon_warrior_2` and open Ghidra.
2. Create a **Non-Shared Project**: **File** -> **New Project** -> **Non-Shared Project**.
3. Import `dragon_warrior_2`, double-click it, choose **Yes** when prompted to analyse, retain the defaults, and wait for analysis to finish.
4. In **Symbol Tree**, open `main` if Ghidra recovered that name. If it did not, open the function reached from the entry point that prints `JADE PALACE SECURITY`.
5. In the Decompiler, find the function call which receives the player input and returns true or false. Double-click that function. It calls three smaller validation functions.
6. Inspect the first routine. It gives the first three characters directly:

```text
input[0] == 0x70   -> p
input[1] == 0x30   -> 0
input[2] == 0x34   -> 4
```

7. Inspect the next routine. It checks the middle characters using small operations:

```text
(input[3] ^ 0x20) == 0x4e  -> 0x4e ^ 0x20 = 0x6e = n
input[4] + 3 == 0x67       -> 0x67 - 3 = 0x64 = d
(input[5] ^ 0x55) == 0x61  -> 0x61 ^ 0x55 = 0x34 = 4
```

8. Inspect the final routine:

```text
input[6] - 5 == 0x1c  -> 0x1c + 5 = 0x21 = !
input[7] + 7 == 0x28  -> 0x28 - 7 = 0x21 = !
```

9. Combine all recovered characters in index order: `p04nd4!!`.
10. Run the downloaded binary:

```bash
chmod +x dragon_warrior_2
./dragon_warrior_2
```

11. Enter `p04nd4!!`. It prints `The Dragon Warrior has returned.` followed by `sentctf{n0_s3cr3t_1ngr3d13nt}`.

## Reviewer Notes

- Correct code: `p04nd4!!`
- Wrong input prints `The scroll remains sealed.`
- Function names are intentionally stripped in the distributed binary.
- The complete code and flag do not occur as normal plaintext strings in the distributed binary.
