#include "helpers.h"
#include <math.h>
#include <stdio.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE new [height][width];
    //itterating over the height of the image
    for (int i = 0; i < height; i++)
    {
        //iterating over the width of the image to access each pixel
        for (int j = 0; j < width; j++)
        {
            //calcuating the average of the three RED, GREEN, BLUE values
            float grayscale_float = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            BYTE grayscale_byte = round(grayscale_float);
            //setting all RGB values to grayscale_byte
            new[i][j].rgbtRed = grayscale_byte;
            new[i][j].rgbtGreen = grayscale_byte;
            new[i][j].rgbtBlue = grayscale_byte;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = new[i][j];
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //hwidth is half of width
    int hwidth = width / 2;
    //iterating over the height of the image
    for (int i = 0 ; i < height; i++)
    {
        //shift to how much i need to shift the first pixel
        int shift = width - 1;
        for (int j = 0 ; j < hwidth; j++, shift -= 2)
        {
            //shifting the pixel through the width
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][j + shift];
            image[i][j + shift] = temp;
        //iterating over half of the width
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE new[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int wl = j, wr = j, hu = i, hd = i;
            if (j + 1 < width)
            {
                wr = j + 1;
            }
            if (j - 1 > -1)
            {
                wl = j - 1;
            }
            if (i - 1 > -1)
            {
                hu = i - 1;
            }
            if (i + 1 < height)
            {
                hd = i + 1;
            }
            int redaverage = 0;
            int greenaverage = 0;
            int blueaverage = 0;
            float count = 0;
            for (int k = hu; k <= hd; k++)
            {
                for (int l = wl; l <= wr; l++)
                {
                    redaverage += image[k][l].rgbtRed;
                    greenaverage += image[k][l].rgbtGreen;
                    blueaverage += image[k][l].rgbtBlue;
                    count++;
                }
            }
            float redavef = redaverage / count;
            float greenavef = greenaverage / count;
            float blueavef = blueaverage / count;
            
            redaverage = round(redavef);
            greenaverage = round(greenavef);
            blueaverage = round(blueavef);

            new[i][j].rgbtRed = redaverage;
            new[i][j].rgbtGreen = greenaverage;
            new[i][j].rgbtBlue = blueaverage;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = new[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE new[height][width];
    const int Gx[3][3] = 
    {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1},
    };
    const int Gy[3][3] = 
    {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1},
    };
    for (int i = 0; i < height; i++)
    {
        for (int j = 0 ; j < width; j++)
        {
            int wl = j - 1, wr = j + 1, hu = i - 1, hd = i + 1;
            int rax = 0, ray = 0;
            int gax = 0, gay = 0;
            int bax = 0, bay = 0;
            int kernel_i = 0;
            int kernel_j = 0;
            for (int k = hu; k <= hd; k++)
            {
                kernel_j = 0;
                for (int l = wl; l <= wr; l++)
                {
                    if ((l < 0 || l >= width) || (k < 0 || k >= height))
                    {
                        rax += 0 * Gx[kernel_i][kernel_j];
                        ray += 0 * Gy[kernel_i][kernel_j];
                        
                        gax += 0 * Gx[kernel_i][kernel_j];
                        gay += 0 * Gy[kernel_i][kernel_j];

                        bax += 0 * Gx[kernel_i][kernel_j];
                        bay += 0 * Gy[kernel_i][kernel_j];
                    }
                    else
                    {
                        rax += image[k][l].rgbtRed * Gx[kernel_i][kernel_j];
                        ray += image[k][l].rgbtRed * Gy[kernel_i][kernel_j];

                        gax += image[k][l].rgbtGreen * Gx[kernel_i][kernel_j];
                        gay += image[k][l].rgbtGreen * Gy[kernel_i][kernel_j];

                        bax += image[k][l].rgbtBlue * Gx[kernel_i][kernel_j];
                        bay += image[k][l].rgbtBlue * Gy[kernel_i][kernel_j];
                    }
                    kernel_j++;
                }
                kernel_i++;
            }
            float redavef = sqrt(pow(rax, 2) + pow(ray, 2));
            float greenavef = sqrt(pow(gax, 2) + pow(gay, 2));
            float blueavef = sqrt(pow(bax, 2) + pow(bay, 2));
            
            int redaverage = round(redavef);
            if (redaverage > 255)
            {
                redaverage = 255;
            }
            int greenaverage = round(greenavef);
            if (greenaverage > 255)
            {
                greenaverage = 255;
            }
            int blueaverage = round(blueavef);
            if (blueaverage > 255)
            {
                blueaverage = 255;
            }

            new[i][j].rgbtRed = redaverage;
            new[i][j].rgbtGreen = greenaverage;
            new[i][j].rgbtBlue = blueaverage;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = new[i][j];    
        }
    }
    return;
}
