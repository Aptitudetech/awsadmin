#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Create a new mysql rds database

This script creates a new db instance in AWS.

Options:
         --db-identifier=<value>
         --allocated-storage=<value>
         --db-class=<value>
         --engine=<value>
         --mysql-username=<value>
         --mysql-user-password=<value>
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
    return "Create a new RDS instance identifier."

def main(*args):
    """ Create AWS RDS instance
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hi:s:c:u:p:', ['help', 
        'db-identifier=', 'allocated-storage=', 'db-class=',
        '--mysql-username=', '--mysql-user-password='])
    except getopt.error, msg:
        sys_exit(1, msg)

    # Default values
    random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(15))
    db_identifier = awsadmin_cfg.RDS_PREFIX + random_str
    db_class = awsadmin_cfg.RDS_CLASSES[0]
    db_storage = awsadmin_cfg.RDS_STORAGE
    db_engine  = awsadmin_cfg.RDS_ENGINE
    db_mysql_username = awsadmin_cfg.RDS_ADMIN
    db_maintenance_window = awsadmin_cfg.RDS_MAINTENANCE_WINDOW
    db_mysql_username=awsadmin_cfg.RDS_ADMIN

    db_mysql_userpassword = ''

    # Process options
    for option, arg in opts:
        if option in ('-i', '--db_identifier'):
            db_identifier=(arg)
        elif option in ('-s','--db_storage'):
            db_storage = arg
        elif option in ('-u', '--db_mysql_username'):
            db_mysql_username = arg
        elif option in ('-p', '--db_mysql_userpassword'):
            print arg
            db_mysql_userpassword = arg
            print db_mysql_userpassword
        elif option in ('-h', '--help'):
            sys_exit(0,__doc__)

    if not db_mysql_userpassword: 
        db_mysql_userpassword=awsadmin_cfg.RDS_ADMIN_PASSWORD

    cmd = ' '.join(['aws rds create-db-instance',
                   '--db-instance-identifier',db_identifier,
                   '--allocated-storage',db_storage,
                   '--db-instance-class',db_class,
                   '--engine',db_engine,'--master-username',db_mysql_username,
                   '--preferred-maintenance-window',db_maintenance_window,
                   '--master-user-password',db_mysql_userpassword])

    (status,output) = commands.getstatusoutput(cmd)
    if status != 0:
        print "ERROR in creating " + db_identifier 
        print output
        sys.exit(1)
    else:
        cmd = ' '.join(['aws rds describe-db-instances',
                        '--db-instance-identifier', db_identifier])
        (status,output) = commands.getstatusoutput(cmd)
        print "Creating " + db_identifier + "..."
        print json.loads(output)['DBInstances']
        sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
