# Intended solve path

**1. `Q87-E1200V2`**

Players learn how to find the FCC ID from the product name (Linksys E1200 v2)

- A Google search for:

```
linksys e1200 v2 fcc id
```

Provides multiple results with the FCC ID `Q87-E1200V2`

A general search for the router model + researcher name will also yield multiple related results:

```
linksys e1200 jarrettgxz
```

**2. `BCM5357`**

Players learn how to identify the CPU model of this router from: FCC page data entry, or internal Printed Circuit Board (PCB) image

**2.1 FCC page data entry**

- A Google search for

```
linksys e1200 v2 fcc
```

Yields multiple results:

- https://openwrt.org/toh/linksys/e1200_v2 -> find "cpu" on page
- https://fccid.io/Q87-E1200V2 -> https://fccid.io/Q87-E1200V2/Internal-Photos/Internal-Photos-1564096 (internal photos)

**2.2 Researcher notes**

The researcher notes on [Gitbook](https://jarrettgxz-sec.gitbook.io/penetration-testing-ethical-hacking-concepts/iot-hardware-hacking/research-projects/linksys-e1200-v2/1.-initial-research-osint) also provides an image of the internal PCB

Internal PCB image: [openwrt.org data entry](https://openwrt.org/toh/hwdata/linksys/linksys_e1200_v2)
-> [internal PCB image](https://openwrt.org/_media/media/linksys/e1200_v2_serial.jpg?cache=)

The CPU model can be found from the data entry or internal photos: `BCM5357`

**3. `CVE-2025-60690`**

Players learn how to discover publicly available proof-of-concept scripts for CVE IDs on specific vulnerability types (eg. stack buffer-overflow)

- A Google search for:

```
linksys e1200 stack overflow
```

may yield results for multiple CVE IDs, but theres only one the named researcher has worked on: `CVE-2025-60690`

**4. `githubp0c`**

Searching for Github

```
 linksys e1200 jarrettgxz github
```

may not yield any useful results (due to the Github page not really being indexed properly).

Reusing the old query from the previous step with the researcher name:

```
linksys e1200 jarrettgxz stack overflow
```

will yield multiple similar results for **CVE-2025-60690**:

- https://www.exploit-db.com/exploits/52548 (exploit-db)
- https://nvd.nist.gov/vuln/detail/CVE-2025-60690 (NVD NIST)
- https://feedly.com/cve/CVE-2025-60690

Each of them will contain links to the [Github](https://github.com/Jarrettgohxz/CVE-research/tree/main/Linksys/E1200-V2/CVE-2025-60690), which contains the required flag portion at the flag bottom of the page: `githubp0c`

**5. `gitb0ok`**

Gitbook link: https://jarrettgxz-sec.gitbook.io/penetration-testing-ethical-hacking-concepts/iot-hardware-hacking/research-projects/linksys-e1200-v2/1.-initial-research-osint

The gitbook technical write-up page can be found in many of the previously found resources:

- [Github technical write-up](https://github.com/Jarrettgohxz/CVE-research/tree/main/Linksys/E1200-V2/CVE-2025-60690) -> "Comprehensive technical write-up"
- **Google search terms**:
  - `linksys e1200 gitbook` -> [Linksys E1200 v2 research](https://jarrettgxz-sec.gitbook.io/penetration-testing-ethical-hacking-concepts/iot-hardware-hacking/research-projects/linksys-e1200-v2)
  - `linksys e1200 stack overflow gitbook` -> [Linksys E1200 v2 stack-overflow exploit research](https://jarrettgxz-sec.gitbook.io/penetration-testing-ethical-hacking-concepts/iot-hardware-hacking/research-projects/linksys-e1200-v2/5.-reverse-engineering-+-exploit-development)

Navigate to the "Initial researchh (OSINT)" page. Scroll to the bottom to retrieve the flag

**6. FIRMWARE-RELEASE-ID**

- Google search term that works:

```
# returns iotsec.tools "releases" page

site:github.com releases e1200 v2.0.02
site:github.com releases linksys e1200 v2.0.02
site:github.com inurl:releases linksys v2.0.02
site:github.com "e1200 v2.0.02" "releases"

# returns iotsec.tools main page

site:github.com jarrettgxz releases
site:github.com jarrettgxz inurl:releases
```

This will lead to the firmware "releases" page under the **iotsec.tools** project:
https://github.com/Jarrettgohxz/iotsec.tools/releases

Navigation within the researcher's github repository will lead to the **iotsec.tools** project too

Find the release for "Linksys E1200 FW v2.0.02" and retrieve the 7 characters release id: `d973da7`

**7. Combine final flag**

Final flag:
`sentctf{Q87-E1200V2_BCM5357_CVE-2025-60690_githubp0c_gitb0ok_d973da7}`
