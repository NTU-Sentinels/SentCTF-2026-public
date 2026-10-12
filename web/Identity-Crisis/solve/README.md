# Solution

- Flag is in format of sentctf{A_B}
  - A is a flag found via ldap injection by logging in as a specific user.
  - B is a flag found via the completion of saml signature bypass to log into the admin account.
- Solution to A is done by realising ldap server was the means of authentication, then attempting to bypass the login by using wildcards to retrieve a specific user info:
  - Username = “_3_”
  - Password=”\*”
- Solution to B is done by using burp suite to observe the full login flow using the given credentials.
  - Users will eventually see after signing in through the idp page, that it redirects them before finally signing them in to the main page.
    - This redirection contains a SAML response encoded in base64.
    - The user is to parse this response and identify the fields needed to add and edit in order to log in as another user, e.g. Admin.
  - This SAML response consists of long XML detailing the credentials and signature of the user singing in.
  - To achieve the signature bypass, the user is to copy the entire assertion section of the saml response and paste it in front of the existing one
  - Removing the entire <dsig:Signature> section from the copied assertion
  - Changing the relevant fields (NameID, employeeType) to the desired options (admin, admin)
    - The user just needs to change these two fields to succeed, I got lazy to actively verify everything else.
    - The user will be able to acquire the relevant details by using LDAP injection to find the admin account details.
  - Finally, change the Assertion ID of the copied asserted section to a different UUIDv4 value, this can be any UUIDv4 value, I went online to get a random generated value
  - Inject your edited SAML Response into the SAML response body and submit it. If all goes well, you will log in as the admin, despite only logging in with the credentials given at the start of the challenge.
  - This gives us the final flag put together as: sentctf{Ld4p_1nj3C+\_S4ML_S1gn4+ure3_Byp4ss3d}

# Hints

- (LDAP) Is there a way to retrieve a specific username from an ldap server?
- (LDAP) What goes into an ldap filter?
- (SAML) Burp suite can observe traffic, observe the SAML Auth flow.
- (SAML) How does SAML verify and receive user credentials before authenticating them?
