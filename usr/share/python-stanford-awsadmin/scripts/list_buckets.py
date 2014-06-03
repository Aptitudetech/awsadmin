#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Describe a RDS instance

This script retrieve s3 buckets information

Options:
         -b / --bucket=<value>
             Optional. Display a bucket information, or display all buckets 
             under the account if no value is given.
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
    return "List S3 buckets."

def main(*args):
    """ List S3 buckets."
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hvb:', ['help', 'verbose',
        'bucket='])
    except getopt.error, msg:
        print msg
        sys.exit(1)

    # Process options
    bucket = ''
    verbose = False
    for option, arg in opts:
        if option in ('-b', '--bucket'):
            bucket = arg.lower()
        elif option in ('-v', 'verbose'):
            verbose = True
        elif option in ('-h', '--help'):
            print __doc__
            sys.exit(0)

    cmd = 'aws s3 list-buckets' 
    output_list = commands.getoutput(cmd)

    owner_dict=json.loads(output_list)["Owner"]
    print json.dumps(owner_dict,indent=1)
    for b in json.loads(output_list)["Buckets"]:
        if not bucket:
            print(json.dumps(b,indent=1))
        elif b["Name"] == bucket:
            print(json.dumps(b,indent=1))
            sys.exit(0)

    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
