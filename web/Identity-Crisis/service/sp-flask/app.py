import base64
from datetime import datetime, timezone
import os
import traceback
import urllib.parse
import uuid
import zlib
from functools import wraps
from flask import Flask, request, session, redirect, url_for, render_template, abort
from ldap3 import Server, Connection, ALL, SUBTREE
from lxml import etree
from signxml import XMLVerifier
import secrets
import session_tracking

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

samlsessions = {}
ldapsessions = {}

LDAP_URI = os.getenv("LDAP_URI", "ldap://ldap:389")
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN", "dc=corp,dc=local")
LDAP_BIND_DN = os.getenv("LDAP_BIND_DN", "cn=admin,dc=corp,dc=local")
LDAP_BIND_PASSWORD = os.getenv("LDAP_BIND_PASSWORD", "admin")

SP_ENTITY_ID = os.getenv("SP_ENTITY_ID", "ctf-sp")
SP_ACS_URL = os.getenv("SP_ACS_URL", "http://localhost:49155/saml/acs")
IDP_SSO_URL = os.getenv("IDP_SSO_URL", "http://localhost/idp/realms/ntu-sentinels/protocol/saml")
IDP_CERT_PATH = os.getenv("IDP_CERT_PATH", "/app/saml/idp_cert.pem")

FLAG_ADMIN = os.getenv("FLAG_ADMIN", "flag{admin_saml_wrap_pwn}")
ENABLE_MULTIFLAG = os.getenv("ENABLE_MULTIFLAG", "true").lower() == "true"

#========================================Session type Decorators======================================================
def require_saml(view):
    @wraps(view)
    def wrapper(*args, **kwargs):

        if session.get("auth_source") != "saml":
            return redirect(url_for("sso_login"))

        sid = session.get("saml_session_id")

        if sid not in samlsessions:
            session.clear()
            return redirect(url_for("sso_login"))

        return view(*args, **kwargs)

    return wrapper

def require_ldap(view):
    @wraps(view)
    def wrapper(*args, **kwargs):

        if session.get("auth_source") != "ldap":
            return redirect(url_for("login"))

        sid = session.get("ldap_session_id")

        if sid not in ldapsessions:
            session.clear()
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapper

#==============================================================================================

#=======================================SAML Helper Function======================================================
# This function is used to perform SAML logout by sending a SAML Logout Request to the IdP (Keycloak).
def perform_saml_logout():
    if "user" in session and session.get("auth_source") == "saml" and session.get("saml_session_id") in samlsessions:
        samlsession = samlsessions[session.get("saml_session_id")]
        name_id = samlsession.name_id
        session_index = samlsession.session_index
    else:
        return

    request_id = "_" + str(uuid.uuid4())
    issue_instant = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    saml_logout_request = f"""<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ID="{request_id}" Version="2.0" IssueInstant="{issue_instant}" Destination="{IDP_SSO_URL}">
        <saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">{SP_ENTITY_ID}</saml:Issuer>
        <saml:NameID xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">{name_id}</saml:NameID>
        <samlp:SessionIndex>{session_index}</samlp:SessionIndex>
        </samlp:LogoutRequest>"""
    
    # Compress and encode the Logout Request
    compressor = zlib.compressobj(wbits=-15)
    compressed = compressor.compress(saml_logout_request.encode()) + compressor.flush()
    saml_logout_request_b64 = base64.b64encode(compressed).decode()

    # Redirect to IdP for logout
    params = {
        "SAMLRequest": saml_logout_request_b64,
        "RelayState": "ntu-sentinels"
    }
    samlsession.clear()
    session.clear()
    return redirect(IDP_SSO_URL + "?" + urllib.parse.urlencode(params))

# Function to clean strings by removing unwanted characters
def clean_saml_value(value):
    if isinstance(value, (list, tuple)):
        return value[0] if value else ""
    return value or ""

#========================================Session Clearing======================================
def clear_ldap_session():
    sid = session.get("ldap_session_id")

    if session.get("auth_source") == "ldap":
        ldapsessions.pop(sid, None)

    session.pop("ldap_session_id", None)
    session.pop("auth_source", None)

