#!/bin/bash
set -e

# Export default fallback environment variables if not supplied by CTFd container runner
export SECRET_KEY="${KEY:-default_secret_key}"
export LDAP_URI="${LDAP_URI:-ldap://127.0.0.1:389}"
export LDAP_BASE_DN="${LDAP_BASE_DN:-dc=NTU,dc=Sentinels}"
export LDAP_BIND_DN="${LDAP_BIND_DN:-cn=admin,dc=NTU,dc=Sentinels}"
export LDAP_BIND_PASSWORD="${LDAP_BIND_PASSWORD:-admin}"
export SP_ENTITY_ID="${SP_ENTITY_ID:-ctf-sp}"
export SP_ACS_URL="${SP_ACS_URL:-http://localhost/sso/acs}"
export IDP_SSO_URL="${IDP_SSO_URL:-http://localhost/idp/realms/master/protocol/saml}"
export IDP_CERT_PATH="${IDP_CERT_PATH:-/app/saml/idp_cert.crt.pem}"
export FLAG_ADMIN="${FLAG_ADMIN:-sentctf{Ld4p_1nj3C+_S4ML_S1gn4+ure3_Byp4ss3d}}"

export KC_BOOTSTRAP_ADMIN_USERNAME="${KC_BOOTSTRAP_ADMIN_USERNAME:-admin}"
export KC_BOOTSTRAP_ADMIN_PASSWORD="${KC_BOOTSTRAP_ADMIN_PASSWORD:-admin}"
export KC_HTTP_RELATIVE_PATH="/idp"
export KC_HOSTNAME="localhost"
export KC_PROXY_HEADERS="xforwarded"
export KC_HTTPS_CERTIFICATE_FILE="/etc/x509/https/keycloak.crt.pem"
export KC_HTTPS_CERTIFICATE_KEY_FILE="/etc/x509/https/keycloak.key.pem"

# 1. Start OpenLDAP Service
echo "[*] Starting OpenLDAP..."
service slapd start || slapd -h "ldap://127.0.0.1:389/" -d 0 &

# 2. Start Keycloak in Dev Mode
echo "[*] Starting Keycloak..."
/opt/keycloak/bin/kc.sh start-dev --import-realm &

# 3. Start Nginx Reverse Proxy
echo "[*] Starting Nginx..."
nginx

# Allow services a moment to initialize ports
sleep 5

# 4. Start Flask Application
echo "[*] Starting Flask Application..."
exec python /app/sp-flask/app.pys