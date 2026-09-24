# Multi-stage build: Extract Keycloak distribution binaries
FROM quay.io/keycloak/keycloak:26.0 AS keycloak-stage

# Base runtime container targeting Python 3.12
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

WORKDIR /app

# Install system dependencies: OpenJDK 21 (Keycloak), Nginx, OpenLDAP, and compilation toolchains
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-21-jre-headless \
    nginx \
    slapd \
    ldap-utils \
    build-essential \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    xmlsec1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Keycloak from stage 1
COPY --from=keycloak-stage /opt/keycloak /opt/keycloak

# Install Python requirements for Flask application
COPY sp-flask/requirements.txt /app/sp-flask/requirements.txt
RUN pip install --no-cache-dir -r /app/sp-flask/requirements.txt

# Copy source application files
COPY sp-flask /app/sp-flask

# Configure Nginx reverse proxy
COPY nginx/default.conf /etc/nginx/sites-available/default
RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Stage Keycloak certificates and import realm
RUN mkdir -p /opt/keycloak/data/import /etc/x509/https /app/saml
COPY keycloak/realm-export.json /opt/keycloak/data/import/realm-export.json
COPY keycloak/https_keypair/idp_cert.crt.pem /etc/x509/https/keycloak.crt.pem
COPY keycloak/https_keypair/idp.key.pem /etc/x509/https/keycloak.key.pem
COPY sp-flask/idp_certs/idp_cert.crt.pem /app/saml/idp_cert.crt.pem

# Stage LDAP bootstrap files
RUN mkdir -p /container/service/slapd/assets/config/bootstrap/ldif/custom
COPY ldap/bootstrap/ /container/service/slapd/assets/config/bootstrap/ldif/custom/

# Setup orchestrator entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]