#!/usr/bin/env python
#
# Copyright 2014
#         The Board of Trustees of the Leland Stanford Junior University

"""Deregister an ec2 image

This script deregister an ec2 image.

Options:
         -a, --ami-id=<value>
             AMI id to deregister
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
    return "Deregister an AMI."

def main(*args):
    """ Deregister an AWS AMI image
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'ha:', ['help','ami-id='] )
    except getopt.error, msg:
        sys_exit(1, msg)

    ami_id = ''
    # Process options
    for option, arg in opts:
        if option in ('-a', '--ami-id'):
            ami_id=(arg)
        elif option in ('-h', '--help'):
            sys_exit(0,__doc__)

    if not ami_id:
        sys_exit(1,"AMI Id is required.")

    aws_cmd = ' '.join(['aws ec2 deregister-image --image-id',ami_id])
    (status,output) = commands.getstatusoutput(aws_cmd)
    print output
    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
