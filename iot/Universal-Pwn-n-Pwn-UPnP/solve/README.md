# Intended solve path

**1. Simple Service Discovery Protocol (SSDP)**

Use the provided `m-search.py` script to send UDP M-SEARCH to port 1900

**2. GET device.xml**

We can use a HTTP client such as: `wget`, `curl` to send a HTTP GET request

- read the `SCDPURL` value

**3. GET deviceconfig.xml**

**4. Enumerate SOAP actions**

After retrieving `deviceconfig.xml`, we can enumerate the possible SOAP actions.

- this can be sent to the value we have found in the `controlURL` field from `device.xml` field previously: **/upnp/control/deviceconfig** in our case

**5. Send POST SOAP requests**

Send SOAP request to each endpoints found previously

- we will notice that none of them returns any useful values

Remember that the challenge description hints toward needing to reverse the `upnpd` binary

<img width="1034" height="549" alt="image" src="https://github.com/user-attachments/assets/3b8f8a5b-4b84-4b83-9f68-fbc98d40ad84" />
<img width="1034" height="814" alt="image" src="https://github.com/user-attachments/assets/59a90c09-4ea6-4c6d-8c87-2ef64ecbf86e" />
<img width="1034" height="814" alt="image" src="https://github.com/user-attachments/assets/80741164-1c84-4810-ae3e-cbd4a2aa0c26" />
<img width="1229" height="593" alt="image" src="https://github.com/user-attachments/assets/eede6813-3816-45da-b625-ff341928f9f9" />
<img width="918" height="693" alt="image" src="https://github.com/user-attachments/assets/68a3c9e7-af5a-451e-98d3-2153280fac1d" />

<img width="1264" height="749" alt="image" src="https://github.com/user-attachments/assets/cb2dc155-d224-42fc-952d-a478ca1c2b94" />
<img width="1264" height="676" alt="image" src="https://github.com/user-attachments/assets/8b2768c6-2cf0-4f65-b18e-8351e59bf50c" />
