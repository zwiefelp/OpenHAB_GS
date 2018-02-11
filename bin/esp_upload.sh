fw=firmware.bin
ip=192.168.1.129
echo -e "Uploading $fw to $ip"
python2 /home/pi/.arduino15/packages/esp8266/hardware/esp8266/2.4.0/tools/espota.py -i $ip -p 8266 -f "/etc/openhab2/espconfig/$fw" && echo -e "Success:\t$ip" || echo -e "Fail:   \t$ip" 

