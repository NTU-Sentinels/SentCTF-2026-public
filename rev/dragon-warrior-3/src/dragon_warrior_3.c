#include <stdio.h>
#include <string.h>
#include <stdint.h>

static void __attribute__((used)) forged_scroll(void) {
    const unsigned char fake[] = { 18, 36, 9, 75, 91, 46, 110, 17 };
    volatile unsigned char sink = 0;
    size_t i;
    for (i = 0; i < sizeof(fake); i++) sink ^= fake[i];
    (void)sink;
}

static int real_trial(const char *input) {
    const uint8_t order[16] = { 5, 2, 14, 1, 9, 7, 0, 12, 4, 15, 6, 3, 10, 8, 13, 11 };
    const uint8_t target[16] = { 104, 92, 124, 72, 116, 115, 83, 140, 100, 134, 122, 89, 112, 113, 116, 102 };
    uint8_t transformed[16];
    size_t i;

    if (strlen(input) != 16) return 0;
    for (i = 0; i < 16; i++) {
        transformed[i] = (uint8_t)(((uint8_t)input[i] ^ 0x37) + i * 3);
    }
    for (i = 0; i < 16; i++) {
        if (transformed[order[i]] != target[i]) return 0;
    }
    if ((uint8_t)input[0] + (uint8_t)input[15] != 210) return 0;
    if (((uint8_t)input[3] ^ (uint8_t)input[10]) != 2) return 0;
    if ((int)(uint8_t)input[6] - (int)(uint8_t)input[2] != -2) return 0;
    return 1;
}

static void reveal_scroll(void) {
    const unsigned char scroll[] = {
        24, 14, 5, 31, 8, 31, 13, 16, 90, 5, 5, 88, 25, 52, 27,
        88, 95, 8, 88, 52, 95, 8, 3, 90, 88, 29, 88, 15, 22
    };
    size_t i;
    for (i = 0; i < sizeof(scroll); i++) putchar(scroll[i] ^ 0x6b);
    putchar('\n');
}

int main(void) {
    char input[80];
    puts("THE FINAL DRAGON WARRIOR TRIAL");
    fputs("Enter Dragon Scroll phrase: ", stdout);
    if (fgets(input, sizeof(input), stdin) == NULL) return 1;
    input[strcspn(input, "\n")] = '\0';

    if (!real_trial(input)) {
        puts("You have not found inner peace.");
        return 0;
    }

    puts("The Dragon Scroll opens.");
    reveal_scroll();
    return 0;
}
