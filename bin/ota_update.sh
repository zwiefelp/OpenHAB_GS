#!/bin/bash
echo "Scanning for Arduino OTA devices on the network ..."
ip_arr=($(((avahi-browse _arduino._tcp --resolve --parsable --terminate) 2>/dev/null | grep -F "=;") | cut -d\; -f8))
if [ ${#ip_arr[@]} == 0 ]
then
	    echo "No devices found"
	        exit
	fi
	echo "IP addresses found: "
	printf '\t%s\n' "${ip_arr[@]}"

	read -p "Path to binary: " path
	read -p "Password: " password

	read -p "Press [ENTER] to start OTA"
	echo    "--------------------------"

	for ip in ${ip_arr[@]}
	do
		    python2 /home/$USER/.arduino15/packages/esp8266/hardware/esp8266/2.3.0/tools/espota.py -i $ip -p 8266 --auth="$password" -f "$path" 2> /dev/null && echo -e "Success:\t$ip" || echo -e "Fail:   \t$ip" &
	done
	wait
