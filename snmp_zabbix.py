import os
import sys
from pysnmp.hlapi import *
import logging
from sys import argv
from pysnmp.smi import builder, view, rfc1902, error
from pysnmp.entity.rfc3413.oneliner import cmdgen

logging.basicConfig(
    level=logging.DEBUG, filename="./log.txt",
    format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
)
logger = logging.getLogger("/tmp/log.txt")
deviceip = "192.168.1.2"
dstfile = "/tmp/host.xml"
snmp_community_string = "public"
snmp_port = 161
snmp_noresult = "No Such Object currently exists at this OID"
snmp_noresult2 = "No Such Instance currently exists at this OID"
if (2 > len(sys.argv)):
    print("usage " + sys.argv[0] + " ip-addr [dst-file.xml snmp-community-string snmp-port-num] \n")
    print("defaults: \n")
    print("dst-file = " + dstfile + "\n")
    print("snmp-community-string = " + snmp_community_string + "\n")
    print("snmp-port-num = " + str(snmp_port) + "\n")
    print("example: " + sys.argv[0] + "  " + deviceip + "  " + dstfile + "  " + snmp_community_string + " " + str(snmp_port) + "\n")
    print("example2: " + sys.argv[0] + "  " + deviceip + "\n")
    exit(1)
if (2 < len(sys.argv)):
    deviceip = argv[1]
    dstfile = argv[2]
    snmp_community_string = argv[3]
    snmp_port = int(argv[4])

