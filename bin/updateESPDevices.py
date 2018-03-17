#!/usr/bin/python

from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange
from time import sleep
import socket
import re

DB_NAME = 'espDevices'

TABLES = {}
TABLES['device'] = (
    "CREATE TABLE `device` ("
    "`id` varchar(20) NOT NULL,"
    "`servicename` varchar(50) NOT NULL,"
    "`ipaddr` varchar(16) NOT NULL,"
    "`configfile` varchar(255) NOT NULL,"
    "`status` enum('Online','Offline') NOT NULL,"
    "`topic` varchar(255) NOT NULL,"
    "`last_seen` timestamp NOT NULL,"
    "PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

global dbconn


def connect_db():
    global dbconn
    try:
        dbconn = mysql.connector.connect(user='pi', password='', host='localhost', database=DB_NAME)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            exit()
        else:
            print(err)
            exit()


def create_tables():
    global dbconn
    cursor = dbconn.cursor()
    for name, ddl in TABLES.iteritems():
        try:
            # print("Creating table \"{}\": ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                pass
                # print("already exists.")
            else:
                pass
                # print(err.msg)
        else:
            pass
            # print("OK")

    cursor.close()


def reset_devices():
    global dbconn
    cursor = dbconn.cursor()
    query = "update device set status='Offline'"
    cursor.execute(query)
    dbconn.commit()
    cursor.close()


def update_device(espid, servicename, ipaddr, status):
    global dbconn
    cursor = dbconn.cursor()

    query = "SELECT * FROM device WHERE id = %s and status = %s"
    cursor.execute(query, (espid, "Offline"))
    rows = len(cursor.fetchall())

    # print("Found %i rows" % rows)
    # Read Config Topic from Config gile
    filename = "/etc/openhab2/espconfig/esp" + espid + ".conf"
    f = open(filename,"r")
    for line in f:
        cfgline = line.split(":")
        if cfgline[0] == "cmdTopic":
            topic = cfgline[1].split("/")[3]

    if rows > 0:
        query = "update device set ipaddr=%s, status=%s, topic=%s, last_seen=now(), configfile=%s where id=%s"
        # print(query % (ipaddr, status, topic, espid))
        cursor.execute(query, (ipaddr, status, topic, filename, espid))
    else:
        query = "insert into device (id,servicename,ipaddr,status,topic,last_seen,configfile) values(%s,%s,%s,%s,%s,now(),%s)"
        # print(query % (espid, servicename, ipaddr, status, topic))
        cursor.execute(query, (espid, servicename, ipaddr, status, topic, filename))

    dbconn.commit()
    cursor.close()


def on_service_state_change(zeroconf, service_type, name, state_change):
    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            m = re.search('^esp8266-([0123456789abcdef]+)\.local\.$', info.server)
            espid = str(int(m.group(1), 16))
            servername = info.server
            ipaddr = socket.inet_ntoa(info.address)
            # print("%s %s %s" % (espid, servername, ipaddr))
            update_device(espid, servername, ipaddr, "Online")


def browse_zeroconf():
    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf, "_arduino._tcp.local.", handlers=[on_service_state_change])
    sleep(3)
    browser.cancel()
    zeroconf.close()


def display_devicetable():
    global dbconn
    cursor = dbconn.cursor()
    query = "Select id, servicename, ipaddr, topic, configfile, status, last_seen from device order by id"
    cursor.execute(query)

    print("<html>\n<head>")
    print("<link rel=\"stylesheet\" type=\"text/css\" href=\"espstyle.css\">")
    print("</head>")
    print("<body>\n<table>")
    print("<tr>\n<th>ID</th><th>Service</th><th>IP Adresse</th><th>Topic</th>")
    print("<th>Status</th><th>Last Seen</th>\n</tr>")

    for (espid, servicename, ipaddr, topic, configfile, status, last_seen) in cursor:
        print("<tr>\n<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class=\"%s\">%s</td><td>%s</td>\n</tr>" % (espid, servicename, ipaddr, topic, status, status, last_seen))

    print("</table>\n</body>\n</html>")
    cursor.close()


#  Main
connect_db()
create_tables()
reset_devices()
browse_zeroconf()
display_devicetable()
dbconn.close()
