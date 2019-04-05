#!/bin/bash
echo '**** Get WEBIOPI ****'
`wget http://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz`
echo '**** untar WEBIOPI ****'
`tar xvzf WebIOPi-0.7.1.tar.gz`
cd WebIOPi-0.7.1
echo $PWD
echo '**** Get WEBIOPI patch ****'
`wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch`
echo '**** Patch WEBIOPI ****'
patch -p1 -i webiopi-pi2bplus.patch
echo '**** Install WEBIOPI ****'
./setup.sh
cd ..
echo $PWD
echo '**** Install ffmpeg ****'
apt-get install install ffmpeg
echo '**** Copy Garage Pi ****'
`chown -R pi:pi /usr/share/webiopi`
`chmod 775 *.py`
`chmod 775 *.sh`
`chmod 666 *.log`
`cp garage2.html /usr/share/webiopi/htdocs/`
`cp myscript.py /usr/share/webiopi/htdocs/`
`cp mail.py /usr/share/webiopi/htdocs/`
`cp l_logger.sh /usr/share/webiopi/htdocs/`
`cp r_logger.sh /usr/share/webiopi/htdocs/`
`cp temperature.sh /usr/share/webiopi/htdocs/`
`cp closed.png /usr/share/webiopi/htdocs/`
`cp open.png /usr/share/webiopi/htdocs/`
`cp r_garage.log /usr/share/webiopi/htdocs/`
`cp l_garage.log /usr/share/webiopi/htdocs/`
`cp /etc/webiopi/config /etc/webiopi/config.orig`
`mkdir /usr/share/webiopi/htdocs/vo`
`mkdir /usr/share/webiopi/htdocs/po`
`cp config /etc/webiopi/config`
`update-rc.d webiopi defaults`
echo '**** Done install WEBIOPI and Garage pi ****'