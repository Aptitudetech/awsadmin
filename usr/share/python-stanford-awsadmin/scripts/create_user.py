#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Create a new AWS user.

This script creates a new AWS user.

Options:
         -u / --username=<value>
         -p / --password=<value>
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
        opts, args = getopt.getopt(args, 'hu:p:', ['help','username=','password='])
    except getopt.error, msg:
        print msg
        sys.exit(1)

    username = password = ''

    # Process options
    for option, arg in opts:
        if option in ('-u', '--username'):
            username = arg.lower()
            # Todo: check if it's a valid sunetid
        elif option in ('-p', '--password'):
            password=arg
            # Todo: check if it's a good password
        elif option in ('-h', '--help'):
            sys_exit(0,__doc__)

    if not username or not password:
        print "Username and password are required."
        sys.exit(1)

    # Todo: check if the user already exist.

    #cmd = 'aws iam create-user --user-name ' + username

    #(status,output) = commands.getstatusoutput(cmd)

    status = 0
    if status != 0:
        print "ERROR in creating user " + username
        print output
        sys.exit(1)
    else:
        cmd = 'aws iam create-login-profile --user-name ' + username +  \
              ' --password ' + password
        (status,output) = commands.getstatusoutput(cmd)

    if status != 0:
        print "ERROR in setting password for " + username
        print output
        sys.exit(1)

    print username + " is created."

    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
