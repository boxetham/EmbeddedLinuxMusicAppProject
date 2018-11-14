# EmbeddedLinuxMusicAppProject

Insert the USB Audio Dongle into one of the USB ports on the BeagleBone. 
Connect a speaker to the dongle using an auxiliary cable. 

Run the setup.sh file (./setup.sh) to make the BeagleBone discoverable via Bluetooth. If the phone is unable to find the BeagleBone, simply run setup.sh again. 
The BeagleBone should be running the perky_blue.py (may have to run as root, 'sudo ./perky_blue.py') program found in AppToSpeaker folder.

Open the Android app. 

Start by selecting "discover" and then selecting your BeagleBone device to Bluetooth connect to. 
Select the song to play once the BeagleBone is connected to the device. 
You can also manually input a file to play that is not one of the songs listed by selecting the "Play Custom Song" button, then enter the file name without the extension and press enter.
If you want to download a new song onto the bone to play, press the "Download Song" button and enter the link to download the mp3 file. The bone must have an internet connection for this feature to work properly. 
Once the song is downloaded, you can use the "Play Custom Song" button to input the file name and play the song. 
Once songs are playing, they can be controlled by the buttons at the bottom of the application. 
From left to right, the buttons are: Pause, Play, Stop, Volume Down, and Volume Up. 
Closing the Android Application will end the program on the bone.
