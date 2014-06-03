#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Describe a RDS instance

This script retrieve a RDS instance information

Options:
         -i / --db-identifier=<value>
             If no value is given, all instances are returned.
         -v / --verbose
             Print out all information for the instance.
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

def main(*args):
    """ Retrieve RDS instance information."
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hvi:', ['help', 'verbose',
        'db-identifier='])
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
        cmd = 'aws rds describe-db-instances ' + \
          ' --db-instance-identifier ' + db_identifier
    else:
        cmd = 'aws rds describe-db-instances'

    output_list = commands.getoutput(cmd)
    if verbose:
        print json.loads(output_list)
    else:
        json_output = json.loads(output_list)
        for db in json_output['DBInstances']:
            print "RDS identifier: %s " % db['DBInstanceIdentifier']
            print "RDS status: %s" % db['DBInstanceStatus'] 
            if db['DBInstanceStatus'] != 'creating':
                print "RDS public address: %s " % db['Endpoint']['Address']
            print

    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
