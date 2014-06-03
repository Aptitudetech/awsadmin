#!/usr/bin/env python
#
# Copyright 2014
#         The Board of Trustees of the Leland Stanford Junior University

"""Describe load balancer

This script describes a load-balancer.

Options:
         -n, --name=<value>
           load-balancer name.
         -h / --help
            Print this message and exit
                
"""

__author__ = 'sfeng@stanford.edu'

import sys
import getopt
import time
import string
import random
import re
import commands
import json

import paths
import awsadmin_cfg
import ConfigParser
from lib.Utils import sys_exit

def short_desc():
    return "Describes a load-balancer."

def my_print(data):
    elb_data = json.loads(data)
    groups =  elb_data["LoadBalancerDescriptions"]
    for group in groups:
        for i in ('LoadBalancerName','CreatedTime','AvailabilityZones',
                     'Instances'):
            if i is 'Instances':
                instances = group['Instances']
                for inst in instances:
                    for k,v in inst.items():
                        print '{0:23s}: {1:20s}'.format(k, v)
            elif i is 'AvailabilityZones':
               for z in group['AvailabilityZones']:
                   print '{0:23s}: {1:20s}'.format(i, z)
            else:
               print '{0:23s}: {1:20s}'.format(i, group[i])

def main(*args):
    """ Print a load-balancer's information
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hn:', ['help','name='] )
    except getopt.error, msg:
        sys_exit(1, msg)

    name=''
    instances = False
    # Process options
    for option, arg in opts:
        if option in ('-n', '--name'):
            name=(arg)
        elif option in ('-h', '--help'):
            sys_exit(0,__doc__)

    if not name:
        print "load balancer name is required."
        sys.exit(1)
  
    # Get load-balancer information
    elb_cmd = 'aws elb describe-load-balancers'
    exec_cmd = ' '.join([elb_cmd,'--load-balancer-name',name,
                       '--output json'])

    (status,output) = commands.getstatusoutput(exec_cmd)
    if status != 0:
        print output
        sys.exit(1)

    my_print(output)
    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
