#!/usr/bin/python
# Imports
import webiopi
import time
import subprocess
import os

# Enable debug output
webiopi.setDebug()

# Retrieve GPIO lib
GPIO = webiopi.GPIO
LEFT_DOOR = 7
RIGHT_DOOR = 8
LEFT_STATUS = ' '
RIGHT_STATUS = ' '
LEFT_TIME_OPEN = 0
RIGHT_TIME_OPEN = 0
LEFT_ALERT = 0
RIGHT_ALERT = 0
# About 5 mins
ALERT1 = 375
# About 5 Hours
ALERT2 = 22500

# Called by WebIOPi at script loading
def setup():
    global LEFT_STATUS
    global RIGHT_STATUS
    global LEFT_TIME_OPEN
    global RIGHT_TIME_OPEN
    webiopi.debug("Script with macros - Setup")
    # Setup GPIOs
    GPIO.setFunction(LEFT_DOOR, GPIO.IN)
    GPIO.setFunction(RIGHT_DOOR, GPIO.IN)
    # READ current status from log file
    lines=tail("/usr/share/webiopi/htdocs/l_garage.log",1)
    webiopi.debug(lines)
    LEFT_STATUS = lines[28:29]
    LEFT_TIME_OPEN = int(lines[17:27])
    webiopi.debug(LEFT_TIME_OPEN)
    lines=tail("/usr/share/webiopi/htdocs/r_garage.log",1)
    webiopi.debug(lines)
    RIGHT_STATUS = lines[28:29]
    RIGHT_TIME_OPEN = int(lines[17:27])
    webiopi.debug(RIGHT_TIME_OPEN)

# Looped by WebIOPi
def loop():
    global LEFT_STATUS
    global RIGHT_STATUS
    global LEFT_TIME_OPEN
    global RIGHT_TIME_OPEN
    global LEFT_ALERT
    global RIGHT_ALERT
# Check if we need to send alert
    if(LEFT_STATUS == 'O'):
      sec_now=int(now_in_seconds())
      webiopi.debug('Now:'+str(sec_now)+' LOT:'+str(RIGHT_TIME_OPEN))
      dif=int(sec_now) - int(LEFT_TIME_OPEN)
      if(dif > ALERT1 and LEFT_ALERT == 0):
        LEFT_ALERT = 1
        mail_alert('Door Open L1')
      if(dif>ALERT2 and  LEFT_ALERT == 1):
        LEFT_ALERT = 2
        mail_alert('Door Open L2')
    if(LEFT_STATUS == 'C' and  LEFT_ALERT != 0):
        LEFT_ALERT = 0
        mail_alert('Door Close L')

    if(RIGHT_STATUS == 'O'):
      sec_now=int(now_in_seconds())
      webiopi.debug('Now:'+str(sec_now)+' ROT:'+str(RIGHT_TIME_OPEN))
      dif=int(sec_now) - int(RIGHT_TIME_OPEN)
      if(dif > ALERT1 and RIGHT_ALERT == 0):
        RIGHT_ALERT = 1
        mail_alert('Door Open R1')
      if(dif>ALERT2 and  RIGHT_ALERT == 1):
        RIGHT_ALERT = 2
        mail_alert('Door Open R2')
    if(RIGHT_STATUS == 'C' and  RIGHT_ALERT != 0):
        RIGHT_ALERT = 0
        mail_alert('Door Close R')


    if(GPIO.digitalRead(LEFT_DOOR) == GPIO.HIGH):
      NEW_LEFT_STATUS  = 'O'
    if(GPIO.digitalRead(LEFT_DOOR) == GPIO.LOW):
      NEW_LEFT_STATUS  = 'C'
    if(NEW_LEFT_STATUS != LEFT_STATUS):
      LEFT_STATUS=NEW_LEFT_STATUS
      webiopi.debug(subprocess.call(["/usr/share/webiopi/htdocs/l_logger.sh "+LEFT_STATUS],shell=True))
      webiopi.debug('NEW LEFT STATUS: '+LEFT_STATUS)
      if(LEFT_STATUS=='O'):
        LEFT_TIME_OPEN=int(now_in_seconds())

    if(GPIO.digitalRead(RIGHT_DOOR) == GPIO.HIGH):
      NEW_RIGHT_STATUS  = 'O'
    if(GPIO.digitalRead(RIGHT_DOOR) == GPIO.LOW):
      NEW_RIGHT_STATUS  = 'C'
    if(NEW_RIGHT_STATUS != RIGHT_STATUS):
      RIGHT_STATUS=NEW_RIGHT_STATUS
      webiopi.debug(subprocess.call(["/usr/share/webiopi/htdocs/r_logger.sh "+RIGHT_STATUS],shell=True))
      webiopi.debug('NEW RIGHT STATUS:'+RIGHT_STATUS);
      if(RIGHT_STATUS=='O'):
        RIGHT_TIME_OPEN=int(now_in_seconds())

    webiopi.sleep(1) 

# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("Script with macros - Destroy")
    # Reset GPIO functions

def tail(f, n):
  p=subprocess.Popen(['tail','-n',str(n),f],stdout=subprocess.PIPE,universal_newlines=True)
  cnt=0
  line=p.stdout.readline()
  while (cnt < n):
    line = line + p.stdout.readline()
    cnt = cnt + 1
  return line

def mail_alert(msg):
   p=subprocess.Popen(['/usr/share/webiopi/htdocs/mail.py',msg],stdout=subprocess.PIPE,universal_newlines=True)
   webiopi.debug('Send mail')
   return

def now_in_seconds():
  p=subprocess.Popen(['date','+%s'],stdout=subprocess.PIPE,universal_newlines=True)
  secs=p.stdout.readline()
  return secs

@webiopi.macro
def l_log_read():
    lines=tail("/usr/share/webiopi/htdocs/l_garage.log",10)
    return lines

@webiopi.macro
def r_log_read():
    lines=tail("/usr/share/webiopi/htdocs/r_garage.log",10)
    return lines

@webiopi.macro
def l_log_read1():
    lines=tail("/usr/share/webiopi/htdocs/l_garage.log",1)
    return lines

@webiopi.macro
def r_log_read1():
    lines=tail("/usr/share/webiopi/htdocs/r_garage.log",1)
    return lines
