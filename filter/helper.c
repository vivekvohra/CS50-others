#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int rgbt =
                round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = rgbt;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}
// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create temp array as we require original values
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++) // went to a pixel
        {
            // Initialise values for each i,j pixel
            float sum_red;
            float sum_blue;
            float sum_green;
            int counter; // to count no. of surr. pixels
            sum_red = sum_blue = sum_green = counter = 0;

            for (int k = i - 1; k <= i + 1; k++) // for surr. pixels
            {
                for (int l = j - 1; l <= j + 1; l++)
                { // cases of surr. ipixel

                    if (k >= 0 && l >= 0 && k < height && l < width)
                    { // if that ipixel is in img.

                        sum_red += temp[k][l].rgbtRed;
                        sum_blue += temp[k][l].rgbtBlue;
                        sum_green += temp[k][l].rgbtGreen;
                        counter++;
                    }
                }
            }
            // take average
            image[i][j].rgbtRed = round(sum_red / counter);
            image[i][j].rgbtGreen = round(sum_green / counter);
            image[i][j].rgbtBlue = round(sum_blue / counter);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Create temp array as we require original values
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }
    // initialize the sobel opreator array
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++) // went to a pixel
        {
            // Initialise values for each i,j pixel
            float Gx_red;
            float Gx_blue;
            float Gx_green;
            float Gy_red;
            float Gy_blue;
            float Gy_green;
            Gx_red = Gx_blue = Gx_green = Gy_red = Gy_blue = Gy_green = 0;

            for (int k = i - 1; k <= i + 1; k++) // for surr. pixels
            {
                for (int l = j - 1; l <= j + 1; l++)
                { // cases of surr. ipixel

                    if (k >= 0 && l >= 0 && k < height && l < width)
                    { // if that ipixel is outside the border

                        Gx_red += temp[k][l].rgbtRed * Gx[k - i + 1][l - j + 1];
                        Gx_green += temp[k][l].rgbtGreen * Gx[k - i + 1][l - j + 1];
                        Gx_blue += temp[k][l].rgbtBlue * Gx[k - i + 1][l - j + 1];
                        Gy_red += temp[k][l].rgbtRed * Gy[k - i + 1][l - j + 1];
                        Gy_green += temp[k][l].rgbtGreen * Gy[k - i + 1][l - j + 1];
                        Gy_blue += temp[k][l].rgbtBlue * Gy[k - i + 1][l - j + 1];
                    }
                }
            }

            // Combine Gx and Gy into new pixel value
            int red = round(sqrt(Gx_red * Gx_red + Gy_red * Gy_red));
            int green = round(sqrt(Gx_green * Gx_green + Gy_green * Gy_green));
            int blue = round(sqrt(Gx_blue * Gx_blue + Gy_blue * Gy_blue));
            // if value is above limit; assg. it maxm possible
            if (red > 255)
            {
                red = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            // assign value to new pixel
            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }

    return;
}
