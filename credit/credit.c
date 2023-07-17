#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(void)
{
    long input = get_long("Number: ");
    int n = floor(log10(labs(input))) + 1;
    if (!(n == 16 || n == 15 || n == 13))
    {
        printf("INVALID\n");
        return 0;
    }
    int start = -1;
    long copy = input;
    int dig2 = 0, dig1 = 0;
    while (copy > 0)
    {
        if (copy < 1000 && start == -1)
        {
            if (copy > 100)
            {
                start = (copy - (copy % 10)) / 10;
            }
            else
            {
                start = copy;
            }
            //printf("hello\n");
        }
        int first = copy % 10;
        dig1 += first;
        copy = (copy - first) / 10;
        int second = (copy % 10);
        copy = (copy - second) / 10;
        second *= 2;
        if (second > 9)
        {
            int x = second % 10;
            second = (second - x) / 10;
            second += x;
        }
        dig2 += second;
        //printf("number= %ld\tfirst= %d\tsecond= %d\tdigit1= %d\tdigit2= %d\n",copy,first,second,dig1,dig2);
    }
    int luhn = dig1 + dig2;
    //printf("luhn= %d\tstart= %d\n", luhn,start);
    if (luhn % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    if ((start >= 51 && start <= 55) && n == 16)
    {
        printf("MASTERCARD\n");
    }
    else if ((start == 34 || start == 37) && n == 15)
    {
        printf("AMEX\n");
    }
    else if (((start - (start % 10)) / 10 == 4) && (n == 13 || n == 16))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

}
