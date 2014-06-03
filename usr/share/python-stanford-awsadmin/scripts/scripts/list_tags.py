#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""List resource tags.

This script list tags for ec2 or rds instances.

Options:
         -i / --identifier=<value>
             instance identifier.
         -t / --type
             instance type, e.g. ec2, rds
         -h / --help
            Print this message and exit
                
"""

__author__ = 'sfeng@stanford.edu'

import sys
import getopt
import json
import string
import random
import re
import commands
import pprint

import paths
import awsadmin_cfg
from lib.Utils import list_tags

def short_desc():
    return "list tags for an AWS instance."

def main(*args):
    """ List tags for an AWS instance
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hi:t:c:p:', ['help', 
        'identifier=', 'type='])
    except getopt.error, msg:
        print msg
        sys.exit(1)

    # Default values
    identifier = type = ''

    # Process options
    for option, arg in opts:
        if option in ('-i', '--identifier'):
            identifier=arg
        if option in ('-t', '--type'):
            type=arg
        elif option in ('-h', '--help'):
            print __doc__
            sys.exit(0)

    if not identifier:
        print "identifier is required."
        sys.exit(1)

    if not type or type not in ('ec2', 'rds'):
        print "dentifier is required. Please select ec2 or rds."
        sys.exit(1)

    
    resource_name = identifier
    if type == 'rds':
        resource_name = awsadmin_cfg.RDS_ARN + identifier
        taglist = 'TagList'
    elif type == 'ec2':
        resource_name = identifier
        taglist = 'Tags'

    (status,output) = list_tags(type, resource_name)

    if status != 0:
       print "ERROR in listing tags."
       print resource_name
       print output
       sys.exit(1) 
    else:
        #list = json.dumps(json.loads(output)[taglist])
        for i in json.loads(output)[taglist]:
            for k,v in i.items():
                if k == 'Key':
                    print i[k],":",
                elif k == 'Value':
                    print i[k]
                else:
                    print k,":",v
    sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
