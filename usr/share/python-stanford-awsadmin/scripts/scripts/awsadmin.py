#!/usr/bin/python
#
# Copyright 2013
#     The Board of Trustees of the Leland Stanford Junior University

""" awsdmin wrapper to call various sub commands
Usage:
  awsadmin sub-cmd [sub-cmd options]: Invoke the command with its options
  awsadmin help                     : Show summary of all sub-commands
  awsadmin help sub-cmd             : Show sub-cmd usage; if sub-cmd not found, 
                                    print sub-cmds matching sub-cmd string 
"""

__author__ = 'sfeng@stanford.edu'

import os
import sys
import getopt
import traceback

import paths
from lib.Utils import sys_exit, setenvs

def generate_commands_list(command_dir, reg=''):
    cmds = []
    script_name =  os.path.basename(sys.argv[0]).replace('.py','')
    for file in os.listdir(command_dir):
        if file[-3:] == '.py':
            if script_name in 'awsadmin':
                cmds.append(file[:-3])
            elif script_name in file:
                cmds.append(file[:-3])
    cmds.sort()
    docstring = __doc__ + '\nCommands matching your query:\n\n'
    for cmd in cmds: 
        try:
            m = __import__(cmd)
            if reg:
                if reg in m.short_desc().lower() or reg in cmd.lower():
                    docstring += "%-20s %s" % (cmd.replace('_','-'), m.short_desc()) + '\n'
            else:
                docstring += "%-20s %s" % (cmd.replace('_','-'), m.short_desc()) + '\n'
        except StandardError,e:
            pass
            
    return docstring

def main():
    # Scripts directory for auto-generated help
    command_dir = paths.scripts
    try:
        opts, args = getopt.getopt(sys.argv[1:],'')
    except getopt.error, msg:
        sys_exit(1,msg)

    if not args:
        sys_exit(0, generate_commands_list(command_dir))
    
    cmd = ''
    if args[0] == 'help':
        if args[1:]:
            cmd = args[1].lower().replace('-','_').replace('.py','')

            # Skip a few python system modules
            if cmd not in ('user', 'calendar', 'resource'):
                try:
                    m = __import__(cmd)
                    sys_exit(0, m.__doc__)
                except StandardError:
                    pass
        sys_exit(0, generate_commands_list(command_dir, cmd))
    
    # Run a command
    (program, surfix) = os.path.splitext(args[0])
    cmd = program.replace('-','_') # so both '-' and '_' works.
    try:
        m = __import__(cmd)
        sys.stdout.flush()
        return m.main(*args[1:])
    except ImportError:
        sys_exit(1, "No such command.")
        sys_exit(0,__doc__)

    #except:
    #    print "Exception in user code:"
    #    print '-'*60
    #    traceback.print_exc(file=sys.stdout)
    #    print '-'*60

if __name__ == '__main__':
    setenvs()
    main()
