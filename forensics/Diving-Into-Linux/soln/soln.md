## Solution
To solve this, first we need to import the OVA file to any application that can run VM.

As users first log in, they realise they dont have the password.

As such, users need to interrupt the bootloader so that they can bypass and create shell by rapidly pressing e and then tab to edit the boot entry.

Type the following into the bootloader at the end of the line.

```
init=/bin/sh
```

Once in they will need to mount the file system to read write as they need to change the password.

```
mount -o remount, rw /
```

they will need to change the password by using the following command (can change to anything they want)

```
passwd root
```

then to ensure that everything is updated, use the following command

```
sync
reboot -f
```

Once in, they will need to find the flag which is hidden secretly in one of the files in /etc, users can easily do this by using the grep command

```
grep -r "sentctf" /etc
```
