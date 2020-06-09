#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int red;
    int green;
    int blue;
    float middle;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            red = image[i][j].rgbtRed;
            green = image[i][j].rgbtGreen;
            blue = image[i][j].rgbtBlue;
            middle = round((red + green + blue) / 3.000);
            image[i][j].rgbtRed = middle;
            image[i][j].rgbtGreen = middle;
            image[i][j].rgbtBlue = middle;

        }
    }
    return;
}

int limit(int RGB)
{
    if (RGB > 255)
    {
        RGB = 255;
    }
    return RGB;
}
// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int red;
    int green;
    int blue;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            red = limit(round(.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue));
            green = limit(round(.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue));
            blue = limit(round(.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue));
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int i, j;
    int temp[3];
    for (i = 0; i < height; i++)
    {
        for (j = 0; j < (width / 2); j++)
        {
            temp[0] = image[i][j].rgbtRed;
            temp[1] = image[i][j].rgbtGreen;
            temp[2] = image[i][j].rgbtBlue;

            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;

            image[i][width - j - 1].rgbtRed = temp[0];
            image[i][width - j - 1].rgbtGreen = temp[1];
            image[i][width - j - 1].rgbtBlue = temp[2];

        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int red;
    int green;
    int blue;
    float counter;
    RGBTRIPLE tempImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            red = image[i][j].rgbtRed;
            green = image[i][j].rgbtGreen;
            blue = image[i][j].rgbtBlue;
            counter = 1;

            if (j > 0)
            {
                red += image[i][j - 1].rgbtRed;
                green += image[i][j - 1].rgbtGreen;
                blue += image[i][j - 1].rgbtBlue;
                counter += 1;

                if (i > 0)
                {
                    red += image[i - 1][j - 1].rgbtRed;
                    green += image[i - 1][j - 1].rgbtGreen;
                    blue += image[i - 1][j - 1].rgbtBlue;
                    counter += 1;
                }
            }

            if (j < width - 1)
            {
                red += image[i][j + 1].rgbtRed;
                green += image[i][j + 1].rgbtGreen;
                blue += image[i][j + 1].rgbtBlue;
                counter += 1;

                if (i < height - 1)
                {
                    red += image[i + 1][j + 1].rgbtRed;
                    green += image[i + 1][j + 1].rgbtGreen;
                    blue += image[i + 1][j + 1].rgbtBlue;
                    counter += 1;
                }
            }

            if (i > 0)
            {
                red += image[i - 1][j].rgbtRed;
                green += image[i - 1][j].rgbtGreen;
                blue += image[i - 1][j].rgbtBlue;
                counter += 1;

                if (j < width - 1)
                {
                    red += image[i - 1][j + 1].rgbtRed;
                    green += image[i - 1][j + 1].rgbtGreen;
                    blue += image[i - 1][j + 1].rgbtBlue;
                    counter += 1;
                }


            }

            if (i < height - 1)
            {
                red += image[i + 1][j].rgbtRed;
                green += image[i + 1][j].rgbtGreen;
                blue += image[i + 1][j].rgbtBlue;
                counter += 1;

                if (j > 0)
                {
                    red += image[i + 1][j - 1].rgbtRed;
                    green += image[i + 1][j - 1].rgbtGreen;
                    blue += image[i + 1][j - 1].rgbtBlue;
                    counter += 1;
                }
            }
            tempImage[i][j].rgbtRed = round(red / counter);
            tempImage[i][j].rgbtGreen = round(green / counter);
            tempImage[i][j].rgbtBlue = round(blue / counter);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = tempImage[i][j];
        }
    }
    return;
}
