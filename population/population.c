#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start_size = 0, end_size = -1;
    while (start_size < 9)
    {
        printf("Start size: ");
        scanf("%d", &start_size);
    }
    // TODO: Prompt for end size
    while (end_size < start_size)
    {
        printf("End size: ");
        scanf("%d", &end_size);
    }
    // TODO: Calculate number of years until we reach threshold
    int n = 0;
    while (start_size < end_size)
    {
        start_size += (start_size / 3) - (start_size / 4);
        n++;
    }
    // TODO: Print number of years
    printf("Years: %d\n", n);
}

