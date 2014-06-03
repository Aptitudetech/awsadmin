#!/usr/bin/env python
#
# Copyright 2014
#         The Board of Trustees of the Leland Stanford Junior University

"""Describe EC2.
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
import argparse
import ConfigParser
from lib.Utils import sys_exit

def short_desc():
    return "Describes the given EC2 information."

def main(*args):
    """ Describe EC2
    """
    # Parse command line options
    parser = argparse.ArgumentParser(description='Describe EC2')
    parser.add_argument('-i', '--instance_id', action="store", required=True)

    args, unknown = parser.parse_known_args()
    instance_id = args.instance_id

    as_cmd = ' '.join(['admin-ec2 instance details', instance_id])

    (status,output) = commands.getstatusoutput(as_cmd)
   
    if status != 0:
        print "ERROR in verifing ASG"
        sys.exit(1)
    else:
        print output

    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
