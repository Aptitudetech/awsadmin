# -*- python -*-

# Copyright (C) 2013, Stanford University

"""Utility modules""" 

import os
import sys
import re
import commands
import json
from random import random
import argparse

import paths
import awsadmin_cfg

def add_tag(type, resource_name,instancekey,value):

    tag = 'key=' + instancekey + ',' + 'value=' + value

    if type == 'ec2':
        subcmd = 'create-tags --resources='
    elif type == 'rds':
        subcmd = 'add-tags-to-resource --resource-name='
    else:
        print "Unsupported type: " + type

    cmd = 'aws ' + type + ' ' + subcmd + resource_name + \
           ' --tags ' + tag

    (status, output) = commands.getstatusoutput(cmd)
    return (status, output)

def list_tags(type, resource_name):

    if type == 'ec2':
        subcmd = 'describe-tags --filters Name=resource-id,Values=' + resource_name
    elif type == 'rds':
        subcmd = 'list-tags-for-resource --resource-name=' + resource_name
    else:
        print "Unsupported type: " + type

    cmd = ' '.join(['aws',type,subcmd])

    (status, output) = commands.getstatusoutput(cmd)
    return (status, output)

def sys_exit(code, msg=''):
    if code:
            fd = sys.stderr
    else:
            fd = sys.stdout
    if msg:
            print >> fd, msg
    sys.exit(code)

def return_status(code, msg=''):
    if code:
        fd = sys.stderr
    else:
        fd = sys.stdout
    if msg:
        print >> fd, msg

    return code

def str2bool(v):
    """convert string 'yes' 'no' to boolean."""
    return v.lower() in ["yes", "true"]

def bool2str(v):
    """convert boolean to string."""
    if type(v) is bool:
        if v:
            return 'True'
        else:
            return 'False'
    elif v is None:
            return 'False'

    return v

def writefile(filename,line):
    """ Write to a file."""
    try:
        fp = open(filename, 'w')
        fp.write(line)
        fp.close()
    except IOError, e:
        sys_exit(2, e)
        
def readfile(filename):
    """Read from a file and return its content."""
    if filename == '-':
        fp = sys.stdin
        closep = 0
    else:
        fp = open(filename)
        closep = 1

    content = fp.read()
    if closep:
        fp.close()
    return content

def readlines(filename):
    """Read from a file and return list of lines."""
    if filename == '-':
        fp = sys.stdin
        closep = 0
    else:
        try:
            fp = open(filename)
            closep = 1
        except IOError, e:
            sys_exit(2,e)

    lines = fp.readlines()
    if closep:
        fp.close()
    return lines

def add_domain(addr,domain):
    """
    Take an address and add default domain if the address is not fully 
    qualified.
    """
    addr = addr.lower()
    at_sign = addr.find('@')
    if at_sign < 1:
        addr  = addr + '@' + domain

    return addr

def remove_domain(addr):
    """
    Take an address and remove domain if it exists. Return userid.
    """
    addr = addr.lower()
    at_sign = addr.find('@')
    if at_sign < 1:
        return addr
    else:
        return addr[:at_sign]

def parse_email(addr):
    """
    Takes an email address, and returns a tuple containing (user,host).

    """
    at_sign = addr.find('@')
    if at_sign < 1:
        return addr, gdata_cfg.DOMAIN
    
    return addr[:at_sign], addr[at_sign+1:]

def setenvs():
 
    for k,v in awsadmin_cfg.ENVARS.items():
        os.environ[k] = v

def config_option():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--config_name', action="store")
    parser.add_argument('-c', action="store")
