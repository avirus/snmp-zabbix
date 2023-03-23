snmp-zabbix
===========

Zabbix host xml from snmp network device creator

triggers and graphs will be created automatically for every interface/mem/cpu/vpn and so on

requires: pysnmp

usage: grant SNMP access (use snmp v2 with community string password, allow access from IP of zabbix server) then run tool from zabbix server

$ python3 snmp_zabbix.py ip file-name.xml

import xml into zabbix as a host, data will be gathered via SNMP

example: python3 snmp_zabbix.py 10.1.1.254 file.xml
