snmp-zabbix
===========

Zabbix host xml from snmp network device creator

triggers and graphs will be created automatically for every interface/mem/cpu/vpn and so on



requires: snmp-tools and php-snmp

 

usage: grant SNMP access (use snmp without password, allow access by zabbix server IP) after then run tool from zabbix server

$ php snmp-zabbix.php ip file-name.xml

after then import this xml into zabbix as a host, data will be gathered via SNMP

 

example: php snmp-zabbix.php 10.2.3.254 file.xml
