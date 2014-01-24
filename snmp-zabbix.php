<?php
// $LastChangedBy: slavik $ $Rev: 310 $ $LastChangedDate: 2014-01-24 10:13:37 +0600 (Пт, 24 янв 2014) $
// $Id: snmp-zabbix.php 310 2014-01-24 04:13:37Z slavik $
if (3==$argc) {
$deviceip=$argv[1];
$dstfile=$argv[2];
$host_count=2;	
} else {
	$host_count=$argc;
	$dstfile="hosts.xml";
}

$snmp_community_string="public";
if ($argc<2) echo "\n single host mode: \nsnmp-zabbix.php ip filename.xml \n multihost mode: \nsnmp-zabbix.php ip1 ip2 ip3 ...\n";

$sys_items=array();
$net_items=array();
$net_triggers=array();
$net_graphs=array();
$sys_triggers=array();
// system items
$sys_items[]=array('fname'=>"chassis temperature", 'iname'=>"sys.temp", 'isdelta'=>0, 'type'=>3, 'units'=>"celcius", 'MIB'=>"1.3.6.1.4.1.9.9.13.1.3.1.3.1", 'interval'=>600);
$sys_items[]=array('fname'=>"chassis serial", 'iname'=>"sys.serial", 'isdelta'=>0, 'type'=>4, 'units'=>"", 'MIB'=>"SNMPv2-SMI::mib-2.47.1.1.1.1.2.1", 'interval'=>86400);
$sys_items[]=array('fname'=>"system version", 'iname'=>"sys.ver", 'isdelta'=>0, 'type'=>4, 'units'=>"", 'MIB'=>"SNMPv2-MIB::sysDescr.0", 'interval'=>86400);
$sys_items[]=array('fname'=>"system uptime", 'iname'=>"sys.uptime", 'isdelta'=>0, 'type'=>3, 'units'=>"ticks", 'MIB'=>".1.3.6.1.2.1.1.3.0", 'interval'=>30);
$sys_items[]=array('fname'=>"system cpu load", 'iname'=>"sys.cpu.avg1", 'isdelta'=>0, 'type'=>3, 'units'=>"percent", 'MIB'=>".1.3.6.1.4.1.9.9.109.1.1.1.1.7.1", 'interval'=>60);
$sys_items[]=array('fname'=>"system free cpu ram", 'iname'=>"sys.ramfree.cpu", 'isdelta'=>0, 'type'=>3, 'units'=>"bytes", 'MIB'=>"1.3.6.1.4.1.9.9.48.1.1.1.6.1", 'interval'=>600);
$sys_items[]=array('fname'=>"system used cpu ram", 'iname'=>"sys.ramused.cpu", 'isdelta'=>0, 'type'=>3, 'units'=>"bytes", 'MIB'=>"1.3.6.1.4.1.9.9.48.1.1.1.5.1", 'interval'=>600);
$sys_items[]=array('fname'=>"system free io ram", 'iname'=>"sys.ramfree.io", 'isdelta'=>0, 'type'=>3, 'units'=>"bytes", 'MIB'=> ".1.3.6.1.4.1.9.9.48.1.1.1.6.2", 'interval'=>600);
$sys_items[]=array('fname'=>"system used io ram", 'iname'=>"sys.ramused.io", 'isdelta'=>0, 'type'=>3, 'units'=>"bytes", 'MIB'=> ".1.3.6.1.4.1.9.9.48.1.1.1.5.2", 'interval'=>600);
// network items
$net_items[]=array('fname'=>"#ifnum# #ifname# description", 'iname'=>"net.descr.if#ifnum#", 'isdelta'=>0, 'type'=>4, 'units'=>"", 'MIB'=>"IF-MIB::ifAlias.#ifnum#", 'interval'=>86400);
$net_items[]=array('fname'=>"#ifnum# #ifname# name", 'iname'=>"net.name.if#ifnum#", 'isdelta'=>0, 'type'=>4, 'units'=>"", 'MIB'=>"IF-MIB::ifName.#ifnum#", 'interval'=>86400);
$net_items[]=array('fname'=>"#ifnum# #ifname# status", 'iname'=>"net.status.if#ifnum#", 'isdelta'=>0, 'type'=>4, 'units'=>"", 'MIB'=>"IF-MIB::ifOperStatus.#ifnum#", 'interval'=>60);
$net_items[]=array('fname'=>"#ifnum# #ifname# configured status", 'iname'=>"net.astatus.if#ifnum#", 'isdelta'=>0, 'type'=>4, 'units'=>"", 'MIB'=>"IF-MIB::ifAdminStatus.#ifnum#", 'interval'=>86400);
$net_items[]=array('fname'=>"#ifnum# #ifname# traffic in Bps", 'iname'=>"net.in.if#ifnum#", 'isdelta'=>1, 'type'=>0, 'units'=>"Bytesps", 'MIB'=>"IF-MIB::ifHCInOctets.#ifnum#", 'interval'=>60);
$net_items[]=array('fname'=>"#ifnum# #ifname# traffic out Bps", 'iname'=>"net.out.if#ifnum#", 'isdelta'=>1, 'type'=>0, 'units'=>"Bytesps", 'MIB'=>"IF-MIB::ifHCOutOctets.#ifnum#", 'interval'=>60);
$net_items[]=array('fname'=>"#ifnum# #ifname# unicasts in pps", 'iname'=>"net.ucast.in.if#ifnum#", 'isdelta'=>1, 'type'=>0, 'units'=>"pps", 'MIB'=>"IF-MIB::ifHCInUcastPkts.#ifnum#", 'interval'=>3600);
$net_items[]=array('fname'=>"#ifnum# #ifname# unicasts out pps", 'iname'=>"net.ucast.out.if#ifnum#", 'isdelta'=>1, 'type'=>0, 'units'=>"pps", 'MIB'=>"IF-MIB::ifHCOutUcastPkts.#ifnum#", 'interval'=>3600);
$net_items[]=array('fname'=>"#ifnum# #ifname# multicasts in pps",'iname'=>"net.mcast.in.if#ifnum#",'isdelta'=>1,'type'=>0,'units'=>"pps",'MIB'=>"IF-MIB::ifHCInMulticastPkts.#ifnum#", 'interval'=>3600);
$net_items[]=array('fname'=>"#ifnum# #ifname# multicasts out pps",'iname'=>"net.mcast.out.if#ifnum#",'isdelta'=>1,'type'=>0,'units'=>"pps",'MIB'=>"IF-MIB::ifHCOutMulticastPkts.#ifnum#", 'interval'=>3600);
$net_items[]=array('fname'=>"#ifnum# #ifname# broadcasts in pps",'iname'=>"net.bcast.in.if#ifnum#",'isdelta'=>1,'type'=>0,'units'=>"pps",'MIB'=>"IF-MIB::ifInBroadcastPkts.#ifnum#", 'interval'=>3600);
$net_items[]=array('fname'=>"#ifnum# #ifname# broadcasts out pps",'iname'=>"net.bcast.out.if#ifnum#",'isdelta'=>1,'type'=>0,'units'=>"pps",'MIB'=>"IF-MIB::ifOutBroadcastPkts.#ifnum#", 'interval'=>3600);
$net_items[]=array('fname'=>"#ifnum# #ifname# errors in",'iname'=>"net.errin.if#ifnum#",'isdelta'=>0,'type'=>0,'units'=>"events",'MIB'=>"IF-MIB::ifInErrors.#ifnum#", 'interval'=>60);
$net_items[]=array('fname'=>"#ifnum# #ifname# errors out",'iname'=>"net.errout.if#ifnum#",'isdelta'=>0,'type'=>0,'units'=>"events",'MIB'=>"IF-MIB::ifOutErrors.#ifnum#", 'interval'=>60);
//$net_items[]=array('fname'=>"#ifnum# #ifname# last change",'iname'=>"net.changed.if#ifnum#",'isdelta'=>0,'type'=>3,'units'=>"ticks",'MIB'=>"IF-MIB::ifLastChange.#ifnum#", 'interval'=>3600);
$net_items[]=array('fname'=>"#ifnum# #ifname# current speed",'iname'=>"net.speed.if#ifnum#",'isdelta'=>0,'type'=>3,'units'=>"Mbps",'MIB'=>"IF-MIB::ifHighSpeed.#ifnum#", 'interval'=>60);
// network triggers
$net_triggers[]=array('name'=>"#ifnum# description changed",'expr'=>"{#sysname#:net.descr.if#ifnum#.abschange(0)}#0",'dep'=>"net.descr.if#ifnum#",'descr'=>"administrative description changed on interface #ifname# (#iftext#)", 'sev'=>1);
$net_triggers[]=array('name'=>"#ifnum# name changed",'expr'=>"{#sysname#:net.name.if#ifnum#.abschange(0)}#0",'dep'=>"net.descr.if#ifnum#",'descr'=>"interface name changed (this is bad) on interface #ifname# (#iftext#)", 'sev'=>5);
$net_triggers[]=array('name'=>"#ifnum# adminstatus changed",'expr'=>"{#sysname#:net.astatus.if#ifnum#.abschange(0)}#0",'dep'=>"net.astatus.if#ifnum#",'descr'=>"administrative status (shutdown/up) changed on interface #ifname# (#iftext#)", 'sev'=>4);
$net_triggers[]=array('name'=>"#ifnum# status changed",'expr'=>"{#sysname#:net.status.if#ifnum#.abschange(0)}#0",'dep'=>"net.status.if#ifnum#",'descr'=>"port status (up/down) changed on interface #ifname# (#iftext#)", 'sev'=>2);
$net_triggers[]=array('name'=>"#ifnum# link speed changed",'expr'=>"{#sysname#:net.speed.if#ifnum#.abschange(0)}#0",'dep'=>"net.speed.if#ifnum#",'descr'=>"link speed changed on interface #ifname# (#iftext#)" , 'sev'=>1);
//$net_triggers[]=array('name'=>"#ifnum# change on #ifname# (#iftext#)",'expr'=>"{#sysname#:net.changed.if#ifnum#.last(0)}&lt;1000000",'dep'=>"net.changed.if#ifnum#",'descr'=>"interface #ifname# modified recently");
// network graphs
$net_graphs[]=array('name'=>"#ifname# traffic (#iftext#)",'item1'=>"#sysname#:net.in.if#ifnum#",'item2'=>"#sysname#:net.out.if#ifnum#");
$net_graphs[]=array('name'=>"#ifname# unicasts (#iftext#)",'item1'=>"#sysname#:net.ucast.in.if#ifnum#",'item2'=>"#sysname#:net.ucast.out.if#ifnum#");
$net_graphs[]=array('name'=>"#ifname# multicasts (#iftext#)",'item1'=>"#sysname#:net.mcast.in.if#ifnum#",'item2'=>"#sysname#:net.mcast.out.if#ifnum#");
$net_graphs[]=array('name'=>"#ifname# bloadcasts (#iftext#)",'item1'=>"#sysname#:net.bcast.in.if#ifnum#",'item2'=>"#sysname#:net.bcast.out.if#ifnum#");
$net_graphs[]=array('name'=>"#ifname# errors (#iftext#)",'item1'=>"#sysname#:net.errin.if#ifnum#",'item2'=>"#sysname#:net.errout.if#ifnum#");
// system triggers
$sys_triggers[]=array('name'=>"{HOSTNAME} system version changed",'expr'=>"{#sysname#:sys.ver.abschange(0)}#0",'descr'=>"version changed. firmware update?", 'dep'=>"sys.ver", 'sev'=>3);
$sys_triggers[]=array('name'=>"{HOSTNAME} serial changed",'expr'=>"{#sysname#:sys.serial.abschange(0)}#0",'descr'=>"version changed. hardware replaced?", 'dep'=>"sys.serial", 'sev'=>3);
$sys_triggers[]=array('name'=>"{HOSTNAME} rebooted",'expr'=>"{#sysname#:sys.uptime.last(0)}&lt;4000000",'descr'=>"hardware rebooted", 'dep'=>"sys.uptime", 'sev'=>5);
$sys_triggers[]=array('name'=>"{HOSTNAME} offline",'expr'=>"{#sysname#:sys.uptime.nodata(90)}=1",'descr'=>"hardware offline", 'dep'=>"sys.uptime", 'sev'=>5);
$sys_triggers[]=array('name'=>"{HOSTNAME} cpu overloaded",'expr'=>"{#sysname#:sys.cpu.avg1.last(0)}&gt;90",'descr'=>"hardware cpu overloaded", 'dep'=>"sys.cpu.avg1", 'sev'=>2);
$sys_triggers[]=array('name'=>"{HOSTNAME} memory overloaded",'expr'=>"{#sysname#:sys.ramfree.cpu.last(0)}&lt;100000",'descr'=>"hardware cpu memory overloaded", 'dep'=>"sys.ramfree.cpu", 'sev'=>2);
// system graphs
$sys_graphs[]=array('name'=>"cpuload {HOSTNAME}",'item1'=>"#sysname#:sys.cpu.avg1");
$sys_graphs[]=array('name'=>"memload cpu {HOSTNAME}",'item1'=>"#sysname#:sys.ramfree.cpu",'item2'=>"#sysname#:sys.ramused.cpu");
$sys_graphs[]=array('name'=>"memload io {HOSTNAME}",'item1'=>"#sysname#:sys.ramfree.io",'item2'=>"#sysname#:sys.ramused.io");

