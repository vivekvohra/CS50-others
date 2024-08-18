![recovered_image](recovered_image.png)

**GOAL**
- To write a program in C that can recover JPEG images from a forensic file.
- The program must accept one and only one command line argument, the name of the file the images will be recovered from.
- The program should output each of the JPEG images recovered as a separate file.
- The files generated should each be named ###.jpg, where ### is a three-digit decimal number, starting with 000 for the first image and counting up.
  
JPEGs have “signatures,” patterns of bytes that can distinguish them from other file formats. Specifically, the first three bytes of JPEGs are
0xff 0xd8 0xff

The fourth byte, meanwhile, is either 0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, or 0xef.

Digital cameras often initialize cards with a FAT file system whose “block size” is 512 bytes (B).

I wrote a program that iterates over a copy of my memory card, looking for JPEGs’ signatures. Each time I find a signature,
we can open a new file for writing and start filling that file with bytes from my memory card, closing that file only once we encounter another signature. 
Moreover, rather than read the memory card’s bytes one at a time, we can read 512 of them at a time into a buffer for efficiency’s sake. 
