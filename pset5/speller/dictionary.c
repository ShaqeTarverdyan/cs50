#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>

#include "dictionary.h"

struct node
{
    char word[LENGTH + 1];
    struct node *next;
};

typedef struct node *new_node;

new_node table[HASHTABLE_SIZE];

// Keeps track of the # of words in dictionary
unsigned long words = 0;

//taken from http://www.cse.yorku.ca/~oz/hash.html
unsigned long hash(const void *_str)
{
  const char *str = _str;
  unsigned long _hash = 5381;
  int c;

  while ((c = *str++))
  {
    _hash = ((_hash << 5) + _hash) + c; /* hash * 33 + c */
  }

  return _hash;

}

// Returns true if word is in dictionary else false
bool check(const char *word)
{

    char copy[strlen(word) + 1];
    strcpy(copy, word);

    //make lowerCase all letters
    for (int i = 0; i < strlen(word); i++)
    {
        copy[i] = tolower(word[i]);
    }

    unsigned long index = hash(copy) % HASHTABLE_SIZE;
    new_node cursor = table[index];

    while (cursor != NULL)
    {
        if (strcmp(cursor->word, copy) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }

    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        return false;
    }

    char buffer[LENGTH];
    while (fscanf(file, "%s", buffer) != EOF)
    {
        new_node node = malloc(sizeof(struct node));
        strcpy(node->word, buffer);
        node->next = NULL;

        unsigned long index = hash(buffer) % HASHTABLE_SIZE;
        if (table[index] != NULL)
        {
            node->next = table[index];
        }

        table[index] = node;

        words++;
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < HASHTABLE_SIZE; i++)
    {
        new_node cursor = table[i];

        while (cursor != NULL)
        {
            new_node tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }

    return true;
}