$fd = fopen($dstfile, 'w');
fwrite($fd, tmpl_head());

for ($hostnum=1;$hostnum<$host_count;$hostnum++)
// there is hostcycle
{
$items="";
$triggers="";
$graphs="";
if (2!=$host_count)  $deviceip=$argv[$hostnum];
//$iffound=(int)asksnmp("IF-MIB::ifNumber.0");
$ifarray=getifs();
$iffound=count($ifarray);
print_r($ifarray);
//exit;
$sysname=htmlspecialchars(asksnmp("SNMPv2-MIB::sysName.0"));
fwrite($fd, tmpl_header($sysname, $deviceip));

foreach ($sys_items as &$this_item) {
    if (NULL!=asksnmp($mib=$this_item['MIB'])) 
    	$items.=tmpl_item( $this_item['iname'], $this_item['fname'], $mib, $this_item['units'], $this_item['type'], $this_item['isdelta'], "system", $this_item['interval']);
}
unset($this_item); 

foreach ($sys_triggers as &$this_item) {
    if (false!==strpos($items, $this_item['dep']))
    	$triggers.=my_preprocess(tmpl_trigger($this_item['name'], $this_item['expr'], $this_item['descr']));
}
unset($this_item);

foreach ($sys_graphs as &$this_item) {
	 $dep1= substr($this_item['item1'], strpos($this_item['item1'], ":")+1);
	if (isset($this_item['item2'])) $dep2= substr($this_item['item2'], strpos($this_item['item2'], ":")+1);
    if (FALSE=== strpos($items, $dep1)) continue; 
    if (isset($dep2)) if (FALSE=== strpos($items, $dep2)) continue;
    if (isset($this_item['item2'])) $item2=$this_item['item2']; 
    else $item2=NULL;  
    $graphs.=my_preprocess(tmpl_graph($this_item['name'], $this_item['item1'], $item2)); 
}
unset($this_item);

//$iffound=0;
echo "$deviceip: count $iffound \n"; 
//fix: upload_max_filesize, post_max_size
for ($i=0; $i<$iffound;$i++){
	$ifindex=(int)str_replace("INTEGER:", "", $ifarray[$i]);
	//$ifindex=(int)asksnmp("IF-MIB::ifIndex.$i");
	//if (0==$ifindex) continue;
	$ifdesc=htmlspecialchars(asksnmp("IF-MIB::ifName.$ifindex"));
	$iftext=htmlspecialchars(asksnmp("IF-MIB::ifAlias.$ifindex"));
	if (NULL==$iftext) $iftext=$ifdesc;
	if (0==strlen($iftext)) $iftext=$ifdesc.$ifindex;
	
//skip cisco virtual interfaces	
	if (false!==strpos($ifdesc, "Vi")) continue;
	
foreach ($net_items as &$this_item) {
    if (NULL!=$mib=mcheck(my_preprocess($this_item['MIB']))) 
    	$items.=my_preprocess(tmpl_item( $this_item['iname'], $this_item['fname'], $mib, $this_item['units'], $this_item['type'], $this_item['isdelta'], "network", $this_item['interval']));
}
unset($this_item); 
foreach ($net_triggers as &$this_item) {
	  if (false!==strpos($items, my_preprocess($this_item['dep'])))
    	$triggers.=my_preprocess(tmpl_trigger($this_item['name'],$this_item['expr'], $this_item['descr'], $this_item['sev']));
}
unset($this_item); 

unset($this_item); 
foreach ($net_graphs as &$this_item) {
	 $dep1= my_preprocess( substr($this_item['item1'], strpos($this_item['item1'], ":")+1));
	if (isset($this_item['item2'])) $dep2=my_preprocess( substr($this_item['item2'], strpos($this_item['item2'], ":")+1));
	
    if (FALSE=== strpos($items, $dep1)) continue; 
    if (isset($dep2)) if (FALSE=== strpos($items, $dep2)) continue;
    $item2=$this_item['item2'];
    if (!isset($this_item['item2'])) $item2=NULL;  
	$graphs.=my_preprocess(tmpl_graph($this_item['name'], $this_item['item1'], $item2));
}
unset($this_item); 

	
	echo "$i, if.$ifindex $ifdesc \n";
}; 
fwrite($fd, "<items>$items</items>");
fwrite($fd, "<triggers>$triggers</triggers>");
fwrite($fd, "<graphs>$graphs</graphs>");
fwrite($fd, tmpl_footer());

}// end of hosts 
fwrite($fd, tmpl_last());

