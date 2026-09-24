#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

#include <unistd.h>

#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include "http.h"
#include "dispatcher.h"

#define DEVICE_XML_PATH "/etc/upnp/device.xml"
#define DEVICE_CONFIG_XML_PATH "/etc/upnp/deviceconfig.xml"
#define SOAP_ACCEPTED_ENDPOINT "/upnp/control/deviceconfig"


void print_http_request(const HttpRequest *request)
{
    printf("\n========== HTTP Request ==========\n");
    printf("Method         : %s\n", request->method);
    printf("Path           : %s\n", request->path);
    printf("SOAPAction     : %s\n", request->soap_action);
    printf("Content-Length : %d\n", request->content_length);
    printf("Body:\n%s\n", request->body);
    printf("==================================\n\n");
}

void send_404_error(int client_fd)
{
    const char *response =
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Length: 0\r\n"
        "Connection: close\r\n"
        "\r\n";

    send(client_fd, response, strlen(response), 0);
}

void send_400_error(int client_fd, const char *body)
{
    char response[1024];

    if (body == NULL)
    {
        body = "";
    }

    snprintf(
        response,
        sizeof(response),
        "HTTP/1.1 400 Bad Request\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: %zu\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s",
        strlen(body),
        body);

    send(client_fd, response, strlen(response), 0);
}

int parse_http_request(char *buffer, HttpRequest *request)
{
    char *line;
    char *headers_end;
    char *body;

    memset(request, 0, sizeof(HttpRequest));

    /*
     * Locate the beginning of the HTTP body before strtok()
     * modifies the buffer.
     */
    headers_end = strstr(buffer, "\r\n\r\n");

    if (headers_end != NULL)
    {
        *headers_end = '\0';      /* Terminate header section */
        body = headers_end + 4;   /* Skip "\r\n\r\n" */

        strncpy(
            request->body,
            body,
            sizeof(request->body) - 1);

        request->body[sizeof(request->body) - 1] = '\0';
    }

    /*
     * Parse request line.
     */
    line = strtok(buffer, "\r\n");

    if (line == NULL)
        return -1;

    if (sscanf(
            line,
            "%7s %255s",
            request->method,
            request->path) != 2)
    {
        return -1;
    }

    /*
     * Parse HTTP headers.
     */
    while ((line = strtok(NULL, "\r\n")) != NULL)
    {
        if (strncmp(line, "SOAPAction:", 11) == 0)
        {
            const char *value = line + 11;

            while (*value == ' ')
                value++;

            strncpy(
                request->soap_action,
                value,
                sizeof(request->soap_action) - 1);

            request->soap_action[
                sizeof(request->soap_action) - 1] = '\0';

            /* Remove leading quote */
            if (request->soap_action[0] == '"')
            {
                memmove(
                    request->soap_action,
                    request->soap_action + 1,
                    strlen(request->soap_action));
            }

            /* Remove trailing quote */
            char *quote = strchr(request->soap_action, '"');

            if (quote != NULL)
                *quote = '\0';

            /* Keep only the action after '#' */
            char *action = strrchr(
                request->soap_action,
                '#');

            if (action != NULL)
            {
                memmove(
                    request->soap_action,
                    action + 1,
                    strlen(action));
            }
        }
        else if (strncmp(line, "Content-Length:", 15) == 0)
        {
            request->content_length = atoi(line + 15);
        }
    }

    return 0;
}


void handle_get(int client_fd, HttpRequest *request)
{
    const char *filepath = NULL;

    FILE *fp;
    long filesize;
    char *buffer;
    char header[256];
    size_t bytes_read;

    printf("%s", request->path);

    if (strcmp(request->path, "/device.xml") == 0)
    {
        filepath = DEVICE_XML_PATH;
    }
    else if (strcmp(request->path, "/deviceconfig.xml") == 0)
    {
        filepath = DEVICE_CONFIG_XML_PATH;
    }
    else
    {
        send_404_error(client_fd);
        return;
    }

    fp = fopen(filepath, "rb");

    if (fp == NULL)
    {
        perror("fopen");
        send_404_error(client_fd);
        return;
    }

    fseek(fp, 0, SEEK_END);
    filesize = ftell(fp);
    rewind(fp);


    buffer = malloc(filesize);

    if (buffer == NULL)
    {
        fclose(fp);
        return;
    }


    bytes_read = fread(buffer, 1, filesize, fp);

    fclose(fp);

    if ((long)bytes_read != filesize)
    {
        free(buffer);
        return;
    }


    snprintf(
        header,
        sizeof(header),
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/xml\r\n"
        "Content-Length: %ld\r\n"
        "Connection: close\r\n"
        "\r\n",
        filesize);

    send(client_fd, header, strlen(header), 0);
    send(client_fd, buffer, filesize, 0);

    free(buffer);

    printf("[HTTP] Served %s\n", filepath);
}



void handle_post(int client_fd, HttpRequest *request)
{

    if (strcmp(request->path, SOAP_ACCEPTED_ENDPOINT) != 0)
    {
        send_404_error(client_fd);
        return;
    }

    if (request->soap_action[0] == '\0')
    {
        send_400_error(client_fd, "Missing SOAPAction");
        return;
    }


    if (request->content_length <= 0)
    {
        send_400_error(client_fd, "Missing SOAP body");
        return;
    }

    dispatch_soap_action(
        client_fd,
        request->soap_action,
        request->body);
}

void handle_client(int client_fd)
{
    HttpRequest request;

    char buffer[8192];

    int bytes_received;

    // clear the "request" struct
    memset(&request, 0, sizeof(request));

    // read the HTTP request from the client socket.
    bytes_received = recv(
        client_fd,            // returned by accept()
        buffer,               // buffer to store incoming request
        sizeof(buffer) - 1,   
        0                    
    );

    // recv() will return 0 or a negative value if the client disconnected or an error occurred
    if (bytes_received <= 0)
    {
        return;
    }

    // null-terminate buffer, so it will treated as a string
    buffer[bytes_received] = '\0';

    parse_http_request(buffer, &request);
    print_http_request(&request);

    //----------------------------------------------------------
    // GET request routes
    //----------------------------------------------------------

    if (strcmp(request.method, "GET") == 0)
    {
        handle_get(
            client_fd,
            &request
        );

        return;
    }

    //----------------------------------------------------------
    // POST request routes
    //----------------------------------------------------------

    if (strcmp(request.method, "POST") == 0)
    {
        handle_post(
            client_fd,
            &request
        );

        return;
    }


    send_404_error(client_fd);
}

int http_server_start(int port)
{

    int server_fd;
    int client_fd;

    // a struct containing the server's IP address and port
    struct sockaddr_in server_addr;

    server_fd = socket(
        AF_INET,      // IPv4
        SOCK_STREAM,  // TCP 
        0             
    );

    // zero-init "server_addr" variable
    memset(&server_addr, 0, sizeof(server_addr)  );

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY; // binds to 0.0.0.0
    server_addr.sin_port = htons(port);


    bind(
        server_fd,                        
        (struct sockaddr *)&server_addr,
        sizeof(server_addr)                 
    );


    listen(
        server_fd, 
        5  // max no. of pending connections in the accept queue
    );

    printf("[HTTP] Listening on TCP/%d\n", port);


    while (1)
    {
        client_fd = accept(
            server_fd, 
            NULL,      
            NULL        
        );
        
        handle_client(client_fd);

        close(client_fd);
    }

    close(server_fd);

    return 0;
}