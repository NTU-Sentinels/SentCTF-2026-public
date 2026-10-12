#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void sentctf() {
    puts("Successfully exploited! Now, run it on the live server to get the flag! ~ Refer to the cheatsheet for more information.");
}

void vuln() {
    char buf[32];
    puts("Welcome to SENTCTF! Give me your input:");
    read(0, buf, 64); // Reads 64 bytes into a 32-byte buffer
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    vuln();
    return 0;
}