fclose($fd);
exit(0);

function tmpl_trigger($trigger_description, $trigger_expression, $trigger_comment, $trigger_priority=1)
{
	// priority 0-5
	$data="
	<trigger>
	<description>$trigger_description</description>
	<type>0</type>
	<expression>$trigger_expression</expression>
	<url></url>
	<status>0</status>
	<priority>$trigger_priority</priority>
	<comments>$trigger_comment</comments>
	</trigger>
	";
	return $data;
}

function tmpl_item($item_name, $item_description, $item_oid, $item_units, $item_vtype=0, $item_isdelta=0, $apptype="network", $item_delay=180)
{
	global $snmp_community_string;
	// vtype=4 --- text
	// vtype=0 --- float
	// vtype=3 --- integer
	// 1 --- character
	$data="<item type=\"4\" key=\"$item_name\" value_type=\"$item_vtype\">
	<description>$item_description</description>
	<ipmi_sensor></ipmi_sensor>
	<delay>$item_delay</delay>
	<history>90</history>
	<trends>365</trends>
	<status>0</status>
	<data_type>0</data_type>
	<units>$item_units</units>
	<multiplier>0</multiplier>
	<delta>$item_isdelta</delta>
	<formula>0</formula>
	<lastlogsize>0</lastlogsize>
	<logtimefmt></logtimefmt>
	<delay_flex></delay_flex>
	<authtype>0</authtype>
	<username></username>
	<password></password>
	<publickey></publickey>
	<privatekey></privatekey>
	<params></params>
	<trapper_hosts>localhost</trapper_hosts>
	<snmp_community>$snmp_community_string</snmp_community>
	<snmp_oid>$item_oid</snmp_oid>
	<snmp_port>161</snmp_port>
	<snmpv3_securityname></snmpv3_securityname>
	<snmpv3_securitylevel>0</snmpv3_securitylevel>
	<snmpv3_authpassphrase></snmpv3_authpassphrase>
	<snmpv3_privpassphrase></snmpv3_privpassphrase>
	<applications>
		<application>$apptype</application>
	</applications>
	</item>
	";
	return $data;
}

