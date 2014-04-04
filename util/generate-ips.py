#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# generate vm network range

import random

# randomMAC() - method to generate a MAC address for Red Hat Virtualization guests
def randomMAC():
	mac = [ 0x00, 0x16, 0x3e,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac))

for num in range(110, 130+1):
    print("vm{0}\t192.168.122.{0}\t{1}".format(num, randomMAC()))
