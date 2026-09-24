#include <stdio.h>
#include <string.h>

#include <unistd.h>

#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include "ssdp.h"

#define CTFD_REMOTE_URL "CTFD-URL"
#define SSDP_PORT 1900
#define BUFFER_SIZE 4096
#define HTTP_PORT 5000


void send_msearch_response(int client_fd, struct sockaddr_in *client_addr)
{
    char response[1024];

    snprintf(
        response,
        sizeof(response),

        "HTTP/1.1 200 OK\r\n"
        "CACHE-CONTROL: max-age=1800\r\n"
        "LOCATION: http://%s:%d/device.xml\r\n"
        "SERVER: Linux/5.10 UPnP/1.1 NTUSentinels/1.0\r\n"
        "ST: upnp:rootdevice\r\n"
        "USN: uuid:ntu-sentinels-gateway::upnp:rootdevice\r\n"
        "\r\n",

        CTFD_REMOTE_URL,
        HTTP_PORT
    );

    // Send directly over the established TCP connection
    send(client_fd, response, strlen(response), 0);

    printf(
        "[SSDP] Response sent to %s\n",
        inet_ntoa(client_addr->sin_addr)
    );
}

void handle_msearch(
    int client_fd,
    const char *buffer,
    ssize_t bytes_received,
    struct sockaddr_in *client_addr)
{
    (void)bytes_received;

    printf("[SSDP] Packet received:\n%s\n", buffer);

    if (strncmp(buffer, "M-SEARCH * HTTP/1.1", 19) != 0)
    {
        return;
    }

    if (strstr(buffer, "ssdp:discover") == NULL)
    {
        return;
    }

    printf("[SSDP] Valid M-SEARCH request received.\n");

    send_msearch_response(client_fd, client_addr);
}


void *ssdp_server_start(void *arg)
{
    int listen_fd, client_fd;
    int opt = 1;

    char buffer[BUFFER_SIZE];
    ssize_t bytes_received;

    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;
    socklen_t client_len;

    (void)arg;

    //----------------------------------------------------------
    // Create TCP socket
    //----------------------------------------------------------

    listen_fd = socket(
        AF_INET,     // IPv4
        SOCK_STREAM, // TCP
        0
    );

    if (listen_fd < 0)
    {
        perror("socket");
        return NULL;
    }

    // Allow quick reuse of the port upon restart
    if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0)
    {
        perror("setsockopt");
        close(listen_fd);
        return NULL;
    }

    //----------------------------------------------------------
    // Bind to TCP/1900
    //----------------------------------------------------------

    memset(&server_addr, 0, sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(SSDP_PORT);

    if (bind(
            listen_fd,
            (struct sockaddr *)&server_addr,
            sizeof(server_addr)) < 0)
    {
        perror("bind");
        close(listen_fd);
        return NULL;
    }

    //----------------------------------------------------------
    // Start listening for TCP connections
    //----------------------------------------------------------

    if (listen(listen_fd, 10) < 0)
    {
        perror("listen");
        close(listen_fd);
        return NULL;
    }

    printf("[SSDP] Listening on TCP/%d\n", SSDP_PORT);

    //----------------------------------------------------------
    // Main connection loop
    //----------------------------------------------------------

    while (1)
    {
        client_len = sizeof(client_addr);

        client_fd = accept(
            listen_fd,
            (struct sockaddr *)&client_addr,
            &client_len
        );

        if (client_fd < 0)
        {
            perror("accept");
            continue;
        }

        bytes_received = recv(
            client_fd,
            buffer,
            sizeof(buffer) - 1,
            0
        );

        if (bytes_received > 0)
        {
            buffer[bytes_received] = '\0';

            printf(
                "[SSDP] Received %ld bytes from %s\n",
                (long)bytes_received,
                inet_ntoa(client_addr.sin_addr)
            );

            handle_msearch(
                client_fd,
                buffer,
                bytes_received,
                &client_addr
            );
        }
        else if (bytes_received < 0)
        {
            perror("recv");
        }

        // Close the client connection after handling the request
        close(client_fd);
    }

    close(listen_fd);

    return NULL;
}