function tmpl_graph($graph_name, $graph_element1=NULL, $graph_element2=NULL)
{
	$data="<graph name=\"$graph_name\" width=\"900\" height=\"200\">
	<ymin_type>0</ymin_type>
	<ymax_type>0</ymax_type>
	<ymin_item_key></ymin_item_key>
	<ymax_item_key></ymax_item_key>
	<show_work_period>1</show_work_period>
	<show_triggers>1</show_triggers>
	<graphtype>0</graphtype>
	<yaxismin>0.0000</yaxismin>
	<yaxismax>100.0000</yaxismax>
	<show_legend>0</show_legend>
	<show_3d>0</show_3d>
	<percent_left>0.0000</percent_left>
	<percent_right>0.0000</percent_right>
	<graph_elements>
	";
            $data=$data."<graph_element item=\"$graph_element1\">
            <drawtype>0</drawtype>
            <sortorder>0</sortorder>
            <color>00AA00</color>
            <yaxisside>0</yaxisside>
            <calc_fnc>2</calc_fnc>
            <type>0</type>
            <periods_cnt>5</periods_cnt>
            </graph_element>
            ";                                                                                                                                          
            if (NULL!=$graph_element2) $data=$data."<graph_element item=\"$graph_element2\">
            <drawtype>0</drawtype>
            <sortorder>1</sortorder>
            <color>0000AA</color>
            <yaxisside>0</yaxisside>
            <calc_fnc>2</calc_fnc>
            <type>0</type>
            <periods_cnt>5</periods_cnt>
            </graph_element>
            ";
                                                                                                                                                      
          $data=$data."</graph_elements></graph>";
	return $data;
}

