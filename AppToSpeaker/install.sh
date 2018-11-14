#!/bin/sh

#install pulse audio
sudo apt install pulseaudio-module-bluetooth
pulseaudio --k
pulseaudio --start

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential python-dev libbluetooth-dev 
