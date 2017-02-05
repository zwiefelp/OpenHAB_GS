#!/usr/bin/python
#
# Copyright 2014 Mikael Magnusson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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
    #logger.addHandler(logging.StreamHandler())

    liblogger = logging.getLogger('lightify')
    #liblogger.addHandler(logging.StreamHandler())
    liblogger.setLevel(logging.INFO)

    logger.info("Logging %s", MODULE)

    ip = "192.168.20.66"
	 
    conn = lightify.Lightify(ip)

    conn.update_all_light_status()
    conn.update_group_list()

    print "Groups"
    for (name, group) in conn.groups().iteritems():
        print "group: %s %s" % (name, group)
    
    
    print ""
    print "keys:%s" % conn.groups().keys()
#    desk = conn.groups()["Desk"]
#    desk.set_onoff(0)
#    desk.set_luminance(0, 0)
#    desk.set_onoff(1)
#    desk.set_luminance(25, 10)

 #   sys.exit(0)
    print ""
    print "Addr On/Off Lum Temp RGB Name"
    for (addr, light) in conn.lights().iteritems():
        print "%x %d %d %d %s %s" % (addr, light.on(), light.lum(), light.temp(), light.rgb(), light)

#    sys.exit(0)
    print ""

    for (name, group) in conn.groups().iteritems():
        lights = group.lights()
        print "Group %s - Lights: %s" % (name,lights)

    light = conn.light_byname("Bett")
    printlight(light)
    
    sys.exit(0)

main(sys.argv)



