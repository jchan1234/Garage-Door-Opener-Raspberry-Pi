# Garage Door Opener for Raspberry Pi

This is for a remote garage door opener using a raspberry pi, a 2 channel relay, and a couple of NO (Normally Open) switch.

Here is the link for SainSmart 2 Channel Relay. I tried some other relay but did not work well with the pi.
https://www.amazon.ca/SainSmart-2-Channel-Arduino-Raspberry-Electronic/dp/B0057OC6D8/ref=sr_1_2?keywords=sainsmart+2+channel+relay&qid=1553876623&s=gateway&sr=8-2

Link for 2 NO switch. You can use any NO switch
https://www.amazon.ca/uxcell%C2%AE-uxcell3Sets-Magnetic-Normally-Security/dp/B07F5ZDLDR/ref=sr_1_5?crid=3F08GJP32J9WJ&keywords=normally%2Bopen%2Bmagnetic%2Bswitch&qid=1553876734&s=gateway&sprefix=Normally%2BOpen%2Caps%2C241&sr=8-5&th=1

This will allow you to open/close 2 garage doors, log open and close time and email me if door is left open for more than 5 mins and more than 5 hours. Also, if it alerted me, it will also alert me when it is closed. Also show the last 10 lines of the log on the page.
Uses WebIOPI.

GPIO Configuration
------------------
1 (3.3V) - Connect to the Right NO switch. Send some power to the switch. (2 cables)
2 (5.0V) - Sainsmart Power VOC (This will provide power to the relay switch)
6 (Gnd)  - Connect to the Right NO switch.
9 (Gnd)  - Sainsmart GND (Ground)
11(GPIO17) - Sainsmart IN2 (Switch for Left Door to send open/close signal)
12(GPIO18) - Sainsmart IN1 (switch for Right Door to send open/close signal)
17 (3.3V) - Connect to Left NO switch. Send some power to the switch. (2 cables)
24(GPIO8) - Connect to the right NO switch.(2 cables)
26(GPIO7) - Connect to the left NO switch.(2 cables)
39(gnd)   - Connect to left NO switch

Connection from relay to garage door opener
-------------------------------------------
Most garage door opener will have a simple push button to open and close. You can find out where the cable from those button connect to. You can connect 2 new wires there and when both wires are connected for a short period, it should send the signal to open/close the door. You need to connect 1 cable to K1 or K2 and the other one to the connection below.
e.g
-|
/
k1---> To garage door opener 
-|---> To garage door opener

How to prepare cable (2 cables) for NO switch
---------------------------------------------
You need a 10kOhm and a 1kOhm resistor to prepare a 2 cables connector.
Example. Using 1 (3.3v) and 24 (GPIO 8) for 2 cables 
         Using 6(Gnd) for the second cable 

3.3 V -> 10kOhm resistor------->|
                                |----->|
GPIO Input -> 1lOhm resistor -->|      | NO Switch
                                       |
Gnd ---------------------------------->|

The way, the NO switch works is that when the garage is close, the power will go to the ground.
When it is open, the power will go to the GPIO. The resistor are there to cut back the electricity so that it does not burn the pi.

Code description
----------------
garage2.html and myscript.py are the main programs.

garage2.html build and display the page. It also give you the button to open/close the door and any other UI interface on the web page. It is the front-end portion. Written in Javascript.

myscript.py monitors the garage status and log open and close time to a file. Also send alert when door is left open too long. It is the back-end portion. Written in python.

l_logger.sh logs open and close time to l_garage.log. 
r_logger.sh logs open and close time to r_garage.log
mail.py sends email when door is left open too long.

Those 3 scripts above are called by myscript.py

Change the attribute of install.sh and run it using sudo. Below are the commands
chmod 775 install.sh
sudo ./install.sh

What does install.sh do?
------------------------
. Download webiopi
. Download webiopi patch to work for newer pi like pi2 and above
. Install webiopi
. Change attribute of /usr/share/webiopi/htdocs to be owned by pi instead of root
. Change attribute of Garage pi code to be able and copy to /usr/share/webiopi/htdocs
. Copy new webiopi config to /etc/webiopi/config
. Get webiopi to startup automatically on reboot

To reboot pi, issue this command
sudo reboot

To set-up a password for the site, follow instruction here
http://webiopi.trouch.com/PASSWORD.html

To access the site, go to http://<ip address of pi>:8000

If you want to install webiopi and the patch, look here.
https://github.com/doublebind/raspi

For more information on webiopi, look here
http://webiopi.trouch.com/

Original code comes from https://www.driscocity.com/idiots-guide-to-a-raspberry-pi-garage-door-opener/

You can get instruction on how to configure and connect the hardware (PI, RELAY, SWITCH) and other software (RASPIAN, WEBIOPI) needed there.
