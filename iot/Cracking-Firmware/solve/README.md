# Intended solve path

**1. Discover the `binwalk --extract` option**

A quick lookup of the binwalk tool help menu will show the `--extract` flag

```shell
$ binwalk --help | grep extract
    -e, --extract                Automatically extract known file types
    ...
```

**2. Extract the root filesystem**

```shell
$ binwalk --extract firmware.bin
$ cd firmware.bin.extracted/squashfs-root
```

**3. Find the location of `flag.txt`**

```shell
$ find . -ipath '*flag.txt' 2>/dev/null
./htdocs/webinc/getcfg/SentCTF/flag.txt

$ cat ./htdocs/webinc/getcfg/SentCTF/flag.txt
sentctf{cr4ck1ng_f!rmw$re}
```
