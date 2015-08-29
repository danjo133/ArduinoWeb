This repository is about a default setup for developing/prototyping 
IoT applications with a Raspberry Pi and an Arduino.

To setup the RPi you need raspbian:
https://www.raspberrypi.org/downloads/

Download the image and unpack the zip-file.
Then you can install it from Linux to your sd-card of choice with dd.

When booting your RPi for the first time, you will get into a configuration utility.
* From there you can resize the filesystem to use all of the available space
* Set the password
* Set locale (enable en_US.utf8 and sv_SE.utf8)
* From advanced options - enable ssh-server

After that, reboot and log in with the defaul user 'pi' and the password you just set.

Now we're ready to install some software.

 $ sudo apt-get install python3-rpi.gpio python3-pip

Second, clone this repo:

 $ git clone https://github.com/danjo133/arduinoweb.git

Then you can go into arduinoweb and run:

 $ pip install -r requirements.txt
 $ # And then to run the webserver:
 $ python3 main.py
 
Now your web-server is up and running and allow you to point your browser to the raspberry pi on port 5000!