system_items = [
    {"fname": "chassis temperature", "iname": "sys.temp", 'isdelta': 0, 'type': 3, 'units': "celcius",
     'MIB': "1.3.6.1.4.1.9.9.13.1.3.1.3.1", 'interval': 600},
    {'fname': "chassis serial", 'iname': "sys.serial", 'isdelta': 0, 'type': 4, 'units': "",
     'MIB': "1.3.6.1.4.1.25506.2.6.1.1.1.1.6.47", 'interval': 86400},
    {'fname': "system version", 'iname': "sys.ver", 'isdelta': 0, 'type': 4, 'units': "",
     'MIB': "1.3.6.1.2.1.1.1.0", 'interval': 86400},
    {'fname': "system uptime", 'iname': "sys.uptime", 'isdelta': 0, 'type': 3, 'units': "ticks",
     'MIB': "1.3.6.1.2.1.1.3.0", 'interval': 30},
    {'fname': "system cpu load", 'iname': "sys.cpu.avg1", 'isdelta': 0, 'type': 3, 'units': "percent",
     'MIB': "1.3.6.1.4.1.9.9.109.1.1.1.1.7.1", 'interval': 60},
    {'fname': "system free cpu ram", 'iname': "sys.ramfree.cpu", 'isdelta': 0, 'type': 3, 'units': "bytes",
     'MIB': "1.3.6.1.4.1.9.9.48.1.1.1.6.1", 'interval': 600},
    {'fname': "system used cpu ram", 'iname': "sys.ramused.cpu", 'isdelta': 0, 'type': 3, 'units': "bytes",
     'MIB': "1.3.6.1.4.1.9.9.48.1.1.1.5.1", 'interval': 600},
    {'fname': "system free io ram", 'iname': "sys.ramfree.io", 'isdelta': 0, 'type': 3, 'units': "bytes",
     'MIB': "1.3.6.1.4.1.9.9.48.1.1.1.6.2", 'interval': 600},
    {'fname': "system used io ram", 'iname': "sys.ramused.io", 'isdelta': 0, 'type': 3, 'units': "bytes",
     'MIB': "1.3.6.1.4.1.9.9.48.1.1.1.5.2", 'interval': 600}
]
network_items = [
    {'fname': "#ifnum# #ifname# description", 'iname': "net.descr.if#ifnum#", 'isdelta': 0, 'type': 4, 'units': "",
     'MIB': "1.3.6.1.2.1.31.1.1.1.18.#ifnum#", 'interval': 86400},
    {'fname': "#ifnum# #ifname# name", 'iname': "net.name.if#ifnum#", 'isdelta': 0, 'type': 4, 'units': "",
     'MIB': "1.3.6.1.2.1.31.1.1.1.1.#ifnum#", 'interval': 86400},
    {'fname': "#ifnum# #ifname# status", 'iname': "net.status.if#ifnum#", 'isdelta': 0, 'type': 4, 'units': "",
     'MIB': "1.3.6.1.2.1.2.2.1.8.#ifnum#", 'interval': 60},
    {'fname': "#ifnum# #ifname# configured status", 'iname': "net.astatus.if#ifnum#", 'isdelta': 0, 'type': 4,
     'units': "", 'MIB': "IF-MIB::ifAdminStatus.#ifnum#", 'interval': 86400},
    {'fname': "#ifnum# #ifname# traffic in Bps", 'iname': "net.in.if#ifnum#", 'isdelta': 1, 'type': 0,
     'units': "Bytesps", 'MIB': "IF-MIB::ifHCInOctets.#ifnum#", 'interval': 60},
    {'fname': "#ifnum# #ifname# traffic out Bps", 'iname': "net.out.if#ifnum#", 'isdelta': 1, 'type': 0,
     'units': "Bytesps", 'MIB': "IF-MIB::ifHCOutOctets.#ifnum#", 'interval': 60},
    {'fname': "#ifnum# #ifname# unicasts in pps", 'iname': "net.ucast.in.if#ifnum#", 'isdelta': 1, 'type': 0,
     'units': "pps", 'MIB': "IF-MIB::ifHCInUcastPkts.#ifnum#", 'interval': 3600},
    {'fname': "#ifnum# #ifname# unicasts out pps", 'iname': "net.ucast.out.if#ifnum#", 'isdelta': 1, 'type': 0,
     'units': "pps", 'MIB': "IF-MIB::ifHCOutUcastPkts.#ifnum#", 'interval': 3600},
    {'fname': "#ifnum# #ifname# multicasts in pps", 'iname': "net.mcast.in.if#ifnum#", 'isdelta': 1, 'type': 0,
     'units': "pps", 'MIB': "IF-MIB::ifHCInMulticastPkts.#ifnum#", 'interval': 3600},
    {'fname': "#ifnum# #ifname# multicasts out pps", 'iname': "net.mcast.out.if#ifnum#", 'isdelta': 1, 'type': 0,
     'units': "pps", 'MIB': "IF-MIB::ifHCOutMulticastPkts.#ifnum#", 'interval': 3600},
    {'fname': "#ifnum# #ifname# broadcasts in pps", 'iname': "net.bcast.in.if#ifnum#", 'isdelta': 1, 'type': 0,
     'units': "pps", 'MIB': "IF-MIB::ifInBroadcastPkts.#ifnum#", 'interval': 3600},
    {'fname': "#ifnum# #ifname# broadcasts out pps", 'iname': "net.bcast.out.if#ifnum#", 'isdelta': 1, 'type': 0,
     'units': "pps", 'MIB': "IF-MIB::ifOutBroadcastPkts.#ifnum#", 'interval': 3600},
    {'fname': "#ifnum# #ifname# errors in", 'iname': "net.errin.if#ifnum#", 'isdelta': 0, 'type': 0, 'units': "events",
     'MIB': "IF-MIB::ifInErrors.#ifnum#", 'interval': 60},
    {'fname': "#ifnum# #ifname# errors out", 'iname': "net.errout.if#ifnum#", 'isdelta': 0, 'type': 0,
     'units': "events", 'MIB': "IF-MIB::ifOutErrors.#ifnum#", 'interval': 60},
    {'fname': "#ifnum# #ifname# current speed", 'iname': "net.speed.if#ifnum#", 'isdelta': 0, 'type': 3,
     'units': "Mbps", 'MIB': "IF-MIB::ifHighSpeed.#ifnum#", 'interval': 60}
]
network_triggers = [
    {'name': "#ifnum# description changed", 'expr': "{#sysname#:net.descr.if#ifnum#.abschange(0)}#0",
     'dep': "net.descr.if#ifnum#", 'descr': "administrative description changed on interface #ifname# (#iftext#)",
     'sev': 1},
    {'name': "#ifnum# name changed", 'expr': "{#sysname#:net.name.if#ifnum#.abschange(0)}#0",
     'dep': "net.descr.if#ifnum#", 'descr': "interface name changed (this is bad) on interface #ifname# (#iftext#)",
     'sev': 5},
    {'name': "#ifnum# adminstatus changed", 'expr': "{#sysname#:net.astatus.if#ifnum#.abschange(0)}#0",
     'dep': "net.astatus.if#ifnum#",
     'descr': "administrative status (shutdown/up) changed on interface #ifname# (#iftext#)", 'sev': 4},
    {'name': "#ifnum# status changed", 'expr': "{#sysname#:net.status.if#ifnum#.abschange(0)}#0",
     'dep': "net.status.if#ifnum#", 'descr': "port status (up/down) changed on interface #ifname# (#iftext#)",
     'sev': 2},
    {'name': "#ifnum# link speed changed", 'expr': "{#sysname#:net.speed.if#ifnum#.abschange(0)}#0",
     'dep': "net.speed.if#ifnum#", 'descr': "link speed changed on interface #ifname# (#iftext#)", 'sev': 1}
]
network_graphs = [
    {'name': "#ifname# traffic (#iftext#)", 'item1': "#sysname#:net.in.if#ifnum#",
     'item2': "#sysname#:net.out.if#ifnum#"},
    {'name': "#ifname# unicasts (#iftext#)", 'item1': "#sysname#:net.ucast.in.if#ifnum#",
     'item2': "#sysname#:net.ucast.out.if#ifnum#"},
    {'name': "#ifname# multicasts (#iftext#)", 'item1': "#sysname#:net.mcast.in.if#ifnum#",
     'item2': "#sysname#:net.mcast.out.if#ifnum#"},
    {'name': "#ifname# bloadcasts (#iftext#)", 'item1': "#sysname#:net.bcast.in.if#ifnum#",
     'item2': "#sysname#:net.bcast.out.if#ifnum#"},
    {'name': "#ifname# errors (#iftext#)", 'item1': "#sysname#:net.errin.if#ifnum#",
     'item2': "#sysname#:net.errout.if#ifnum#"}
]
system_triggers = [
    {'name': "{HOSTNAME} system version changed", 'expr': "{#sysname#:sys.ver.abschange(0)}#0",
     'descr': "version changed. firmware update?", 'dep': "sys.ver", 'sev': 3},
    {'name': "{HOSTNAME} serial changed", 'expr': "{#sysname#:sys.serial.abschange(0)}#0",
     'descr': "version changed. hardware replaced?", 'dep': "sys.serial", 'sev': 3},
    {'name': "{HOSTNAME} rebooted", 'expr': "{#sysname#:sys.uptime.last(0)}&lt;4000000", 'descr': "hardware rebooted",
     'dep': "sys.uptime", 'sev': 5},
    {'name': "{HOSTNAME} offline", 'expr': "{#sysname#:sys.uptime.nodata(90)}=1", 'descr': "hardware offline",
     'dep': "sys.uptime", 'sev': 5},
    {'name': "{HOSTNAME} cpu overloaded", 'expr': "{#sysname#:sys.cpu.avg1.last(0)}&gt;90",
     'descr': "hardware cpu overloaded", 'dep': "sys.cpu.avg1", 'sev': 2},
    {'name': "{HOSTNAME} memory overloaded", 'expr': "{#sysname#:sys.ramfree.cpu.last(0)}&lt;100000",
     'descr': "hardware cpu memory overloaded", 'dep': "sys.ramfree.cpu", 'sev': 2}
]
system_graphs = [
    {'name': "cpuload {HOSTNAME}", 'item1': "#sysname#:sys.cpu.avg1"},
    {'name': "memload cpu {HOSTNAME}", 'item1': "#sysname#:sys.ramfree.cpu", 'item2': "#sysname#:sys.ramused.cpu"},
    {'name': "memload io {HOSTNAME}", 'item1': "#sysname#:sys.ramfree.io", 'item2': "#sysname#:sys.ramused.io"}
]


