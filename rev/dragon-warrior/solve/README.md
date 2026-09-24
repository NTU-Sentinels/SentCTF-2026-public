# Solution: Dragon Warrior 1

## Challenge Summary

`dragon_warrior_1` is a 64-bit Linux ELF program. It accepts one phrase and opens the Dragon Scroll only when every character is correct. The program deliberately keeps readable function names, making it a first look at Ghidra's Decompiler.

## Intended Solve

1. Download `dragon_warrior_1` from the challenge page.
2. Open Ghidra. Select **File** -> **New Project**.
3. Choose **Non-Shared Project**, then choose a folder and project name such as `dragon-warrior-1`.
4. In the Project window, select **File** -> **Import File** and choose `dragon_warrior_1`.
5. Double-click the imported file. When Ghidra asks whether to analyse it, click **Yes**.
6. Keep the default analysis options and click **Analyse**. Wait until analysis finishes.
7. On the left, find **Symbol Tree**. Expand **Functions**.
8. Double-click `main`. In the Decompiler window, find the call to `check_dragon_warrior`.
9. Double-click `check_dragon_warrior`. Its decompiled code checks the input length and then compares individual characters:

```text
input[0] == 'i'
input[1] == 'n'
input[2] == 'n'
...
```

10. Write the characters down in index order. They spell `inner_peace`.
11. Open a terminal in the folder containing the downloaded binary and run:

```bash
chmod +x dragon_warrior_1
./dragon_warrior_1
```

12. At `Enter the secret phrase:`, type exactly `inner_peace`.
13. The program prints `The Dragon Scroll opens.` followed by `sentctf{th3_dr4g0n_scr0ll}`.

## Why This Works

`main` passes the entered text into `check_dragon_warrior`. That function checks each expected character directly rather than storing the secret as one normal string. On success, `reveal_dragon_scroll` decodes and prints the flag.

## Reviewer Notes

- Correct phrase: `inner_peace`
- Wrong input prints `You are not the Dragon Warrior.`
- The distributed binary contains neither the complete phrase nor the flag as a normal plaintext string.
