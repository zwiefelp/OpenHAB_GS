#!/bin/sh
killall -9 udptomqtt
/etc/openhab2/bin/udptomqtt -t /openhab/in/rfswitches/state >/var/log/openhab2/udptomqtt.log 2>&1 &

