import hosts_mgr, select, sys
from optparse import OptionParser
from lxml import etree

### Possibly not needed?
parser = OptionParser()
parser.add_option("--name")
(options, args) = parser.parse_args()

if not (select.select([sys.stdin,],[],[],0.0)[0]):
	print "No argument passed."
	print "Usage: python ./get-ip.py < [path/to/base-domain.xml]"
	sys.exit()

domain_tree = etree.parse(sys.stdin)
    
network_name = hosts_mgr.get_network_name(domain_tree)

#ips = get_ips_available(network_name)
#next_ip = get_next_available(network_name)
ip, result, message = hosts_mgr.register_next_ip (network_name, options.name)
if result is False:
	print "There was an error. \n" + message
else:
	print "Success!"

	ip, result, message = hosts_mgr.deregister_ip (options.name, ip)
	if result is False:
		print "There was an error. \n" + message
	else:
		print "Success!"

print ip
#print("Available IPs: " + str(ips))
#print("Next Available: " + str(next_ip))