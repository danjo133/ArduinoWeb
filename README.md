# Introduction

This repository is about a default setup for developing/prototyping 
IoT applications with a Raspberry Pi and an Arduino.

# Initial setup of your Raspberry Pi

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

# Raspberry Pi configuration

Now we're ready to install some software.

    $ sudo apt-get update
    $ sudo apt-get upgrade # will download up to 150MB of packages.
    $ sudo apt-get install emacs

# Get the code and dependencies that you will base your project on

Begin by cloning this repo:

    $ git clone https://github.com/danjo133/ArduinoWeb.git

Then you can go into arduinoweb and run:

    $ pyvenv-3.4 env
    $ source env/bin/activate
    $ pip install RPi.GPIO
    $ pip install -r requirements.txt

And now you're done, time to to run the webserver!

    $ python3 main.py
 
Now your web-server is up and running and allow you to point your browser to the raspberry pi on port 5000!
