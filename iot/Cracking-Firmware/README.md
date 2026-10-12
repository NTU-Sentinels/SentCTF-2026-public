# Cracking-Firmware

## Category

IoT

## Author

Jarrettgxz

## Difficulty

1/5

## Player Description

You have gained access to a firmware file from a router. A firmware is essentially the software portion of IoT devices such as routers. To solve this challenge, you have to extract the filesystem within the provided firmware using the `binwalk` tool, and read `flag.txt`.

**Useful commands**

```shell
binwalk --help
```

**Learning outcomes**

1. Firmware extraction
2. Basic filesystem enumeration

## Player Files

- `dist/firmware.bin`

## Flag

`sentctf{cr4ck1ng_f!rmw$re}`

## Hints

1. binwalk --help | grep extract (**10 points**)
2. binwalk --extract firmware.bin (**10 points**)
