# -- ip.py -- #
# This is a unit test of the ip.sh script

import unittest, subprocess, re, os, shutil, random

class IPTests(unittest.TestCase):

	def setUp(self):
		# Make backup of current /etc/hosts file to ./tmp
		shutil.copyfile('/etc/hosts', '/tmp/hosts')
		self.IP_AVAILABLE = "244.244.244.244"
		self.IP_UNAVAILABLE = "127.0.0.1"

	def strip_chars(self, string):
		characters = ['\n']
		for char in characters:
			# strip all special characters from string
			string = re.sub(re.escape(char), '', string)
		return string

	def random_ip(self):
		return "%s.%s.%s.%s" % (random.randint(0,254), random.randint(0,254), random.randint(0,254), random.randint(0,254))

	def testIsAvailableSucceeds(self):
		message = subprocess.check_output(["./ip.sh", "is_available", self.IP_AVAILABLE, "testIsAvailableSucceeds"], stderr=subprocess.STDOUT)
		self.assertEqual(self.strip_chars(message), "true")

	def testIsAvailableFails(self):
		#print "Current directory: %s" % subprocess.check_output("pwd")
		message = subprocess.check_output(["./ip.sh", "is_available", self.IP_UNAVAILABLE, "localhost"], stderr=subprocess.STDOUT)
		self.assertEqual(self.strip_chars(message), "false")

	def testAddSucceeds(self):
		try:
			message = subprocess.check_output(["./ip.sh", "add", self.IP_AVAILABLE, "testAddSucceeds"], stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError, e:
			message = e.output
		self.assertEqual(self.strip_chars(message), "true")

	def testAddFails(self):
		ip = self.random_ip()
		# Register an IP/Host. This should succceed
		try:
			message1 = subprocess.check_output(["./ip.sh", "add", ip, "testAddFails1"], stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError, e:
			message1 = e.output
		self.assertEqual(self.strip_chars(message1), "true")
		
		# Try to register the IP again. This should not succeed
		try:
			message2 = subprocess.check_output(["./ip.sh", "add", ip, "testAddFails2"], stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError, e:
			message2 = e.output
		self.assertNotEqual(self.strip_chars(message2), "true")

		# Try to register the Host again. This should not succeed
		try:
			message3 = subprocess.check_output(["./ip.sh", "add", self.random_ip(), "testAddFails1"], stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError, e:
			message3 = e.output
		self.assertNotEqual(self.strip_chars(message3), "true")

	#TODO: def testRemoveSucceeds(self):
	

	def tearDown(self):
		# Need to restpre the original /etc/hosts file
		print subprocess.check_output(["sudo", "mv", "/tmp/hosts", "/etc/hosts"], stderr=subprocess.STDOUT)


def main():
    unittest.main()

if __name__ == '__main__':
    main()