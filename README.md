# Garage Door Opener for Raspberry Pi

This is sample code to open/close your garage door using a Raspberry Pi, a sainsmart relay (https://www.amazon.ca/SainSmart-2-Channel-Arduino-Raspberry-Electronic/dp/B0057OC6D8/ref=sr_1_3?ie=UTF8&qid=1506869627&sr=8-3&keywords=sainsmart+relay), and a couple of Normally Open (NO) reed switch. Note. I did try some other relay before and it did not work. That is why I am pushing for the SainSmart relay.
This code, will allow you to open/close your garage door from anywhere in the world, see the status of your garage door to see if it is open/close. It will also log, the open/closure time of the garage door and send you email or text message if you left the garage door open too long. It is currently set-up to send email/text if it is open for more than 5 mins for first alert and more than 5 hours for second alert. Also, if it sent and alert, it will also alert when the door is closed.

This sample code is using GPIO pin 7 for the magnetic sensor to read if the left door is open/close, gpio 17 to send the signal to the relay to open/close the left door. It is using pin 8 for the sensor for right door and pin 18 for the relay for the right door.

For this to work, we have garage2.html which is the code to show you the status of the door, give you the button to open/close the door, show you a log of when the door was closed/opened. We have myscript.py is the code that monitor the garage door, log when it was opened/closed, send alerts if it is opened too long. garage2.html is really the client and myscript.py is acting as a server code. garage2.html will be calling code from myscript.py to get log information. myscript.py will be calling l_logger.sh and r_logger.sh to write log when door is open/close. It will also called mail.py to send mail or text. It is sending text using email to SMS services.

To use this, follow this instruction

. Use Putty to connect to your raspberry pi. You can download putty @ http://www.putty.org/

. You normally sign in using id 'pi' and your password. If you did not change the password, the default password is 'raspberry'.

. Use this command sudo nano /etc/webiopi/config That will bring up the nano editor to change the config file.

. The main thing to edit is my script need to be uncommented for it to run. You need to point to where the file is. e.g myscript = /usr/share/webiopi/htdocs/myscript.py. To exit, press CTRL-X.

. Another option is to copy the config file here to /etc/webiopi using sudo mv ./config /etc/webiopi/config

. In myscript.py, I am using GPIO 7, 8 to read if the door is open or close, you would need to adjust if needed.

. You can use 'sudo nano /usr/share/webiopi/htdocs/myscript.py' to edit it and adjust the line LEFT_DOOR and RIGHT_DOOR if needed.

. Note: If you are using different GPIO pin, you need to adjust garage2.html as well. The code is reading pin 7, and 8 for the sensor and is using pin 17, 18 which is connected to the relay to open/close the door.

. You should make sure that the code are executable by everyone using these commands

sudo chmod 775 /usr/share/webiopi/htdocs/myscript.py

sudo chmod 775 /usr/share/webiopi/htdocs/r_logger.sh

sudo chmod 775 /usr/share/webiopi/htdocs/l_logger.sh

sudo chmod 775 /usr/share/webiopi/htdocs/mail.py

. You shoud create your log files and make them writable using these commands

sudo touch /usr/share/webiopi/htdocs/l_garage.log

sudo touch /usr/share/webiopi/htdocs/r_garage.log

sudo chmod 666 /usr/share/webiopi/htdocs/l_garage.log

sudo chmod 666 /usr/share/webiopi/htdocs/r_garage.log

. You should edit mail.py using sudo nano /usr/share/webiopi/htdocs/mail.py to put your email address or email to SMS address. You need to modify the to_addr_list, your login, and password.

. If you get and error for your email, you will need to ask gmail to allow to send from less secure. Follow instruction from the mail you will get from gmail. You can also just test the email using 

sudo /usr/share/webiopi/htdocs/mail.py test

. If you want to change the timing of the alert, you can edit ALERT1 and ALERT2 in myscript.py. Note each second is about 1.25. For example, if you want 60 seconds, you enter 75. That number may differ depending on which pi, you have. This is tested on a PI 3

Hope that you can get it to work.
