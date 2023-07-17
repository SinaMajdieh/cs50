#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n = -1;
    while (!(n >= 1 && n <= 8))
    {
        printf("Height: ");
        scanf("%d", &n);
    }
    int space = n - 1, brick = 1;
    for (int i = 0 ; i < n; i++)
    {
        for (int j = 0; j < space; j++)
        {
            printf(" ");
        }
        for (int j = 0; j < brick; j++)
        {
            printf("#");
        }
        printf("  ");
        for (int j = 0; j < brick; j++)
        {
            printf("#");
        }
        printf("\n");
        space -= 1;
        brick += 1;
    }
}
