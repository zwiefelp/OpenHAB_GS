#!/usr/bin/python
import lightify
import sys
import time
import logging

MODULE = "__main__"

def printlight(light):
    print "{\"on\":\"%d\",\"lum\":\"%d\",\"temp\":\"%d\",\"rgb\":\"%s\",\"name\":\"%s\"}" % (light.on(), light.lum(), light.temp(), light.rgb(), light)
    return

def main(argv):
    logging.basicConfig()

    logger = logging.getLogger(MODULE)
    logger.setLevel(logging.DEBUG)

    ip = "192.168.20.66"
    conn = lightify.Lightify(ip)
    conn.update_all_light_status()
    conn.update_group_list()

    light = conn.light_byname(argv[1])
    if light is not None: 
	printlight(light)
	sys.exit(0)
    
    group = conn.groups()[argv[1]]
    if group is not None:
	for light_addr in group.lights():
	    light = conn.lights()[light_addr]
	    printlight(light)
	sys.exit(0)
    
    print "{ERROR}"
    sys.exit(0)


if len(sys.argv) > 1:
    main(sys.argv)
print "{ERROR}"