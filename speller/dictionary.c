// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 200000;

unsigned int word_count = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    char *lowered = malloc((LENGTH+1)*sizeof(char));
    strcpy(lowered, word);
    for (int i = 0, l = strlen(word); i < l; i++)
    {
        lowered[i] = tolower(lowered[i]);
    }
    unsigned int bucket = hash(word);

    node *cursor = table[bucket];

    while (cursor != NULL)
    {
        if (strcmp(cursor->word, lowered) == 0)
        {
            free(lowered);
            return true;
        }
        cursor = cursor -> next;
    }
    free(lowered);
    return false;
}

// Hashes word to a number
unsigned int hash_old(const char *word)
{
    // TODO: Improve this hash function
    unsigned int bucket = 0;
    for (int i = 0, l = strlen(word); i < l; i++)
    {
        bucket = bucket + (37 * (tolower(word[i])));
    }
    bucket %= N;
    return bucket;
}
unsigned int hash(const char *word)
{
    unsigned int bucket = 0;
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        bucket = (31 * bucket + tolower(word[i])) % N;
    }
    return bucket;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *dic = fopen(dictionary, "r");
    if (dic == NULL)
    {
        return false;
    }

    char word_buffer[LENGTH + 1];

    while (fscanf(dic, "%s", word_buffer) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }
        strcpy(new_node -> word, word_buffer);
        new_node -> next = NULL;
        int bucket_index = hash(word_buffer);

        if (table[bucket_index] == NULL)
        {
            table[bucket_index] = new_node;
        }
        else
        {
            new_node -> next = table[bucket_index];
            table[bucket_index] = new_node;
        }
        word_count++;
    }
    
    fclose(dic);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }
    // TODO
    return true;
}
