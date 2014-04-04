#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# manage-network.py -- manage libvirt network resources
#
# Copyright (C) 2014 Eric Sauer
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:  The above copyright notice and
# this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re, sys, uuid, subprocess, os
from lxml import etree
from optparse import OptionParser
from netaddr import *

IP_ADDRESS_MATCH='(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

### Possibly not needed?
parser = OptionParser()
parser.add_option("--name")
#parser.add_option("--new-uuid", action="store_true")
#parser.add_option("--device-path")
#parser.add_option("--mac-address")
(options, args) = parser.parse_args()

### Functions ###
# get_ips_available -- navigates virsh's net-xml tree for given network_name and grabs the network's address, and dhcp range. 
# 						Taking those, as well as any IPs already in use (see get_ips_in_use), it returns a list of available
#						ips for hosts.
def get_ips_available(network_name):
	network_xml = subprocess.check_output("sudo virsh net-dumpxml " + network_name, shell=True)
	networkTree = etree.fromstring(network_xml)
	ip_el = networkTree.xpath("/network/ip")[0]
	network_address, netmask = ip_el.get('address'), ip_el.get('netmask') # netmask may not be needed. cleanup if not
	range_el = networkTree.xpath("/network/ip/dhcp/range")[0]
	start = range_el.get('start')
	end = range_el.get('end')

	network = IPNetwork(network_address + "/24")
	print "Network: " + str(network)
	dhcp_range = IPRange(start, end)

	available_set = IPSet(network.iter_hosts())
	available_set.remove(IPAddress(network_address))
	available_set.remove(dhcp_range)
	used_set = get_ips_in_use()
	available_set = available_set - used_set

	return available_set

# get_ips_in_use -- scans /etc/hosts file to see what IPs are already taken.
def get_ips_in_use():
	with open('/etc/hosts', 'r') as content_file:
		content = content_file.read()

	ip_re = re.compile(r"%s"%IP_ADDRESS_MATCH)
	in_use_list = ip_re.findall(content)

	used_set = IPSet(in_use_list)
	return used_set

def get_network_name(domain_tree):
	mac_el = domain_tree.xpath("/domain/devices/interface[@type='network']/source")[0]
	network_name = mac_el.get('network')
	return network_name

def get_next_available(network_name):
	return list(get_ips_available(network_name))[0]

def register_next_ip(network_name, vm_name):
	ip = get_next_available(network_name)
	message = os.system("./ip.sh add %s %s" % (ip,vm_name))
	print "Registering IP: %s" % ip
	return message == 0, message

def deregister_ip(network_name, ip):
	
	return False

domain_tree = etree.parse(sys.stdin)
    
network_name = get_network_name(domain_tree)

#ips = get_ips_available(network_name)
#next_ip = get_next_available(network_name)
result, message = register_next_ip (network_name, options.name)
if result is False:
	print "There was an error. \n" + message
else:
	print "Success!"

#print("Available IPs: " + str(ips))
#print("Next Available: " + str(next_ip))