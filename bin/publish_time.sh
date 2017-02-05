#/bin/bash
t=$(date +%H:%M 2>&1)
d=$(date +%a,%d.%m.%Y 2>&1)
/usr/bin/mosquitto_pub -h 192.168.20.17 -p 1883 -t /openhab/Daytime -m $t
/usr/bin/mosquitto_pub -h 192.168.20.17 -p 1883 -t /openhab/DayDate -m $d

