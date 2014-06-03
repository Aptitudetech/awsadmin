#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Delete a S3 bucket

This script deletes a s3 bucket information

Options:
         -b / --bucket=<value>
             Optional. If no value is given, all instances are returned.
         -h / --help
            Print this message and exit
                
"""

__author__ = 'sfeng@stanford.edu'

import sys
import getopt
import time
import commands
import json

import paths
import awsadmin_cfg

def short_desc():
    return "Delete a S3 bucket."

def main(*args):
    """ Delete a S3 bucket."
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

    if not bucket:
        print "Bucket name is required."
        sys.exit(1)

    cmd = 'aws s3 delete-bucket --bucket ' + bucket
    (status,output) = commands.getstatusoutput(cmd)
    if status != 0:
        print "ERROR in deletig " + bucket
        print output
        sys.exit(status)
    else:
        print bucket + " is deleted."
    
    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
