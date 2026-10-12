# Solution: [Strike TOTO]

## Challenge Details

- **Category:** Pwn
- **Author:** [Rushaidy]
- **Difficulty:** 2/5

## Key Concepts

- Binary analysis
- Reverse engineering
- GDB/Ghidra
- Function analysis
- Stack buffer overflow
- Integer representation (Hexadecimal to Decimal)
- Pwntools
- Remote exploitation

## Intended Solve Path

1. Participants are provided with the challenge binary (ELF executable).
2. Run the binary locally or connect to the remote service to understand its behaviour.

```bash
./luckyDraw3
```

or

```bash
nc <host> <port>
```

The program simulates a lucky draw where users are prompted to enter their name before revealing whether they have won.

---

## Step 1: Enumerate Functions

Open the binary in GDB or another reverse engineering tool.

Using GDB:

```bash
gdb luckyDraw3
```

List the available functions.

```gdb
info functions
```

The important functions include:

- `main()`
- `banner()`
- `generateLuckyNumber()`
- `announceLuckyNumber()`
- `win()`

The presence of a `win()` function immediately suggests it may be the intended target.

---

## Step 2: Analyse the Main Function

Inspect the `main()` function to understand the program flow.

Participants should notice that:

- User input is copied into a fixed-size stack buffer.
- More bytes are accepted than the buffer can safely store.

This indicates a classic **stack buffer overflow** vulnerability.

---

## Step 3: Determine the Winning Number

Since this is a lucky draw program, simply overflowing the buffer is insufficient.

Participants should inspect either:

- `announceLuckyNumber()`
- `win()`

Inside `announceLuckyNumber()`, they will observe a comparison similar to:

```c
if (luckyNumber == PRIZE_NUMBER)
```

The comparison uses the hexadecimal value:

```text
0x43
```

Converting the hexadecimal value to decimal gives:

```text
67
```

This is the winning lucky number required to trigger the `win()` function.

---

## Step 4: Craft the Exploit

Using the stack layout discovered during analysis, construct an input that:

1. Fills the vulnerable buffer.
2. Overwrites the lucky number variable.
3. Sets its value to **67**.

Participants are expected to develop an exploit script using a framework such as Pwntools.

Before attacking the remote service, the exploit should be tested locally.

Since the binary attempts to read a flag from disk, create a dummy flag file for testing.

Example:

```text
flag.txt
```

```text
sentctf{dummy_flag}
```

---

## Step 5: Exploit the Remote Service

After verifying the exploit locally, connect to the remote challenge instance.

```bash
nc <host> <port>
```

or execute the exploit script against the remote target.

When the overwritten value matches the prize number, the program calls:

```c
win();
```

The flag is then displayed.

---

## Final Flag

```text
SentCTF{y0u_str1ked_jackp0t}
```

## Hints

1. Not every function in the binary is equally important.
2. A lucky draw always has a winning number.
3. Numbers stored in hexadecimal may need another representation.
4. Inspect how user input is stored in memory.

## Notes For Reviewers

This is an introductory binary exploitation challenge designed to familiarise participants with reverse engineering and stack buffer overflows. Rather than overwriting a return address, participants must understand the program logic, identify the winning condition, recover the hidden prize number through reverse engineering, and overwrite a nearby stack variable via a buffer overflow. The challenge reinforces function analysis, hexadecimal interpretation, memory layout inspection, and exploit development using standard tools such as GDB, Ghidra, and Pwntools.