def tmpl_head():
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\t<zabbix_export version=\"1.0\" date=\"1.01.23\" time=\"19.26\">\n\t<hosts>"


def tmpl_header(sd, sysip):
    return "<host name=\"" + str(
        sd) + "\">\n\t<proxy_hostid>0</proxy_hostid>\n\t<useip>1</useip>\n\t<dns></dns>\n\t<ip>" + str(
        sysip) + "</ip>\n\t<port>10050</port>\n\t<status>0</status>\n\t<useipmi>0</useipmi>\n\t<ipmi_ip></ipmi_ip>\n\t<ipmi_port>623</ipmi_port>\n\t<ipmi_authtype>-1</ipmi_authtype>\n\t<ipmi_privilege>2</ipmi_privilege>\n\t<ipmi_username></ipmi_username>\n\t<ipmi_password></ipmi_password>\n\t<groups>\n\t\t<group>ptk</group>\n\t</groups>\n\t"


def tmpl_footer():
    return "\n\t<templates/>\n\t<macros/>\n\t</host>"


def tmpl_last():
    return "</hosts><dependencies/></zabbix_export>"


def tmpl_item(item_name, item_description, item_oid, item_units, item_vtype=0, item_isdelta=0, apptype="network",
              item_delay=180):
    #     global snmp_community_string;
    #     # vtype=4 --- text
    #     # vtype=0 --- float
    #     # vtype=3 --- integer
    #     # 1 --- character
    data = "<item type=\"4\" key=\"" + str(item_name) + "\" value_type=\"" + str(item_vtype) + "\">\n\t<description>" \
           + str(item_description) + "</description>\n\t<ipmi_sensor></ipmi_sensor>\n\t<delay>" + str(item_delay) \
           + "</delay>\n\t<history>90</history>\n\t<trends>365</trends>\n\t<status>0</status>\n\t<data_type>0</data_type>\n\t<units>" + str(
        item_units) \
           + "</units>\n\t<multiplier>0</multiplier>\n\t<delta>" + str(item_isdelta) \
           + "</delta>\n\t<formula>0</formula>\n\t<lastlogsize>0</lastlogsize>\n\t<logtimefmt></logtimefmt>\n\t<delay_flex></delay_flex>\n\t" \
           + "<authtype>0</authtype>\n\t<username></username>\n\t<password></password>\n\t<publickey></publickey>\n\t<privatekey></privatekey>\n\t" \
           + "<params></params>\n\t<trapper_hosts>localhost</trapper_hosts>\n\t<snmp_community>" + str(
        snmp_community_string) + "</snmp_community>\n\t<snmp_oid>" \
           + str(
        item_oid) + "</snmp_oid>\n\t<snmp_port>161</snmp_port>\n\t<snmpv3_securityname></snmpv3_securityname>\n\t<snmpv3_securitylevel>0</snmpv3_securitylevel>\n\t" \
           + "<snmpv3_authpassphrase></snmpv3_authpassphrase>\n\t<snmpv3_privpassphrase></snmpv3_privpassphrase>\n\t<applications>\n\t\t<application>" + str(
        apptype) \
           + "</application>\n\t</applications>\n\t</item>\n\t"
    return data


