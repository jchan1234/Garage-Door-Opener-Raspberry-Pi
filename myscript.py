#!/usr/bin/python
# Imports
import webiopi
import time
import datetime
import subprocess
import os
from os import listdir

# Enable debug output
#webiopi.setDebug()

# Retrieve GPIO lib
GPIO = webiopi.GPIO
LEFT_DOOR = 7
RIGHT_DOOR = 8
LEFT_DOOR_BUTTON = 17
RIGHT_DOOR_BUTTON = 18
LEFT_STATUS = ' '
RIGHT_STATUS = ' '
LEFT_TIME_OPEN = 0
RIGHT_TIME_OPEN = 0
LEFT_ALERT = 0
RIGHT_ALERT = 0
AUTO_CLOSE = 1
AUTO_CLOSE_START = 22
AUTO_CLOSE_END = 6
#DEBUG='ON'
DEBUG='OFF'

# About 5 mins
ALERT1 = 375
#ALERT1 = 20
# About 5 Hours
ALERT2 = 22500
#ALERT2 = 25

path='/usr/share/webiopi/htdocs/'
po=path+'po/'

# Called by WebIOPi at script loading
def setup():
    global LEFT_STATUS
    global RIGHT_STATUS
    global LEFT_TIME_OPEN
    global RIGHT_TIME_OPEN
    # Setup GPIOs
    GPIO.setFunction(LEFT_DOOR, GPIO.IN)
    GPIO.setFunction(RIGHT_DOOR, GPIO.IN)
    #GPIO.setFunction(LEFT_DOOR_BUTTON, GPIO.OUT)
    # READ current status from log file
    lines=tail(path+"l_garage.log",1)
    if(lines!=''):
      LEFT_STATUS = lines[28:29]
      LEFT_TIME_OPEN = int(lines[17:27])
    if(lines==''):
      LEFT_STATUS = 'O'
      LEFT_TIME_OPEN = int(now_in_seconds())
    lines=tail(path+"r_garage.log",1)
    if(lines!=''):
      RIGHT_STATUS = lines[28:29]
      RIGHT_TIME_OPEN = int(lines[17:27])
    if(lines==''):
      RIGHT_STATUS = 'O'
      RIGHT_TIME_OPEN = int(now_in_seconds())
    return

# Looped by WebIOPi
def loop():
    global LEFT_STATUS
    global RIGHT_STATUS
    global LEFT_TIME_OPEN
    global RIGHT_TIME_OPEN
    global LEFT_ALERT
    global RIGHT_ALERT
    debug_log('LEFT:'+LEFT_STATUS+' RIGHT:'+RIGHT_STATUS)

# Check if we need to send alert
    while True:
      if(LEFT_STATUS == 'O'):
        sec_now=int(now_in_seconds())
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
      if(GPIO.digitalRead(RIGHT_DOOR) == GPIO.HIGH):
        NEW_RIGHT_STATUS  = 'O'
      if(GPIO.digitalRead(RIGHT_DOOR) == GPIO.LOW):
        NEW_RIGHT_STATUS  = 'C'

      if(NEW_LEFT_STATUS != LEFT_STATUS):
        debug_log('NEW LEFT:'+NEW_LEFT_STATUS)
        if(NEW_LEFT_STATUS=='O'):
          cam2()
          debug_log('CAM2 for L')
        LEFT_STATUS=NEW_LEFT_STATUS
        if(LEFT_STATUS=='O'):
          LEFT_TIME_OPEN=int(now_in_seconds())
          write_log('l','O')
          webiopi.debug('Called left logger for open')
        if(LEFT_STATUS=='C'):
          write_log('l','C')

      if(NEW_RIGHT_STATUS != RIGHT_STATUS):
        debug_log('NEW RIGHT:'+NEW_RIGHT_STATUS)
        if(NEW_RIGHT_STATUS=='O'):
          cam2()
        RIGHT_STATUS=NEW_RIGHT_STATUS
        if(RIGHT_STATUS=='O'):
          RIGHT_TIME_OPEN=int(now_in_seconds())
          write_log('r','O')
        if(RIGHT_STATUS=='C'):
          write_log('r','C')

      webiopi.sleep(1)
    
    return 

# Called by WebIOPi at server shutdown
def destroy():
  # Reset GPIO functions
  return

