#include <stdio.h>
#include <string.h>

int check_dragon_warrior(const char *input) {
    if (strlen(input) != 11) return 0;
    return input[0] == 'i' && input[1] == 'n' && input[2] == 'n' &&
           input[3] == 'e' && input[4] == 'r' && input[5] == '_' &&
           input[6] == 'p' && input[7] == 'e' && input[8] == 'a' &&
           input[9] == 'c' && input[10] == 'e';
}

void reveal_dragon_scroll(void) {
    const unsigned char scroll[] = {
        41, 63, 52, 46, 57, 46, 60, 33, 46, 50, 105, 5, 62,
        40, 110, 61, 106, 52, 5, 41, 57, 40, 106, 54, 54, 39
    };
    size_t i;
    for (i = 0; i < sizeof(scroll); i++) putchar(scroll[i] ^ 0x5a);
    putchar('\n');
}

int main(void) {
    char input[64];
    puts("DRAGON WARRIOR TRAINING");
    puts("The Dragon Scroll is hidden somewhere within this program.");
    puts("Perhaps the warrior should inspect how this trial decides who is worthy.");
    fputs("Enter the secret phrase: ", stdout);

    if (fgets(input, sizeof(input), stdin) == NULL) return 1;
    input[strcspn(input, "\n")] = '\0';

    if (!check_dragon_warrior(input)) {
        puts("You are not the Dragon Warrior.");
        return 0;
    }

    puts("The Dragon Scroll opens.");
    reveal_dragon_scroll();
    return 0;
}