def str_replace(haystack, value, data):
    value = str(value)
    haystack = str(haystack)
    data = str(data)
    data = data.replace(haystack, value)
    return data


def my_preprocess(sometext, ifindex = Null, ifdesc = Null, iftext = Null):
    result = sometext
    if Null != ifindex:
        result = str_replace("#ifnum#", str(ifindex), result)
    if Null != ifdesc:
        result = str_replace("#ifname#", ifdesc, result)
    if Null != iftext:
        result = str_replace("#iftext#", iftext, result)
    result = str_replace("#sysname#", sysname, result)
    return result


def tmpl_trigger(trigger_description, trigger_expression, trigger_comment, trigger_priority=1):
    # priority 0-5
    data = "\n\t<trigger>\n\t<description>" + str(
        trigger_description) + "</description>\n\t<type>0</type>\n\t<expression>" \
           + str(trigger_expression) + "</expression>\n\t<url></url>\n\t<status>0</status>\n\t<priority>" + str(
        trigger_priority) \
           + "</priority>\n\t<comments>" + str(trigger_comment) + "</comments>\n\t</trigger>\n\t"
    return data


def tmpl_graph(graph_name, graph_element1, graph_element2=Null):
    data = "<graph name=\"" + str(
        graph_name) + "\" width=\"900\" height=\"200\">\n\t<ymin_type>0</ymin_type>\n\t<ymax_type>0</ymax_type>\n\t<ymin_item_key></ymin_item_key>\n\t<ymax_item_key></ymax_item_key>\n\t<show_work_period>1</show_work_period>\n\t<show_triggers>1</show_triggers>\n\t<graphtype>0</graphtype>\n\t<yaxismin>0.0000</yaxismin>\n\t<yaxismax>100.0000</yaxismax>\n\t<show_legend>0</show_legend>\n\t<show_3d>0</show_3d>\n\t<percent_left>0.0000</percent_left>\n\t<percent_right>0.0000</percent_right>\n\t<graph_elements>\n\t"
    data = str(data) + str("<graph_element item=\"" + str(
        graph_element1) + "\">\n            <drawtype>0</drawtype>\n            <sortorder>0</sortorder>\n            <color>00AA00</color>\n            <yaxisside>0</yaxisside>\n            <calc_fnc>2</calc_fnc>\n            <type>0</type>\n            <periods_cnt>5</periods_cnt>\n            </graph_element>\n            ")
    if Null != graph_element2:
        data = str(data) + str("<graph_element item=\"" + str(
            graph_element2) + "\">\n            <drawtype>0</drawtype>\n            <sortorder>1</sortorder>\n            <color>0000AA</color>\n            <yaxisside>0</yaxisside>\n            <calc_fnc>2</calc_fnc>\n            <type>0</type>\n            <periods_cnt>5</periods_cnt>\n            </graph_element>\n            ")
    data = str(data) + "</graph_elements></graph>"
    return data


