#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // TODO #1
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav");
        return 1;
    }
    char *inputfilename = argv[1];
    char *outputfilename = argv[2];

    // Open input file for reading
    // TODO #2
    FILE *input = fopen(inputfilename, "r");
    if (input == NULL)
    {
        printf("Cant open %s.\n", inputfilename);
        return 1;
    }

    // Read header
    // TODO #3
    WAVHEADER wh;
    fread(&wh, sizeof(wh), 1, input);

    // Use check_format to ensure WAV format
    // TODO #4
    if (!check_format)
    {
        printf("Unsupported file.\n");
        fclose(input);
        return 1;
    }

    // Open output file for writing
    // TODO #5
    FILE *output = fopen(outputfilename, "w");
    if (output == NULL)
    {
        printf("Couldnt open %s.\n", outputfilename);
        fclose(input);
        return 1;
    }

    // Write header to file
    // TODO #6
    fwrite(&wh, sizeof(wh), 1, output);

    // Use get_block_size to calculate size of block
    // TODO #7
    int block_size = get_block_size(wh);

    // Write reversed audio to file
    // TODO #8
    BYTE buffer[block_size];
    fseek(input, 0, SEEK_END);

    long audio_size = ftell(input) - sizeof(WAVHEADER);
    int audio_block = (int) audio_size / block_size;

    for (int i = audio_block - 1; i >= 0; i--)
    {
        fseek(input, sizeof(WAVHEADER) + i * block_size, SEEK_SET);
        fread(&buffer, block_size, 1, input);
        fwrite(&buffer, block_size, 1, output);
    }

    fclose(input);
    fclose(output);
}

int check_format(WAVHEADER header)
{
    // TODO #4
    if (strcmp(header.format, "WAVE") == 0)
    {
        return 1;
    }
    return 0;
}

int get_block_size(WAVHEADER header)
{
    // TODO #7
    return header.numChannels * (header.bitsPerSample / 8);
}

