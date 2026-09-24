#ifndef SSDP_H
#define SSDP_H

#include <sys/types.h>
#include <netinet/in.h>

void *ssdp_server_start(void *arg);

void handle_msearch(
    int sockfd,
    const char *buffer,
    ssize_t bytes_received,
    struct sockaddr_in *client_addr
);

void send_msearch_response(
    int sockfd,
    struct sockaddr_in *client_addr
);

#endif