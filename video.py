#!/usr/bin/python
# Imports
import sys
import subprocess
cur_ts=str(sys.argv[1])
subprocess.call('raspivid -w 320 -h 240 -mm matrix -vf -hf -o /usr/share/webiopi/htdocs/vid.h264 -t 30000',shell=True)
subprocess.call('systemctl start motioneye',shell=True)
subprocess.call('ffmpeg -y -i /usr/share/webiopi/htdocs/vid.h264 -c:v libvpx -cpu-used 5 -threads 8 /usr/share/webiopi/htdocs/vid.webm',shell=True)
subprocess.call('cp /usr/share/webiopi/htdocs/vid.webm /usr/share/webiopi/htdocs/vo/v'+cur_ts+'.webm',shell=True)