def walksnmp(oid, lookupMib = True):
    res = {}
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData(snmp_community_string),
                              UdpTransportTarget((deviceip, snmp_port)),
                              ContextData(),
                              ObjectType(ObjectIdentity(oid)),
                              lexicographicMode=False, lookupMib=lookupMib):
        if errorIndication:
            print(errorIndication, file=sys.stderr)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'),
                  file=sys.stderr)
            break
        else:
            for varBind in varBinds:
                res[varBind[0].prettyPrint()] = varBind[1].prettyPrint()
    return res


def asksnmp(oid):
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(snmp_community_string),
        cmdgen.UdpTransportTarget((deviceip, snmp_port)),
        oid, lookupMib=True
    )
    for varBind in varBinds:
        res = varBind[1].prettyPrint()
    if res == snmp_noresult:
        return Null
    if res == snmp_noresult2:
        return Null
    return res

def mibcheck(mibname):
    if not ("::" in mibname):
        res = asksnmp(mibname)
        if res == Null:
            return Null
        return mibname
    mib0, mibt = mibname.split("::")
    mib1, mib2 = mibt.split(".")
    mibVar1 = rfc1902.ObjectIdentity(mib0, mib1, mib2).addAsn1MibSource('file:///usr/share/snmp',
                                                                          'http://mibs.snmplabs.com/asn1/@mib@')
    value = asksnmp(mibVar1)
    if Null != value:
        return mib0 + "::" + mib1 + "." + mib2
    mib1 = str_replace("HC", "", mib1)
    mibVar1 = rfc1902.ObjectIdentity(mib0, mib1, mib2).addAsn1MibSource('file:///usr/share/snmp',
                                                                          'http://mibs.snmplabs.com/asn1/@mib@')
    value = asksnmp(mibVar1)
    if Null == value:
        return Null
    return mib0 + "::" + mib1 + "." + mib2


fd = open(dstfile, 'w')
fd.write(tmpl_head())