def tail(f, n):
  p=subprocess.Popen(['tail','-n',str(n),f],stdout=subprocess.PIPE,universal_newlines=True)
  cnt=0
  line=p.stdout.readline()
  while (cnt < n):
    line = line + p.stdout.readline()
    cnt = cnt + 1
  return line

def mail_alert(msg):
   p=subprocess.Popen([path+'mail.py',msg],stdout=subprocess.PIPE,universal_newlines=True)
   debug_log('Send mail')
   return

def debug_log(m):
  if(DEBUG=='ON'):
    p=subprocess.Popen(['date','+%Y-%m-%d_%H:%M:%S'],stdout=subprocess.PIPE,universal_newlines=True)
    ts=p.stdout.readline()
    with open(path+'debug.log','a') as file_dbg:
      file_dbg.write(ts[:19]+' '+m+'\n')
  return

def write_log(g,s):
  p=subprocess.Popen(['date','+%Y-%m-%d_%H:%M_%s'],stdout=subprocess.PIPE,universal_newlines=True)
  ts=p.stdout.readline()
  debug_log('ts:'+ts)
  out=ts[:27]+' '+s+' ++'
  if(g=='l'):
    with open(path+'l_garage.log','a') as l_garage_file:
      l_garage_file.write(out+'\n')
  if(g=='r'):
    with open(path+'r_garage.log','a') as r_garage_file:
      r_garage_file.write(out+'\n')
  webiopi.debug('Write Log'+out)
  debug_log('Write Log '+g+' '+out)
  now=datetime.datetime.now()
  return

def now_in_seconds():
  p=subprocess.Popen(['date','+%s'],stdout=subprocess.PIPE,universal_newlines=True)
  secs=p.stdout.readline()
  return secs

def now_in_hours():
  p=subprocess.Popen(['date','+%H'],stdout=subprocess.PIPE,universal_newlines=True)
  hours=p.stdout.readline()
  debug_log('Hour:'+hours)
  return hours

@webiopi.macro
def l_log_read():
    lines=tail(path+"l_garage.log",10)
    p=subprocess.Popen([path+'temperature.sh'],stdout=subprocess.PIPE,universal_newlines=True)
    cpu_t=p.stdout.readline()
    lines=lines+'Temperature:'+cpu_t[:3]+' ++'
    return lines

@webiopi.macro
def r_log_read():
    lines=tail(path+"r_garage.log",11)
    return lines

@webiopi.macro
def l_log_read1():
    lines=tail(path+"l_garage.log",1)
    return lines

@webiopi.macro
def r_log_read1():
    lines=tail(path+"r_garage.log",1)
    return lines

@webiopi.macro
def takePic():
    subprocess.call('systemctl stop motioneye',shell=True)
    subprocess.call('raspistill -w 320 -h 240 -mm matrix -vf -hf -o /usr/share/webiopi/htdocs/cam.jpg',shell=True)
    subprocess.call('raspivid -w 320 -h 240 -mm matrix -vf -hf -o /usr/share/webiopi/htdocs/vid.h264 -t 30000',shell=True)
    subprocess.call('systemctl start motioneye',shell=True)
    subprocess.call('ffmpeg -y -i /usr/share/webiopi/htdocs/vid.h264 -c copy /usr/share/webiopi/htdocs/vid.mp4',shell=True)
    now=datetime.datetime.now()
    cur_ts=now.strftime("%Y-%m-%d_%H:%M")
    subprocess.call('cp /usr/share/webiopi/htdocs/cam.jpg /usr/share/webiopi/htdocs/po/p'+cur_ts+'.jpg',shell=True)
    subprocess.call('cp /usr/share/webiopi/htdocs/vid.mp4 /usr/share/webiopi/htdocs/vo/v'+cur_ts+'.mp4',shell=True)
    return
	
@webiopi.macro
def pic_list():
	os.chdir(po)
	files = filter(os.path.isfile, os.listdir(po))
	files = sorted(files)
	cnt=0
	max=20
	for file in files:
		if cnt==0:
		  files_str=file[1:17]
		else:
		  files_str=files_str+' '+file[1:17]
		cnt=cnt+1
		if cnt==max:
		  break
	return files_str
	
@webiopi.macro
def del_pic(ts):
	subprocess.call('rm /usr/share/webiopi/htdocs/po/p'+ts+'.jpg',shell=True)
	subprocess.call('rm /usr/share/webiopi/htdocs/vo/v'+ts+'.mp4',shell=True)
	return
    
def cam2():
  webiopi.sleep(8)
  takePic()
  return
