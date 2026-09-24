#ifndef HTTP_H
#define HTTP_H

typedef struct
{
    char method[8];
    char path[256];
    char soap_action[128];
    int content_length;
    char body[4096];

} HttpRequest;

#endif

void print_http_request(const HttpRequest *request);

void handle_client(int client_fd);

int http_server_start(int port);

int parse_http_request(
    char *buffer, 
    HttpRequest *request
);

void handle_get(
    int client_fd,
    HttpRequest *request
);

void handle_post(
    int client_fd,
    HttpRequest *request
);


void send_404_error(int client_fd);
void send_400_error(int client_fd, const char *body);
