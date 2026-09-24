#include <stdio.h>
#include <pthread.h>
#include "ssdp.h"
#include "http.h"

#define UPNP_SERVER_PORT 5000

int main(void)
{

    setbuf(stdout, NULL);
    printf("[MAIN] Starting upnpd\n");

    pthread_t ssdp_thread;

    if (pthread_create(
            &ssdp_thread,
            NULL,
            ssdp_server_start,
            NULL) != 0)
    {
        return 1;
    }

    http_server_start(UPNP_SERVER_PORT);

    pthread_join(ssdp_thread, NULL);

    return 0;
}