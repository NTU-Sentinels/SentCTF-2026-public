#include <stdio.h>
#include <string.h>

static int stage_a(const char *s) {
    return s[0] == 0x70 && s[1] == 0x30 && s[2] == 0x34;
}

static int stage_b(const char *s) {
    return (((unsigned char)s[3] ^ 0x20) == 0x4e) &&
           ((unsigned char)s[4] + 3 == 0x67) &&
           (((unsigned char)s[5] ^ 0x55) == 0x61);
}

static int stage_c(const char *s) {
    return ((unsigned char)s[6] - 5 == 0x1c) &&
           ((unsigned char)s[7] + 7 == 0x28);
}

static int warrior_check(const char *s) {
    return strlen(s) == 8 && stage_a(s) && stage_b(s) && stage_c(s);
}

static void show_scroll(void) {
    const unsigned char scroll[] = {
        78, 88, 83, 73, 94, 73, 91, 70, 83, 13, 98, 78, 14, 94, 79,
        14, 73, 98, 12, 83, 90, 79, 14, 89, 12, 14, 83, 73, 64
    };
    size_t i;
    for (i = 0; i < sizeof(scroll); i++) putchar(scroll[i] ^ 0x3d);
    putchar('\n');
}

int main(void) {
    char input[64];
    puts("JADE PALACE SECURITY");
    fputs("Enter warrior code: ", stdout);
    if (fgets(input, sizeof(input), stdin) == NULL) return 1;
    input[strcspn(input, "\n")] = '\0';

    if (!warrior_check(input)) {
        puts("The scroll remains sealed.");
        return 0;
    }

    puts("The Dragon Warrior has returned.");
    show_scroll();
    return 0;
}
