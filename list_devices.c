#include <stdio.h>
#include <portaudio.h>

int main()
{
    Pa_Initialize();
    int numDevices = Pa_GetDeviceCount();
    const PaDeviceInfo *deviceInfo;

    printf("Available audio input devices:\n");
    for (int i = 0; i < numDevices; i++)
    {
        deviceInfo = Pa_GetDeviceInfo(i);
        printf("Device %d: %s\n", i, deviceInfo->name);
    }

    Pa_Terminate();
    return 0;
}
