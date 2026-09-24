#include <stdio.h>
#include <string.h>
#include <sys/socket.h>

#include "http.h" 

#define FLAG "sentctf{UPnP_$h0uld_be_disabled}"

typedef struct
{
    char status[64];
    int maintenance_mode;
    char gateway[64];
} DeviceState;

static DeviceState g_state =
{
    .status = "RUNNING",
    .maintenance_mode = 0,
    .gateway = "8.8.8.8"
};

int extract_xml_tag(
    const char *xml,
    const char *tag,
    char *output,
    size_t output_size)
{
    char open_tag[64];
    char close_tag[64];

    const char *start;
    const char *end;

    snprintf(open_tag,
             sizeof(open_tag),
             "<%s>",
             tag);

    snprintf(close_tag,
             sizeof(close_tag),
             "</%s>",
             tag);

    start = strstr(xml, open_tag);

    if (start == NULL)
        return -1;

    start += strlen(open_tag);

    end = strstr(start, close_tag);

    if (end == NULL)
        return -1;

    size_t len = end - start;

    if (len >= output_size)
        len = output_size - 1;

    memcpy(output, start, len);
    output[len] = '\0';

    return 0;
}

void send_soap_response(
    int client_fd,
    const char *body)
{
    char soap[4096];
    char response[8192];

    snprintf(
        soap,
        sizeof(soap),

        "<?xml version=\"1.0\"?>\n"
        "<s:Envelope\n"
        "    xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\"\n"
        "    s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">\n"
        "\n"
        "    <s:Body>\n"
        "%s\n"
        "    </s:Body>\n"
        "\n"
        "</s:Envelope>\n",

        body);

    snprintf(
        response,
        sizeof(response),

        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/xml; charset=\"utf-8\"\r\n"
        "Content-Length: %zu\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s",

        strlen(soap),
        soap);

    send(
        client_fd,
        response,
        strlen(response),
        0);
}


void action_get_status(int client_fd)
{
    char response[512];

    snprintf(
        response,
        sizeof(response),

        "        <u:GetStatusResponse\n"
        "            xmlns:u=\"urn:schemas-upnp-org:service:DeviceConfig:1\">\n"
        "            <Status>%s</Status>\n"
        "        </u:GetStatusResponse>",

        g_state.status);

    send_soap_response(
        client_fd,
        response);
}


void action_run_diagnostic(
    int client_fd,
    const char *soap_body)
{
    char target[128] = {0};
    char result[128];
    char response[512];

    if (extract_xml_tag(
            soap_body,
            "Target",
            target,
            sizeof(target)) != 0)
    {
        send_400_error(client_fd, "Missing Target");
        return;
    }

    // check allowed values
    if (strcmp(target, "ping") != 0 &&
        strcmp(target, "dns") != 0)
    {
        send_400_error(
            client_fd,
            "DiagnosticType must be either 'ping' or 'dns'");
        return;
    }

    snprintf(
        result,
        sizeof(result),
        "Diagnostics completed for %s",
        target);

    snprintf(
        response,
        sizeof(response),

        "        <u:Result\n"
        "            xmlns:u=\"urn:schemas-upnp-org:service:DeviceConfig:1\">\n"
        "            <Result>%s</Result>\n"
        "        </u:Result>",

        result);

    send_soap_response(
        client_fd,
        response);
}

void action_set_maintenance_mode(
    int client_fd,
    const char *soap_body)
{
    char enabled[16] = {0};
    char response[512];

    if (extract_xml_tag(
            soap_body,
            "Enabled",
            enabled,
            sizeof(enabled)) != 0)
    {
        send_400_error(client_fd, "Missing Enabled");
        return;
    }

    // check for boolean value
    if (strcmp(enabled, "true") == 0)
    {
        g_state.maintenance_mode = 1;
    }
    else if (strcmp(enabled, "false") == 0)
    {
        g_state.maintenance_mode = 0;
    }
    else
    {
        send_400_error(
            client_fd,
            "Enabled must be either 'true' or 'false'");
        return;
    }

    snprintf(
        response,
        sizeof(response),

        "        <u:SetMaintenanceModeResponse\n"
        "            xmlns:u=\"urn:schemas-upnp-org:service:DeviceConfig:1\">\n"
        "            <Enabled>%s</Enabled>\n"
        "        </u:SetMaintenanceModeResponse>",

        g_state.maintenance_mode ? "true" : "false");

    send_soap_response(
        client_fd,
        response);
}


// * undocumented SOAP endpoint (not included in deviceconfig.xml)
void action_set_sentinels_gateway(
    int client_fd,
    const char *soap_body)
{
    char gateway[64] = {0};
    char result[128];
    char response[512];

    if (extract_xml_tag(
            soap_body,
            "Gateway",
            gateway,
            sizeof(gateway)) != 0)
    {
        send_400_error(client_fd, "Missing Gateway");
        return;
    }

    if (strcmp(gateway, "1.1.1.1") != 0 &&
        strcmp(gateway, "8.8.8.8") != 0 &&
        strcmp(gateway, "SentCTF") != 0)
    {
        send_400_error(
            client_fd,
            "Invalid gateway value!");
        return;
    }

    strncpy(
        g_state.gateway,
        gateway,
        sizeof(g_state.gateway) - 1);

    g_state.gateway[
        sizeof(g_state.gateway) - 1] = '\0';

    if (strcmp(gateway, "SentCTF") == 0)
    {
        snprintf(
            result,
            sizeof(result),
            FLAG);
    }
    else
    {
        snprintf(
            result,
            sizeof(result),
            "Gateway successfully set to %s",
            g_state.gateway);
    }

    snprintf(
        response,
        sizeof(response),

        "        <u:SetSentinelsGatewayResponse\n"
        "            xmlns:u=\"urn:schemas-upnp-org:service:DeviceConfig:1\">\n"
        "            <Result>%s</Result>\n"
        "        </u:SetSentinelsGatewayResponse>",

        result);

    send_soap_response(
        client_fd,
        response);
}

void dispatch_soap_action(
    int client_fd,
    const char *soap_action,
    const char *body)
{

    if (strcmp(soap_action, "GetStatus") == 0)
    {
        action_get_status(client_fd);
    }
    else if (strcmp(soap_action, "RunDiagnostic") == 0)
    {
        action_run_diagnostic(client_fd, body);
    }
    else if (strcmp(soap_action, "SetMaintenanceMode") == 0)
    {
        action_set_maintenance_mode(client_fd, body);
    }
    else if (strcmp(soap_action, "SetSentinelsGateway") == 0)
    {
        action_set_sentinels_gateway(client_fd, body);
    }
    else
    {
        send_400_error(client_fd, "Unknown SOAP action");
    }
}