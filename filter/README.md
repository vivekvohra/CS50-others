# filter
In this problem, we have to code the following filter:

- **Grayscale** function takes an image and turns it into a black-and-white version of the same image.

- **Reflect** function takes an image and reflects it horizontally.

- **Blur** function takes an image and turns it into a box-blurred version of the same image.

- **Edge** function takes an image and highlights the edges between objects, according to the Sobel operator.


<h3>For detailed explanation click on link below :</h3>

[PSet: Filter(more)](//dev.to/vivekvohra/cs50-pset-filtermore-helperc-4h21 "PSet: Filter(more)")

### Grayscale:
This function takes an image and converts it into a black-and-white version of the same image. This is done by taking an average of the **RGB**  values of each pixel and setting them all equal to the average.

### Reflect:
This function flips an image about the vertical axis, which returns a mirror image. 

## Blur:

The purpose here is to return a blurred version of the input image. We do this by implementing the **“box blur,”** which works by taking each pixel and, for each color value, giving it a new value by averaging the color values of neighboring pixels.

## Edge:

We can achieve this effect by applying the Sobel operator to the image.
<h3>Below is the results of the function:</h3>
<img align="center" src = "https://media.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fw3mrq2kk7kno6oxisioo.png">

For detailed explanation click on link below :

[PSet: Filter(more)](//dev.to/vivekvohra/cs50-pset-filtermore-helperc-4h21 "PSet: Filter(more)")
