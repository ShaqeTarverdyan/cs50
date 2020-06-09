#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{

    if (argc != 2)
    {
        fprintf(stderr, "Please enter file to open.\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    //check if inputFile is not null
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 1;
    }
    FILE *img = NULL;
    int counter = 0;
    unsigned char buffer[512];
    char filename[8];
    bool isJpg = false;
    while (fread(buffer, 512, 1, file) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (isJpg == true)
            {
                fclose(img);
            }
            else
            {
                isJpg = true;
            }
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            counter++;
        }
        if (isJpg == true)
        {
            fwrite(&buffer, 512, 1, img);
        }
    }
    fclose(file);
    fclose(img);
    return 0;
}