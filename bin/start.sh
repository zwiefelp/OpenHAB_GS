#!/bin/sh
/usr/bin/killall -9 udptomqtt
/bin/sleep 1
/etc/openhab2/bin/udptomqtt -t /openhab/in/rfswitches/state >/var/log/openhab2/udptomqtt.log 2>&1 &