function tmpl_head()
{
	$data="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
	<zabbix_export version=\"1.0\" date=\"24.01.11\" time=\"19.26\">
	<hosts>";
		return $data;
}
function tmpl_header($sd, $sysip)
{
	$data="<host name=\"$sd\">
	<proxy_hostid>0</proxy_hostid>
	<useip>1</useip>
	<dns></dns>
	<ip>$sysip</ip>
	<port>10050</port>
	<status>0</status>
	<useipmi>0</useipmi>
	<ipmi_ip></ipmi_ip>
	<ipmi_port>623</ipmi_port>
	<ipmi_authtype>-1</ipmi_authtype>
	<ipmi_privilege>2</ipmi_privilege>
	<ipmi_username></ipmi_username>
	<ipmi_password></ipmi_password>
	<groups>
		<group>ptk</group>
	</groups>
	";
	return $data;
}

function tmpl_footer()
{
	$data="
	<templates/>
	<macros/>
	</host>";
	return $data;
}
function tmpl_last()
{	
	$data="</hosts><dependencies/></zabbix_export>";
	return $data;
}
function getifs()
{
	global $deviceip, $snmp_community_string;
	//$snmpcmd="snmpwalk -v 2c -c $snmp_community_string -O qv $deviceip";
	$result=snmpwalk("$deviceip", "$snmp_community_string", "IF-MIB::ifIndex");
	return $result;
}

