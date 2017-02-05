#!/bin/bash
rm /var/www/html/openhab/photovz.jpg
/usr/bin/wget -qO - http://192.168.20.67:8080/photo.jpg | /usr/bin/convert - -rotate 90 -flop /var/www/html/openhab/photovz.jpg

