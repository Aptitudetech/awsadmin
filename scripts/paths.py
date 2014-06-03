#!/usr/bin/python

import os
import sys

# Change this to your installation path of awsadmin
prod = '/usr/lib/awsadmin'
dev  = os.path.abspath(__file__)
dev = os.path.dirname(dev)   #script
dev = os.path.dirname(dev)   #awsadmin
# print "DEV dir: " + dev
scripts = dev + '/scripts'
testdir = dev + '/test'
awscfg = '/etc/aws/'

# Paths to search for modules
sys.path.insert(0, testdir)
sys.path.insert(0, dev)
sys.path.insert(0, scripts)
sys.path.insert(0, awscfg)
sys.path.insert(0, prod)

# AWS configration
os.environ['AWS_CONFIG_FILE'] = '/etc/aws/awscli.config'
