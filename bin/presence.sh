#!/bin/bash

MAC="CC:20:E8:9F:83:17"
#while true do
    if /usr/bin/l2ping -c 1 $MAC &> /dev/null 
    then
	#echo "ON"
	curl --max-time 2 --connect-timeout 2 --header "Content-Type: text/plain" --request PUT --data "ON" http://127.0.0.1:8080/rest/items/phone1/state
    else
	#echo "OFF"
	curl --max-time 2 --connect-timeout 2 --header "Content-Type: text/plain" --request PUT --data "OFF" http://127.0.0.1:8080/rest/items/phone1/state
    fi
#    sleep 30
#done