function asksnmp($mibname)
{
	global $deviceip, $snmp_community_string;
	$snmpcmd="snmpget -v2c -c $snmp_community_string -Oqv $deviceip";
	$result=exec("$snmpcmd $mibname");
//	echo "$mibname %";
//	$result=@snmpget("$deviceip", "public", $mibname);
//	echo "$result#";
	//print_r($result); echo "\n";
	if (FALSE===$result) return NULL;
	if (FALSE!==strpos($result, "No Such Instance currently exists at this OID")) return NULL;
	if (FALSE!==strpos($result, "No Such Object available on this agent at this OID")) return NULL;
//	$result=substr(strstr("$result"," "),1);
//	echo "$result \n";
	//$result=(strpos($result, ":"))
	return $result;
}
function mcheck($mibname)
{
	$mib1=$mibname;
	if (NULL==$value=asksnmp($mib1)) if(NULL!=strstr($mib1, "HC"))	$value=asksnmp($mib1=str_replace("HC", "", $mib1));
	if (NULL==$value) $mib1=NULL;
	return $mib1;
}

function my_preprocess($sometext)
{
	global $ifindex, $iftext, $sysname,$ifdesc;
	$result=$sometext;
	if (isset($ifindex)) $result=str_replace("#ifnum#", $ifindex,$result);
	if (isset($ifdesc)) $result=str_replace("#ifname#", $ifdesc,$result);
	if (isset($iftext)) $result=str_replace("#iftext#", $iftext,$result);
	$result=str_replace("#sysname#", $sysname,$result);
	return $result;
}



?>