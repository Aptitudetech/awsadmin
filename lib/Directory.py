# -*- python -*-
#
# Copyright 2011
#     The Board of Trustees of the Leland Stanford Junior University

'''
Created on May 22, 2011

@author: sfeng@stanford.edu
'''

"""Utility modules""" 

import os
import sys
import re
import ldap, ldap.sasl

import paths
import gdata_cfg

def sys_exit(code, msg=''):
    if code:
        fd = sys.stderr
    else:
        fd = sys.stdout
    if msg:
        print >> fd, msg
    sys.exit(code)

def is_valid_id(username):
    """Test if the id is a valid sunetid."""
    filter = 'uid=' + username
    return directory_query(filter,['uid'],gdata_cfg.SEARCH_PATH_PPL)

def is_active(username):
    """Test if the id is an active account by checking suEmailStatus."""
    filter = 'uid=' + username
    status = directory_query(filter,['suEmailStatus'],gdata_cfg.SEARCH_PATH_ACCT)
    if status and status.pop() == 'active':
        return True
    return False
  
def directory_query(filter,attrs,searchpath,rawdata=False):
    """Performs a search using specified attributes with the given filter."""

    ldapserver = gdata_cfg.LDAP_SERVER
    os.environ['KRB5CCNAME'] = gdata_cfg.MAIL_KRB5CCNAME

    server = ldap.initialize("ldap://" + ldapserver)
    server.sasl_interactive_bind_s("", ldap.sasl.gssapi(""))
    result = server.search_s(searchpath, ldap.SCOPE_SUBTREE,filter,attrs)

    # Return key/value and entries to the caller to parse
    if rawdata:
        return result

    values = []
    if len(result) > 0:
        """
        'result' is a list of tuplets with two items. The first item is the dn 
         string, the
        second is a dictionary, in which the keys are the search attributes, the value is a 
        list of value(s). For example:

        [('suRegID=869648f8f61311d2ae662436000baa77,cn=people,dc=stanford,dc=edu', 
        {'suDisplayNameFirst': ['Xueshan'], 'suDisplayNameLast': ['Feng']})]
 
        """
        valtuplets = result.pop()
        valdict = valtuplets[1]
        for k,v in valdict.iteritems():
            for i in v:
                values.append(i)
             
        """Return a list object with values, maybe empty."""
    return values

def get_gsb_aliases_tree(email,find,ret):

    """
    Given an email, search the GSB aliases tree to find anything with the
    sumaildrop set to that entry, and return all mail values.  Pulled out into
    its own function because we potentially have to do this twice.
    """

    attributes = [ ret ]
    filter = find + '=' + email
    aliases = []
    rawdata = True
    entries = directory_query(filter,attributes,gdata_cfg.SEARCH_PATH_GSBALIAS,rawdata)
    for entry in entries:
        valdict = entry[1]
        for k,v in valdict.iteritems():
            for i in v:
                j = i.lower()
                if j.find('gsb') == 0:
                    continue  # Skip mail with prefix GSB

                aliases.append(i)
    
    return aliases

# Given a GSB user, look up and return all email aliases for
# the users in LDAP.
def get_gsb_aliases(sunetid):

    aliases = {}
    email = ''
    attributes = [ 'sumaildrop' ]
    filter = 'uid=' + sunetid
    results = directory_query(filter,attributes,gdata_cfg.SEARCH_PATH_ACCT)

    for r in results:    
        if r.find('@zm') > 0 or r.find('vacation') > 0:
            continue
        else:
            email = r

    if not email:
        # No sumaildrop, other than possible zimbra and vacation
        return []

    aliases[email] = 1;
    drop = get_gsb_aliases_tree(email,'mail','sumaildrop');

    if not drop:
        # did not find sumaildrop in GSB tree
        return []
    
    aliases[drop[0]] = 1;
    doit = True;
    while doit:
        doit = False
        for email in aliases.keys():
            if aliases[email] == 0:
                continue
            aliases[email] = 0
            
            for newalias in get_gsb_aliases_tree(email,'sumaildrop','mail'):
                if newalias not in aliases:
                    doit = True
                    aliases[newalias] = 1

                drop = get_gsb_aliases_tree(newalias, 'mail','sumaildrop')
                if drop[0] not in aliases:
                    doit = True
                    aliases[drop[0]] = 1

    return aliases.keys()
