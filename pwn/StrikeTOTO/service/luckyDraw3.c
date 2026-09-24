#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define PRIZE_NUMBER 67

void win()
{
    printf("\n========================================================\n");
    printf("========================================================\n");
    printf(" DING DING DINGGGGGGGGGG\n");
    printf("\nCongratulations!! YOU ARE A WINNER!!\n");
    printf("Here is your prize: ");

    FILE *fp = fopen("flag.txt","r");

    if(!fp)
    {
        printf("Uh oh file not found!\n");
        exit(1);
    }

    char flag[100];
    fgets(flag,sizeof(flag),fp);
    printf("%s\n", flag);

    fclose(fp);

}

void banner()
{
    printf("========================================================\n");
    printf("========================================================\n");
    printf("              Greetings GAMBLERS!\n");
    printf("       Welcome to SentCTF Lucky Draw 2026!\n");
    printf("========================================================\n");
    printf("=========================================================\n");
    
    printf("\nTry your luck NOW!!!\n");

    printf("Choice: \n");
    printf("1. Get your lucky number\n");
    printf("2. Exit\n");

}

int generateLuckyNumber()
{
    printf("\nGenerating your lucky number.....\n");

     for(int i = 0; i < 5; i++)
    {
        printf(".");
        fflush(stdout);
        usleep(500000);
    }

    printf("\n");

    int luckyNumber = rand() % 100;
    return luckyNumber;

}

void announceLuckyNumber(int luckyNumber)
{
    printf("\nYour lucky number is");

    for(int i = 0; i < 3; i++)
    {
        printf(".");
        fflush(stdout);
        usleep(700000);
    }

    printf("%d\n", luckyNumber);

    if(luckyNumber == PRIZE_NUMBER)
    {
        win();
    }
    else
    {
        printf("\nSorry :(\n");
        printf("better luck next time!");
    }
}

int main(){

    srand(time(NULL));

    char name[32];
    int luckyNumber;

    banner();

    int choice;
    scanf("%d",&choice);
    getchar();

    if(choice == 2)
    {
        printf("Exiting the program...\n");
        exit(0);
    }
    else if(choice != 1)
    {
        printf("Invalid choice. Exiting the program...\n");
        exit(0);
    }
    else
    {
        luckyNumber = generateLuckyNumber();
        
        printf("\nEnter your name: ");
	    fflush(stdout);
        read(0, name, 100);

        printf("\nBest of luck!\n");
    }

    announceLuckyNumber(luckyNumber);


    return 0;
}
