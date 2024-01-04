# laundrypi
A small project for sending alerts when laundry is done.

## Materials List
- Raspberry Pi Zero W
- Raspberry Pi Zero power adapter
- 16GB microSD card
- Raspiaudio Mic+ v2 audio hat

## Preparations
1. Flash your microSD card using Raspberry Pi Imager (which you can install [here](https://www.raspberrypi.com/software/)).
2. Make sure to enable SSH and WiFi, as well as set user credentials during config.
3. Insert your microSD card into the Pi.
4. Attach the audio hat to the Pi by pressing it into the GPIO pins.
5. Plug the power adapter into your Pi.
6. Wait for your Pi to become available through SSH on your network.

## Hat Installation
The majority of this installation will mirror the process given by raspiaudio in their instructions for setting up the mic+ v1 hat, which can be found [here](https://forum.raspiaudio.com/t/mic-installation-guide/17).

First, we will need to add our user to the gpio group:
```bash
sudo usermod -aG gpio $USER
```
This will allow our user to interact with the pins utilized by the hat.

Next we run a bash script provided by raspiaudio to configure the hat. The source can be found [here](https://raspiaudio.com/s/mic1), and it is encouraged to verify any code personally before executing it.

Run the install script:
```bash
wget -O - mic.raspiaudio.com | bash
```

Accept the prompt to reboot the Pi.

Finishing the installation requires executing the test script post-install, which can be found [here](https://raspiaudio.com/s/test).

Run the test script:
```bash
wget -O - test.raspiaudio.com | bash
```

Press the onboard button on the hat and you should hear "front left", then "front right". This confirms the hat was installed correctly.

