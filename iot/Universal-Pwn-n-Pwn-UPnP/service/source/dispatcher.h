int extract_xml_tag(
    const char *xml,
    const char *tag,
    char *output,
    size_t output_size);

void send_soap_response(
    int client_fd,
    const char *body);

void action_get_status(int client_fd);

void action_run_diagnostic(
    int client_fd,
    const char *soap_body);

void action_set_maintenance_mode(
    int client_fd,
    const char *soap_body);

void action_set_sentinels_gateway(
    int client_fd,
    const char *soap_body);


void dispatch_soap_action(
    int client_fd,
    const char *soap_action,
    const char *body);