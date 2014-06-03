#!/usr/bin/env python
#
# Copyright 2014
#     The Board of Trustees of the Leland Stanford Junior University

"""Manage auto-scaling group launch configurations.

Usage: launch_config_admin [options] <config name>

Options:
        -s / --show=<config_name|ALL>
          Show a specified launch configuration or all configuratios.
        -d / --delete=<config_name>
          Delete a specified launch configuration.
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
import argparse
import ConfigParser
from lib.Utils import sys_exit

def short_desc():
    return "Show or delete an auto-scaling group launch configuration."

def show_launch_config(lc_name):
    """ show an existing launch configuration or all configurations.
    """
    if lc_name == 'ALL':
        as_cmd = ' '.join(['as-describe-launch-configs'])
    else:
        as_cmd = ' '.join(['as-describe-launch-configs',lc_name])

    return commands.getstatusoutput(as_cmd)
    
def delete_launch_config(config_name):
    """ Delete an auto-scaling group launch configuration.
    """
    as_cmd = ' '.join(['as-delete-launch-config',config_name,'-f'])
    print "Deleting LC " + config_name
    return commands.getstatusoutput(as_cmd)

def main(*args):
    # Parse command line options
    parser = argparse.ArgumentParser(description='Auto Scale LC admin')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-l', '--launch_config', action="store", default='ALL')
    group.add_argument('-s', '--show', action="store_true",
                       help='show all launch configurations or the given LC')
    group.add_argument('-d', '--delete', action="store_true",
                        default=False, help='Delete LC')

    args, unknown = parser.parse_known_args()

    lc_name = args.launch_config
    delete = args.delete
    show = args.show

    if show: 
        (status,output) = show_launch_config(lc_name)
    elif delete:
        if lc_name == 'ALL':
            print "lc name is required."
            sys.exit(1)
        else:
            (status,output) = delete_launch_config(lc_name)

    print output
    if status != 0:
        print "ERROR in operation on " + lc_name
        sys.exit(1)

if __name__ == '__main__':
    main(*sys.argv[1:])