def clear_saml_session():
    sid = session.get("saml_session_id")

    if "user" in session and session.get("auth_source") == "saml" and session.get("saml_session_id") in samlsessions:
        # ensure all prerequisites for SAML logout are met before performing SAML logout
        perform_saml_logout()

    if session.get("auth_source") == "saml":
        samlsessions.pop(sid, None)

    session.pop("saml_session_id", None)
    session.pop("auth_source", None)
#==============================================================================================


# ========================================Vuln related functions======================================================


def ldap_auth_vulnerable(username: str, password: str):
    """
    Intentionally vulnerable for CTF:
    LDAP injection due to string interpolation in filter.
    """
    server = Server(LDAP_URI, get_info=ALL)
    conn = Connection(server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True)

    # DELIBERATE VULN: this allows for LDAP injection if username or password are crafted maliciously.
    ldap_filter = f"(&(uid={username})(userPassword={password}))"

    conn.search(
        search_base=f"ou=People,{LDAP_BASE_DN}",
        search_filter=ldap_filter,
        search_scope=SUBTREE,
        attributes=["uid", "cn", "sn", "title", "employeeNumber", "mail", "employeeType"]
    )
    if conn.entries:
        e = conn.entries[0]
        return {
            "uid": str(e.uid) if "uid" in e else "",
            "cn": str(e.cn) if "cn" in e else "",
            "sn": str(e.sn) if "sn" in e else "",
            "title": str(e.title) if "title" in e else "",
            "employeeNumber": str(e.employeeNumber) if "employeeNumber" in e else "",
            "mail": str(e.mail) if "mail" in e else "",
            "employeeType": str(e.employeeType) if "employeeType" in e else "",
            "source": "ldap"
        }
    return None

# edit the Issue Instant to current time in deployment rather than a fixed time.
def build_authn_request():
        req_id = "_" + str(uuid.uuid4())
        xml = f"""<samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
        ID="{req_id}" Version="2.0" IssueInstant="{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
        Destination="{IDP_SSO_URL}"
        AssertionConsumerServiceURL="{SP_ACS_URL}">
            <saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">{SP_ENTITY_ID}</saml:Issuer>
        </samlp:AuthnRequest>"""
        compressor = zlib.compressobj(wbits=-15)
        compressed = compressor.compress(xml.encode()) + compressor.flush()
        return base64.b64encode(compressed).decode()

# ========================================LEGACY SITE APIs======================================================

