#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //prompting user for input
    string text = get_string("Text: ");
    //counting letters, words, sentences
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    //calculating oleman-Liau index
    float L = (letters / (float)words) * 100;
    float S = (sentences / (float)words) * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    //printing the result
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %d\n", index);
    }
}
//counting letters
int count_letters(string text)
{
    int c = 0;
    for (int i = 0 ; i < strlen(text); i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            c++;
        }
    }
    return c;
}
//counting words
int count_words(string text)
{
    int c = 0;
    for (int i = 0 ; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            c++;
        }
    }
    return c + 1;
}
//counting sentences
int count_sentences(string text)
{
    int c = 0;
    for (int i = 0 ; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            c++;
        }
    }
    return c;
}
