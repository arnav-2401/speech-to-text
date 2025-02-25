#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>
#include <unistd.h>
#include <termios.h>

#define PCM_DEVICE "hw:0,0"
#define SAMPLE_RATE 44100
#define CHANNELS 1
#define FRAME_SIZE (CHANNELS * 2) // 16-bit audio = 2 bytes per frame
#define INITIAL_BUFFER_SIZE 4096  // Start small, but expand dynamically if needed

// Function to set terminal to non-blocking mode
void set_nonblocking_mode(int enable)
{
    struct termios tty;
    tcgetattr(STDIN_FILENO, &tty);
    if (enable)
    {
        tty.c_lflag &= ~(ICANON | ECHO); // Disable line buffering and echo
        tty.c_cc[VMIN] = 0;
        tty.c_cc[VTIME] = 0;
    }
    else
    {
        tty.c_lflag |= (ICANON | ECHO); // Restore normal input mode
    }
    tcsetattr(STDIN_FILENO, TCSANOW, &tty);
}

// Function to check for key press
int key_pressed()
{
    char ch;
    return (read(STDIN_FILENO, &ch, 1) == 1) ? ch : 0;
}

int main()
{
    snd_pcm_t *pcm_handle;
    snd_pcm_hw_params_t *params;
    int err;

    // Open the ALSA PCM device for recording
    if ((err = snd_pcm_open(&pcm_handle, PCM_DEVICE, SND_PCM_STREAM_CAPTURE, 0)) < 0)
    {
        fprintf(stderr, "Error opening PCM device %s: %s\n", PCM_DEVICE, snd_strerror(err));
        return 1;
    }

    // Allocate hardware parameters object
    snd_pcm_hw_params_alloca(&params);
    snd_pcm_hw_params_any(pcm_handle, params);

    // Set parameters: mono, 16-bit, 44.1 kHz
    snd_pcm_hw_params_set_access(pcm_handle, params, SND_PCM_ACCESS_RW_INTERLEAVED);
    snd_pcm_hw_params_set_format(pcm_handle, params, SND_PCM_FORMAT_S16_LE);
    snd_pcm_hw_params_set_channels(pcm_handle, params, CHANNELS);
    snd_pcm_hw_params_set_rate(pcm_handle, params, SAMPLE_RATE, 0);

    // Apply parameters
    if ((err = snd_pcm_hw_params(pcm_handle, params)) < 0)
    {
        fprintf(stderr, "Error setting hardware parameters: %s\n", snd_strerror(err));
        return 1;
    }

    printf("Press 'r' to start recording, 's' to stop, 'q' to quit.\n");

    set_nonblocking_mode(1); // Enable non-blocking keyboard input

    while (1)
    {
        int key = key_pressed();
        if (key == 'r')
        {
            printf("Recording started! Press 's' to stop.\n");

            FILE *fp = fopen("test.raw", "wb");
            if (!fp)
            {
                fprintf(stderr, "Error: Failed to open file for writing!\n");
                return 1;
            }

            // Dynamically allocate the buffer
            size_t buffer_size = INITIAL_BUFFER_SIZE;
            unsigned char *buffer = (unsigned char *)malloc(buffer_size);
            if (!buffer)
            {
                fprintf(stderr, "Error: Memory allocation failed!\n");
                fclose(fp);
                return 1;
            }

            int frames_per_buffer = buffer_size / FRAME_SIZE;
            size_t total_bytes_written = 0;

            while (1)
            {
                key = key_pressed();
                if (key == 's')
                {
                    printf("Recording stopped!\n");
                    break;
                }

                int read_frames = snd_pcm_readi(pcm_handle, buffer, frames_per_buffer);
                if (read_frames < 0)
                {
                    fprintf(stderr, "Read error: %s\n", snd_strerror(read_frames));
                    break;
                }

                // Write recorded data directly to file
                size_t bytes_written = fwrite(buffer, sizeof(unsigned char), read_frames * FRAME_SIZE, fp);
                total_bytes_written += bytes_written;

                // If buffer usage exceeds threshold, increase dynamically
                if (total_bytes_written > buffer_size * 2)
                {
                    buffer_size *= 2;
                    buffer = (unsigned char *)realloc(buffer, buffer_size);
                    if (!buffer)
                    {
                        fprintf(stderr, "Error: Memory reallocation failed!\n");
                        fclose(fp);
                        return 1;
                    }
                    frames_per_buffer = buffer_size / FRAME_SIZE;
                }
            }

            fclose(fp);
            free(buffer);
            printf("Recording saved as 'test.raw'. File size: %lu bytes\n", total_bytes_written);
        }

        if (key == 'q')
        {
            printf("Exiting...\n");
            break;
        }

        usleep(100000); // Sleep for 100ms to reduce CPU usage
    }

    set_nonblocking_mode(0); // Restore normal terminal mode
    snd_pcm_close(pcm_handle);

    return 0;
}