items = ""
triggers = ""
graphs = ""
mibBuilder = builder.MibBuilder()
mibView = view.MibViewController(mibBuilder)
mibVar = rfc1902.ObjectIdentity('IF-MIB', 'ifIndex').addAsn1MibSource('file:///usr/share/snmp','http://mibs.snmplabs.com/asn1/@mib@')
ifarray = walksnmp(mibVar)
iffound = len(ifarray)
logger.debug("array: ")
logger.debug(str(ifarray))
logger.debug(str(iffound))
mibVar = rfc1902.ObjectIdentity('SNMPv2-MIB', 'sysName', 0).addAsn1MibSource('file:///usr/share/snmp','http://mibs.snmplabs.com/asn1/@mib@')
sysname = asksnmp(mibVar)
print("\n sysname: " + sysname)

fd.write(tmpl_header(sysname, deviceip))
for this_item in system_items:
    mib = this_item['MIB']
    itemname = this_item['iname']
    res = asksnmp(mib)
    if res != Null:
        items += tmpl_item(itemname, this_item['fname'], mib, this_item['units'], this_item['type'], this_item['isdelta'], "system", this_item['interval'])
        logger.debug("" + itemname + " " + res)
for this_item in system_triggers:
    triggers += my_preprocess(tmpl_trigger(this_item['name'], this_item['expr'], this_item['descr']))
for this_item in system_graphs:
    item1 = this_item['item1']
    dep1 = str_replace("#sysname#:", "", item1)
    dep2 = Null
    item2 = Null
    if "item2" in this_item:
        item2 = this_item["item2"]
        dep2 = str_replace("#sysname#:", "",  item2)
    if not (dep1 in items):
        continue
    if not (dep2 in items):
        continue
    graphs += my_preprocess(tmpl_graph(this_item['name'], item1, item2))
for iface, ifindex in ifarray.items():
    logger.debug(iface)
    logger.debug(ifindex)
    mibVar = rfc1902.ObjectIdentity('IF-MIB', 'ifName', ifindex).addAsn1MibSource('file:///usr/share/snmp',
                                                                          'http://mibs.snmplabs.com/asn1/@mib@')
    ifdesc = asksnmp(mibVar)
    logger.debug(ifdesc)
    mibVar = rfc1902.ObjectIdentity('IF-MIB', 'ifAlias', ifindex).addAsn1MibSource('file:///usr/share/snmp',
                                                                          'http://mibs.snmplabs.com/asn1/@mib@')
    iftext = asksnmp(mibVar)
    logger.debug(iftext)
    if Null == iftext:
        iftext = ifdesc
# skip cisco virtual interfaces
    if "Vi" in iftext:
        continue
    for this_item in network_items:
        mib = mibcheck(my_preprocess(this_item['MIB'], ifindex, ifdesc, iftext))
        if Null == mib:
            continue
        items += my_preprocess(tmpl_item(this_item['iname'], this_item['fname'], mib, this_item['units'], this_item['type'] ,this_item['isdelta'], "network", this_item['interval']), ifindex, ifdesc, iftext);
    for this_item in network_triggers:
        dep1 = my_preprocess(this_item['dep'], ifindex, ifdesc, iftext)
        if not (dep1 in items):
            continue
        triggers += my_preprocess(tmpl_trigger(this_item['name'], this_item['expr'], this_item['descr'], this_item['sev']), ifindex, ifdesc, iftext);
    for this_item in network_graphs:
        item1 = this_item["item1"]
        dep2 = Null
        item2 = Null
        dep1 = my_preprocess(str_replace("#sysname#:", "", item1), ifindex, ifdesc, iftext)
        if "item2" in this_item:
            item2 = this_item["item2"]
            dep2 = my_preprocess(str_replace("#sysname#:", "", item2), ifindex, ifdesc, iftext)
        if not (dep1 in items):
            continue
        if not (dep2 in items):
            continue
        graphs += my_preprocess(tmpl_graph(this_item['name'], item1, item2), ifindex, ifdesc, iftext)
fd.write("<items>" + str(items) + "</items>")
fd.write("<triggers>" + str(triggers) + "</triggers>")
fd.write("<graphs>" + str(graphs) + "</graphs>")
fd.write(tmpl_footer())
fd.close()
exit(0)

