#!/bin/bash
rm /var/www/html/openhab/photowz.jpg
/usr/bin/wget -qO - http://192.168.20.59:8080/photo.jpg | /usr/bin/convert - -rotate 270 /var/www/html/openhab/photowz.jpg

