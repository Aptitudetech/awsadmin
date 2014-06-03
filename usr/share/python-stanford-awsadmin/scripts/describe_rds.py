#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Describe a RDS instance

This script retrieve a RDS instance information

Options:
         -i / --db-identifier=<value>
            If no value is given, all instances are returned.
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
import pprint

import paths
import awsadmin_cfg

def short_desc():
    return "Retrieve RDS instance information."

def my_print(data):
    json_output = json.loads(data)
    filters = ['DBInstanceIdentifier','EngineVersion', 'AvailabilityZone',
               'DBInstanceClass','AllocatedStorage', 'AvailabilityZone',
               'DBInstanceStatus','DBName','MasterUsername',
               'Endpoint']

    for db in json_output['DBInstances']:
        for k in filters:
            if k == 'Endpoint':
                try:
                    port = db['Endpoint']['Port']
                    address = db['Endpoint']['Address']
                    print "ConnectionString: %s:%d" % (address,port)
                except KeyError, e:
                    pass
            else:
                try:
                    value = db[k]
                    print k,":",value
                except KeyError, e:
                    pass
        print

def main(*args):
    """ Retrieve RDS instance information."
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hi:', ['help','db-identifier='])
    except getopt.error, msg:
        sys_exit(1, msg)

    # Process options
    db_identifier = ''
    verbose = False
    for option, arg in opts:
        if option in ('-i', '--db_identifier'):
            db_identifier=(arg)
        elif option in ('-v', 'verbose'):
            verbose = True
        elif option in ('-h', '--help'):
            sys_exit(0,__doc__)

    if db_identifier:
        cmd = ' '.join(['aws rds describe-db-instances',
          '--db-instance-identifier',db_identifier])
    else:
        cmd = ' '.join(['aws rds describe-db-instances'])

    (status,output) = commands.getstatusoutput(cmd)
    if status != 0:
        print "ERROR in decribe db instance information"
        print output
        sys.exit(1)
    else:
        my_print(output)

    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
