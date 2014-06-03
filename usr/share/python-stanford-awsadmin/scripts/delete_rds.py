#!/usr/bin/env python
#
# Copyright 2013
#         The Board of Trustees of the Leland Stanford Junior University

"""Delete a RDS instance

This script deletes a RDS instance in AWS.

Options:
        -i / --db-identifier=<value>
            RDS instance to delete.
        -s / --skip-final-snapshot
            Do do final snapshot. Otherwise, a final snapshot will be taken.
        -h / --help
            Print this message and exit.
                
"""

__author__ = 'sfeng@stanford.edu'

import sys
import getopt
import time
import string
import random
import re
import commands
import datetime

import paths
import awsadmin_cfg

def short_desc():
    return "Deletes a RDS instance."

def main(*args):
    """ Delete AWS RDS instance
    """
    # Parse command line options
    try:
        opts, args = getopt.getopt(args, 'hsi:', ['help', 
                     '--skip-final-snapshot', 'db-identifier='])
    except getopt.error, msg:
        print msg
        sys.exit(1)

    db_identifier = ''
    skip_final_snapshot = False

    # Process options
    for option, arg in opts:
        if option in ('-i', '--db_identifier'):
            db_identifier=(arg)
        elif option in ('-s', '--skip-final_snapshot'):
            skip_final_snapshot = True
        elif option in ('-h', '--help'):
            print __doc__
            sys.exit(0)

    if not db_identifier:
        sys.exit("RDS instance number is required.")

    if skip_final_snapshot:
        cmd = 'aws rds delete-db-instance ' + \
          ' --db-instance-identifier ' + db_identifier + \
          ' --skip-final-snapshot' 
    else:
        now = datetime.datetime.now()
        final_snapshot_id = db_identifier + 'snapshot-' + \
                        now.strftime("%Y%-m-%d-%H-M")
        cmd = 'aws rds delete-db-instance ' + \
          ' --db-instance-identifier ' + db_identifier + \
          ' --final-db-snapshot-identifier ' + final_snapshot_id 

    (status,output) = commands.getstatusoutput(cmd)
    if status != 0:
        print "ERROR in deleting " + db_identifier 
        print output
        sys.exit(1)
    else:
        print output
        sys.exit(0)
    
# Only execute the code when it's called as a script, not just imported.
if __name__ == '__main__':
    main(*sys.argv[1:])
