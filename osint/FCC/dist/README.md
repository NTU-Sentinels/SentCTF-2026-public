# Steps to craft the final flag

Combine 5 different specific terms relating to the Linksys E1200 (v2) router using the **\_** symbol

**Flag format:**
`sentctf{FCC-ID_CPU-MODEL_STACKOVERFLOW-CVE-ID_GITHUB_GITBOOK_FIRMWARE-RELEASE-ID}`

eg.  
`sentctf{Qxx-xxxxx_BCMxxxx_CVE-xxxx-xxxxx_gxxxxxxxx_gxxxxxx_xxxxxxx}`

**1. FCC-ID**

- The FCC ID of the target router model in the format: **Qxx-xxxxx**

**2. CPU-MODEL**

- The model of the CPU in the format: **BCMxxxx** where **xxxx** is a 4-digit number

**3. STACKOVERFLOW-CVE-ID**

The target router contains a stack buffer-overflow based vulnerability. The named researcher have done extensive research to craft a working exploit script for the vulnerability with a particular CVE ID.

CVE stands for the Common Vulnerabilities and Exposures, and industry-standard catalog system for publicly disclosed computer security flaws, each signed with a particular ID number in the format: **CVE-YEAR-ID** (**CVE-xxxx-xxxxx**), eg. **CVE-2026-12345**

**4. GITHUB and GITBOOK**

The named researcher has published his work on multiple sites such as Github and Gitbook notes. Find these resources and retrieve the 4th and 5th flag portions!

You may also find him on Youtube and Instagram! (@jarrettgxz)

**5. FIRMWARE-RELEASE-ID**

It is possible to perform security research on an IoT device without having access to the physical hardware. This can be done by working directly on the _firmware_ file: the software portion of the hardware that contains the operating system, filesystem, configuration values and other useful information for our research.

To retrieve the last portion of the flag, you are required to use your Google dorking skills to find the Github repository that provides the downloadable firmware file for the Linksys E1200 v2.0.02 router under the "releases" tab. Finally, retrieve the release id (7 character string), which forms the final portion of the flag!
