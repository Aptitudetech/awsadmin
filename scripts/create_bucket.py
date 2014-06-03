#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Create a new mysql rds database

This script creates a new S3 bucket in AWS.

Options:
         -b / --bucket=<value>
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

def short_desc():
    return "Create a new S3 bucket."

def main(*args):
    """ Create AWS S3 bucket
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hb:', ['help','bucket='])
    except getopt.error, msg:
        print msg
        sys.exit(1)

    bucket = ''

    # Process options
    for option, arg in opts:
        if option in ('-b', '--bucket'):
            bucket = arg.lower()
            first_dot_sign = bucket.find('.')
            if first_dot_sign < 1: 
                bucket = bucket + '.' + awsadmin_cfg.DOMAIN
            print bucket
        elif option in ('-h', '--help'):
            sys_exit(0,__doc__)

    if not bucket:
        print "Bucket name is required. e.g. mylogs.stanford.edu."
        sys.exit(1)

    cmd = 'aws --region us-west-2 s3 create-bucket --bucket ' + bucket + \
          ' --create-bucket-configuration \'{"location_constraint":"us-west-2"}\''

    (status,output) = commands.getstatusoutput(cmd)
    
    if status != 0:
        print "ERROR in creating " + bucket
        print output
        sys.exit(1)
    else:
        print bucket + " is created."

    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
