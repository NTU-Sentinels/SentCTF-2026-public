# Are We There Yet Solution

## Challenge Summary

Players receive `lecture_notes.zip`, which contains `lecture_01.pdf`. Each PDF is valid, but also has a ZIP archive appended to it. That archive contains the next numbered PDF. There are 20 layers in total, and the final embedded ZIP contains the lecture notes with the flag written inside them.

The first few layers can be extracted manually. The intended lesson is to recognise the repetition, inspect Binwalk's help, and use recursive Matryoshka extraction with a recursion depth greater than the default.

## Flag

`sentctf{why_pr0f_g4t3k33p1ng}`

## Intended Solve Path

### 1. Extract the supplied archive

```bash
unzip lecture_notes.zip
ls -la
```

The archive contains only `lecture_01.pdf`.

### 2. Identify and inspect the first PDF

```bash
file lecture_01.pdf
binwalk lecture_01.pdf
```

`file` identifies a valid PDF. Binwalk also detects ZIP data appended after the PDF.

### 3. Extract a layer manually

```bash
binwalk -e lecture_01.pdf
find . -type f
```

The extracted ZIP contains `lecture_02.pdf`. Repeating the same process reveals `lecture_03.pdf`, then `lecture_04.pdf`, and so on.

### 4. Look for a recursive option

Manually repeating the extraction 20 times is possible but deliberately inefficient. Inspect Binwalk's available options:

```bash
binwalk --help
```

The relevant options are:

```text
-M, --matryoshka    Recursively scan extracted files
-e, --extract       Automatically extract known file types
-d, --depth         Set the recursive extraction depth
```

### 5. Extract all layers recursively

Binwalk's usual Matryoshka depth is too low for all 20 layers, so increase it:

```bash
binwalk -Me -d 25 lecture_01.pdf
```

### 6. Locate and read the lecture notes

```bash
find . -type f -name "actual_lecture_notes.txt"
cat "$(find . -type f -name 'actual_lecture_notes.txt' | head -n 1)"
```

The final lines are:

```text
Professor's note: You finally found the lecture notes.

sentctf{why_pr0f_g4t3k33p1ng}
```

## Key Concepts

- Linux file navigation with `ls`, `find`, and `cat`
- Identifying files with `file`
- Detecting embedded archives with Binwalk
- Extracting embedded data with `binwalk -e`
- Automating repetitive forensic extraction with Matryoshka mode
- Adjusting recursive extraction depth

## Hints

1. `The file may contain more than its extension suggests. Try examining it with file and binwalk` (10 points)
2. `Read binwalk --help` (20 points)

## Notes for Reviewers

- `lecture_notes.zip` must contain only `lecture_01.pdf`.
- There must be exactly 20 numbered PDF layers.
- Every numbered file must be a valid PDF with an appended ZIP containing the next layer.
- The final embedded ZIP must contain only `actual_lecture_notes.txt`.
- `actual_lecture_notes.txt` must contain the flag on its final line.
- The flag must not appear as plaintext in the distributed outer ZIP or first PDF.
- Recursive extraction must require a depth greater than Binwalk's usual default.
- CTFd must value the challenge at 100 points and charge for both hints.
