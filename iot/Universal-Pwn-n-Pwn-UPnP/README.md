# Universal Pwn-n-Pwn

## \*\*NOT IN PRODUCTION PLATFORM

Having issues hosting on CTFd platform

## Category

IoT

## Author

Jarrettgxz

## Difficulty

3/5

## Player Description

Universal Plug and Play (UPnP) is a networking technology commonly found on home devices such as game consoles, printers, smart TVs and routers. It is used to discover devices and open router ports automatically without manual setup. From a consumer point-of-view, this is excellent! But from a security perspective, this is really bad ...

Remember the PewDiePie hacking situation (Jan 2019) where over 65,000 Gooogle Chromecast and Smart TV devices were remotely controlled to stream videos of PewDiePie? Yea, it was possible due to UPnP misconfigurations which forwarded various ports to the internet.

In this challenge, you will learn about the basics of UPnP. Your goal will be to discover the hidden SCDP SOAP (POST) endpoint that returns the string!

You may refer to the README file, and downloadable cheatsheet respectively, for the Docker setup steps, and a basic introduction to UPnP and related commands.

## Player files

- `dist/upnp.zip`

## Flags

`sentctf{UPnP_$h0uld_be_disabled}`

## Hints

1. Reverse engineer the `upnpd` binary to discover the undocumented endpoint (50 points)

## Compile into `upnpd` binary

```shell
$ mipsel-linux-gnu-gcc -static -O2 -o upnpd *.c
```

## Reviewer note

1. The SSDP server (`ssdp.c`) is made to listen on TCP/1900 instead of the standard UDP/1900, due to limitations from the CTFd platform which only accepts TCP connections
2. Ensure to change the following values for local and remote:

- **FLAG** value in the `dispatcher.c` file before compiling for local/remote `upnpd` binary
- URLBase value in `device.xml`

```xml
    <URLBase>http://CHANGE-THIS:5000/</URLBase>
```