@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    #force clear saml sessions
    clear_saml_session()

    if request.method == "GET":
        return render_template("legacy_login.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    ldapresponse = ldap_auth_vulnerable(username, password) 
    # contacts the LDAP server to auth user, includes vulnerability to LDAP injection
    if not ldapresponse:
        return "Invalid credentials", 401

    ldap_sid = secrets.token_urlsafe(32)
    
    # store ldap session: role, auth source and session id in browser session, 
    # user details will be in server side session class.

    uid = ldapresponse["uid"]
    cn = username = ldapresponse["cn"]
    sn = ldapresponse["sn"]
    title = ldapresponse["title"]
    employeeNumber =ldapresponse["employeeNumber"]
    mail = ldapresponse["mail"]
    employeeType = ldapresponse["employeeType"].strip().lower()
    session["role"] = employeeType
    session["auth_source"] = "ldap"
    session["ldap_session_id"] = ldap_sid

    ldapsessions[ldap_sid] = session_tracking.LdapSession(role=employeeType, 
                                                          uid=uid, cn=cn, sn=sn, 
                                                          employeeNumber=employeeNumber, 
                                                          mail=mail, title=title)
    return redirect(url_for("profile") if employeeType != "admin" else url_for("admin"))

@app.route("/profile")
@require_ldap
def profile():
    if session["ldap_session_id"] is None or session["ldap_session_id"] not in ldapsessions:
        # if the session is not found in server side, redirect to login page
        # clear the session on the client side as well, 
        # mitigating attempts of changing session role to admin by modifying the cookie.
        session.clear()
        return redirect(url_for("login"))
    ldap_sid = session["ldap_session_id"]
    ldap_session = ldapsessions.get(ldap_sid)
    return render_template("legacy_profile.html",ldapsession=ldap_session, user=ldap_session.sessionuser)

@app.route("/admin")
@require_ldap
def admin():
    if session.get("role") != "admin":
        abort(403)

    if session["ldap_session_id"] is None or session["ldap_session_id"] not in ldapsessions:
        session.clear()
        return redirect(url_for("login"))

    ldap_sid = session["ldap_session_id"]
    ldap_session = ldapsessions.get(ldap_sid)
    return render_template("legacy_admin.html", ldapsession=ldap_session, flag=FLAG_ADMIN, user=ldap_session.sessionuser)

@app.route("/logout") 
# logout api call for the legacy sites, checks for LDAP session and clears it both in server and client side
# if the session is not found, returns error 500
# if error occurs during logout, returns error 500
def logout():
    try:
        # if user is logged in via ldap, clear ldap session by looking based on uid stored to remove the server side session.
        if session.get("auth_source") == "ldap" and session.get("ldap_session_id") in ldapsessions:
            ldapsessions[session.get("ldap_session_id")].clear()
            session.clear()
            return redirect(url_for("login"))
    except Exception as e:
        print(f"Error during logout: {str(e)}")
        return "Error during logout", 500
    return "Error during logout", 500

# ====================================================================================================

# ========================================NEW SITE APIs WITH SSO INVOLVED======================================================
@app.route("/sso/login")
def sso_login():
    # force clear ldap sessions
    clear_ldap_session()

    saml_request = build_authn_request()
    relay_state = "ntu-sentinels"
    params = {
        "SAMLRequest": saml_request,
        "RelayState": relay_state
    }
    return redirect(IDP_SSO_URL + "?" + urllib.parse.urlencode(params))

@app.route("/saml/acs", methods=["POST"])
def saml_acs():
    # force clear ldap sessions
    clear_ldap_session()

    saml_response_b64 = request.form.get("SAMLResponse")
    if not saml_response_b64:
        return "Missing SAMLResponse", 400

    xml_bytes = base64.b64decode(saml_response_b64)
    root = etree.fromstring(xml_bytes)
    with open(IDP_CERT_PATH, "rb") as f:
        cert_data = f.read()

    # Step 1: Verify a signature exists and validates against the IdP's certificate
    # (DELIBERATE CTF FLAW: does not bind verified assertion to consumed claims)
    try:
        XMLVerifier().verify(data=root, x509_cert=cert_data)
    except Exception as e:
        return f"{str(e)}", 403

    # Step 2: Parse assertion claims naively
    # DELIBERATE XSW FLAW: picks first Assertion, regardless of what was verified.
    ns = {
        "saml2": "urn:oasis:names:tc:SAML:2.0:assertion",
        "samlp": "urn:oasis:names:tc:SAML:2.0:protocol"
    }
    assertion = root.xpath(".//saml2:Assertion", namespaces=ns)[0]
    if assertion is None:
        return "No assertion", 400

    nameid = assertion.find(".//saml2:NameID", namespaces=ns)
    session_index = assertion.find(".//saml2:AuthnStatement", namespaces=ns).attrib["SessionIndex"]


    # acquire rest of user info from assertion attributes, if available, otherwise use defaults
    user_cn = assertion.find(".//saml2:Attribute[@Name='cn']/saml2:AttributeValue", namespaces=ns)
    user_sn = assertion.find(".//saml2:Attribute[@Name='sn']/saml2:AttributeValue", namespaces=ns)
    user_employeeNumber = assertion.find(".//saml2:Attribute[@Name='employeeNumber']/saml2:AttributeValue", namespaces=ns)
    user_mail = assertion.find(".//saml2:Attribute[@Name='mail']/saml2:AttributeValue", namespaces=ns)
    user_title = assertion.find(".//saml2:Attribute[@Name='title']/saml2:AttributeValue", namespaces=ns)
    user_employeeType = assertion.find(".//saml2:Attribute[@Name='employeeType']/saml2:AttributeValue", namespaces=ns)

    uid = clean_saml_value(nameid.text) if nameid is not None else "N/A"
    cn = clean_saml_value(user_cn.text) if user_cn is not None and user_cn.text else "N/A"
    sn = clean_saml_value(user_sn.text) if user_sn is not None and user_sn.text else "N/A"
    employeeNumber = clean_saml_value(user_employeeNumber.text) if user_employeeNumber is not None and user_employeeNumber.text else "N/A"
    title = clean_saml_value(user_title.text) if user_title is not None and user_title.text else "N/A"
    mail = user_mail.text.strip() if user_mail is not None and user_mail.text else "N/A"
    employeeType = user_employeeType.text.lower().strip() if user_employeeType is not None and user_employeeType.text else "N/A"

    session["role"] = employeeType
    session["auth_source"] = "saml"
    saml_sid = secrets.token_urlsafe(32)
    session["saml_session_id"] = saml_sid
    
    # Store the SAML session information in the server-side session class
    samlsessions[saml_sid] = session_tracking.SamlSession(role=employeeType, session_index=session_index,
                                                          name_id=nameid.text if nameid is not None else "N/A", 
                                                          uid=uid, cn=cn, sn=sn, 
                                                          employeeNumber=employeeNumber, 
                                                          mail=mail, title=title)
    return redirect(url_for("sso_admin" if employeeType == "admin" else "sso_profile"))

#sso related endpoints
@app.route("/sso/profile")
@require_saml
def sso_profile():
    # Check if the user is logged in via SAML and has a valid session
    if session.get("auth_source") != "saml" or session.get("saml_session_id") not in samlsessions or session.get("saml_session_id") is None:
        session.clear()
        return redirect(url_for("sso_login"))

    saml_sid = session["saml_session_id"]
    saml_session = samlsessions.get(saml_sid)
    
    return render_template("sso_profile.html", user=saml_session.sessionuser)

@app.route("/sso/admin")
@require_saml
def sso_admin():
    if session.get("role") != "admin":
        abort(403)

    # Check if the user is logged in via SAML and has a valid session
    if session.get("auth_source") != "saml" or session.get("saml_session_id") not in samlsessions or session.get("saml_session_id") is None:
        session.clear()
        return redirect(url_for("sso_login"))

    saml_sid = session["saml_session_id"]
    saml_session = samlsessions.get(saml_sid)

    return render_template("sso_admin.html", flag=FLAG_ADMIN, user=saml_session.sessionuser)

# Logouts through SSO 
# 1. when user clicks logout, SAML Logout request is sent to Keycloak, this request contains the name_id and session_index of the user. 
#    Keycloak will then terminate the session and send a SAML Logout Response back to the SP.
# 2. The SP will then clear the session on the browser and redirect the user to the login page.

@app.route('/saml/logout', methods=['GET']) # may need POST, test and adjust accordingly
@require_saml
def saml_logout():
    """Initiate SAML logout."""
    # samlLogoutRequest should contain unique ID, Issue instant, destination, issuer, name_id and session_index.
    # The SAML Logout Request is sent to the IdP (Keycloak) for processing
    if session.get("auth_source") == "saml" and session.get("saml_session_id") in samlsessions:
        samlsession = samlsessions[session.get("saml_session_id")]
        name_id = samlsession.name_id
        session_index = samlsession.session_index
    else:
        return "Error: No active SAML session found.", 404

    request_id = "_" + str(uuid.uuid4())
    issue_instant = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    saml_logout_request = f"""<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ID="{request_id}" Version="2.0" IssueInstant="{issue_instant}" Destination="{IDP_SSO_URL}">
        <saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">{SP_ENTITY_ID}</saml:Issuer>
        <saml:NameID xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">{name_id}</saml:NameID>
        <samlp:SessionIndex>{session_index}</samlp:SessionIndex>
        </samlp:LogoutRequest>"""
    
    # Compress and encode the Logout Request
    compressor = zlib.compressobj(wbits=-15)
    compressed = compressor.compress(saml_logout_request.encode()) + compressor.flush()
    saml_logout_request_b64 = base64.b64encode(compressed).decode()

    # Redirect to IdP for logout
    params = {
        "SAMLRequest": saml_logout_request_b64,
        "RelayState": "ntu-sentinels"
    }
    samlsession.clear()
    session.clear()
    return redirect(IDP_SSO_URL + "?" + urllib.parse.urlencode(params))

@app.route('/saml/sls', methods=['GET']) # shouldn't need to indicate a POST method, as this is just called from the IdP after logout 
def saml_sls():
    """Single Logout Service - handle logout response."""
    # This api endpoint is reached from keycloak when user logs out using SLO.
    # Clear the session on the server side
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)