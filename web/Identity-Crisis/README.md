# Challenge details

- **Challenge name**: Identity Crisis
- **Category**: Web
- **Author**: So Cheuk Hong

## Challenge Description

Thanks to the combined efforts of the participants, NTU Staff have since upgraded their authentication system by following the feedback, incorporating SSO into their login flow and moving away from LDAP server for authentication.
Confident, they now task you with another security assessment of their webpage.
Giving you the following credentials for testing.

- user: sentinelstaff01
- password: S3ntCTF@NTU!

However, you have a feeling that it isn’t as secure as they make it out to be…

Task:
Find and piece together the flag in this format: sentctf{A_B}

- A. Note the employee number of the third staff account created
- B. Login as the admin through their new login page.

# **Player files**:

```
- Identity Crisis
	- keycloak\
		- https_keypair\
			- idp_key.pem
			- idp_cert.crt.pem
		- realm-export.json
	- ldap\
		- bootstrap\
			- 1_bootstrap.ldif
			- 2_serviceaccount.ldif
			- 3_acl.ldif
		- Dockerfile
	- nginx\
		- default.conf
	- sp-flask\
		- idp_certs\
			- idp_cert.crt.pem
		- static\
			- legacy_login_style.css
			- legacy_main_style.css
			- main_style.css
		- templates\
			- legacy_admin.html
			- legacy_profile.html
			- legacy_login.html
			- sso_admin.html
			- sso_profile.html
		- app.py
		- Dockerfile
		- requirements.txt
		- session_tracking.py
	- .env
```

# Learning outcomes

SSO is a great under appreciated thing, login once and all nearly services under your org that you would normally have to sign into again is already managed for you.
It is also something that can be exploited if not configured well, I had fun encountering such challenges in other CTFs, and I wish to share the same joy of learning with you all.

# **Hints**:

1. (LDAP) Is there a way to retrieve a specific username from an ldap server?
2. (LDAP) What are applicable syntaxes for an ldap filter?
3. (SAML) How does a user send information back to the IDP?
4. (SAML) How does an IDP verify the user credentials before authenticating them?

# **Flag**

- `sentctf{Ld4p_1nj3C+_S4ML_S1gn4+ure3_Byp4ss3d}`

## **Steps to solve**:

- Start-up the service by running `docker compose up -d` and waiting until all services are up.
  - The supplied files should auto-configure the Keycloak server accordingly so there should be no need to access its admin console.
  - We start from the site: `localhost:49155/login`.

* Flag is in format of sentctf{A_B}
  - **A** is a flag found via ldap injection by logging in as a specific user.
  - **B** is a flag found via the completion of saml signature bypass to log into the admin account.
* Solution to **A** is done by realising ldap server was the means of authentication, then attempting to bypass the login by using wildcards to retrieve a specific user info:
  - Username \= “\*3\*”
  - Password=”\*”
  - This should only need a bit of research and messing around with the fields.

* Solution to B is done by using burp suite to observe the full login flow using the given credentials.
  - Users will eventually see after signing in through the idp page with the given credentials that it redirects them once before finally signing them in to the main page.
    - This redirection contains a SAML response encoded in base64.
      - The user is to parse this response and identify the fields needed to add and edit in order to log in as another user, e.g. Admin.
* This SAML response consists of long XML assertion and signatures detailing the credentials and signature of the user singing in.
  - To achieve the signature bypass, the user is to copy the entire assertion section of the saml response relating to the given user `sentinelstaff01` and paste it in front of the existing one.
  - The user then removes the entire `<dsig:Signature>` section from the copied assertion, as to the idp, it is expecting one signature. Two signatures detected leads to an error and the auth failing.
  - Changing the relevant fields (NameID, employeeType) to the desired options `(admin, admin`)
    - The user just needs to change these two fields to succeed, I got lazy to actively verify everything else. Changing every other user related field wouldn't affect the expected outcome.
    - The user will be able to acquire the relevant details by using LDAP injection to find the admin account details.
      - Username \= “\*”
      - Password=”\*”
      - _Admin account happens to be the last entry in the ldif file, but using Username = Admin is fine too and a acceptable way to find out its details._
* Finally, change the Assertion ID of the injected asserted section to a different UUIDv4 value, this can be any UUIDv4 value, I went online to get a random generated value.
* Inject your edited SAML Response into the SAML response body of burp suite and submit it. If all goes well, you will log in as the admin at the `sso/admin` endpoint rather than `sso/profile`, despite only logging in with the staff credentials given at the start of the challenge.

## **Any other important for the reviewers**

- On initial startup, Keycloak server may take a while to import the realm configuration. Attempting to access the sso login beforehand will lead to 502 error, refresh the page after keycloak properly loads to resolve.
- Keycloak admin interface is blocked by default within the nginx `default.conf`
  - Should you wish to make emergency edits, allow the idp/master endpoint in nginx before proceeding
  - credentials (user/pass) for admin account of that master realm is admin/admin

* port `49155` is only a random port I used in the making of this proj, assigned just in case the physical machines own port 80 is already in use.
* Try and test retrieval of passwords via ldap injection, by right it shouldn't be possible because it isn't configured to do so but I have no clue to what extent someone can craft a malicious input for ldap filtering.
* Lmk if the hints feel unrelated or too vague.
