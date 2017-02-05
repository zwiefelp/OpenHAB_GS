#!/bin/bash

# Aufruf: lightify.sh command group/lamp code data

d2h() {
    t=$(echo "obase=16; $1" | bc) 
    t="0000$t"
    t=${t:${#t}-4:4}
    t=${t:2:2}${t:0:2}
    echo $t
}

if [ $1 = "Switch" ]; then
    if [ $2 = "Lamp" ]; then
	com="0f00003286000000"
	code=$3
    fi
    if [ $2 = "Group" ]; then
	com="0f00023215000000"
	code="${3}00000000000000"
    fi
    if [ $4 = "ON" ]; then
	data="01"
    else
	data="00"
    fi
fi

if [ $1 = "Brightness" ]; then
    if [ $2 = "Lamp" ]; then
        com="1100803119000000"
	code=$3    
    fi
    if [ $2 = "Group" ]; then
	com="1100823116000000"
	code="${3}00000000000000"
    fi
    t=$(printf "%x" $4)
    t="00$t"
    t=${t:${#t}-2:2}
    data="${t}0100"
fi 

if [ $1 = "ColTemp" ]; then
    if [ $2 = "lamp" ]; then
        com="120080331A000000"
	code=$3    
    fi
    if [ $2 = "Group" ]; then
	com="120082331C000000"
	code="${3}00000000000000"
    fi
    t=$(d2h $4)
    data="${t}0100"
fi

if [ $com = "" ]; then
    echo -e "Command Unknown"
else
    send=${com}${code}${data}
    echo -e $send
    echo -e $send | /usr/bin/xxd -r -p | /bin/nc -q 1 192.168.20.66 4000
fi
