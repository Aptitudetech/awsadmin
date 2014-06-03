#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Add an existing user to a group.

This script add a user to an AWS group.

Options:
         -u / --username=<value>
         -g / --groupname=<value>
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
    return "Create a new AWS user."

def main(*args):
    """ Create AWS a new AWS user
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hu:g:', ['help','username=','groupname='])
    except getopt.error, msg:
        print msg
        sys.exit(1)

    username = groupname = ''

    # Process options
    for option, arg in opts:
        if option in ('-u', '--username'):
            username = arg.lower()
            # Todo: check if it's a valid sunetid
            # Todo: check if the user exists in AWS
        elif option in ('-g', '--groupname'):
            groupname=arg
            # Todo: check if the group exists.
        elif option in ('-h', '--help'):
            sys_exit(0,__doc__)

    if not username or not groupname:
        print "Username and groupname are required."
        sys.exit(1)

    cmd = 'aws iam add-user-to-group  --user-name ' + username \
           + ' --group-name ' + groupname

    (status,output) = commands.getstatusoutput(cmd)

    status = 0
    if status != 0:
        print "ERROR in creating user " + username
        print output
        sys.exit(1)

    print username + " is added to " + groupname

    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
