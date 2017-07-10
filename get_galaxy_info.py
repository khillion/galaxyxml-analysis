#! /usr/bin/env python

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kenzo-hugo.hillion1@pasteur.fr
## Python version: 3.6.0
## Date : 11-28-2016

'''
This script aims to list informations on a given Galaxy instance.
'''

###########  Import  ###########

import os
import argparse
import sys
from bioblend import galaxy

###########  Constant(s)  ###########

MOTIF = "toolshed"

###########  Function(s)  ###########

def list_toolsheds_from_gi(gi):
    '''
    Print the list of different toolsheds used for installation
    on the Galaxy server
    '''
    dico_toolsheds = {}

    for tool in gi.tools.get_tools():
        if MOTIF in tool['id']:
            elements = tool['id'].split('/')
            # Save information in a dictionnary
            if not elements[0] in dico_toolsheds.keys():
                dico_toolsheds[elements[0]] = 1

    print ("\n----- Names of toolsheds used on " + gi.base_url)
    for toolshed in dico_toolsheds.keys():
        print (" --> " + toolshed)

def list_owners_from_gi(gi):
    '''
    Print the list of different owners of tools installed
    from toolshed(s) on the Galaxy server
    '''
    dico_owners = {}

    for tool in gi.tools.get_tools():
        if MOTIF in tool['id']:
            elements = tool['id'].split('/')
            # Save information in a dictionnary
            if not elements[2] in dico_owners.keys():
                dico_owners[elements[2]] = 0
            dico_owners[elements[2]] += 1

    print ("\n----- Names of owners from toolsheds used on " + gi.base_url)
    for owner in dico_owners.keys():
        print (" --> " + owner + ": " + str(dico_owners[owner]) + " tool(s)")

def list_tools_number(gi):
    '''
    Print number of tools from the Galaxy instance
    '''
    cpt_all = 0
    cpt_toolshed = 0

    for tool in gi.tools.get_tools():
        cpt_all += 1
        if MOTIF in tool['id']:
            cpt_toolshed += 1

    print ("\n----- Number of tools on " + gi.base_url)
    print ("Total number of tools: " + str(cpt_all) + ".")
    print ("Number of tools installed from a toolshed: " + str(cpt_toolshed) + ".")

###########  Main  ###########

if __name__ == "__main__":

    ## Parse arguments
    parser = argparse.ArgumentParser(description = 'List information about a Galaxy server')
    parser.add_argument('-g', '--galaxy', help='Galaxy server URL', required=True)
    parser.add_argument('-k', '--api_key', help='API key from Galaxy', required=True)
    parser.add_argument('-t', '--toolsheds', help='List toolsheds from which tools were installed',
                        action='store_true')
    parser.add_argument('-n', '--numbers', help='List numbers of tools installed on the galaxy server \
                        (with the number coming from toolshed(s))', action='store_true')
    parser.add_argument('-o', '--owners', help='List owners of tools coming from toolshed(s) installed \
                        on the galaxy server', action='store_true')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    galaxy_site = args.galaxy
    api_key = args.api_key
    list_toolsheds = args.toolsheds
    list_owners = args.owners
    list_numbers = args.numbers

    ## Extra tests for arguments
    '''
    Here is the part to perform the different test for the arguments
    '''

    ###########################################################

    gi = galaxy.GalaxyInstance(galaxy_site, api_key)

    if (list_numbers):
        list_tools_number(gi)

    if (list_toolsheds):
        list_toolsheds_from_gi(gi)

    if (list_owners):
        list_owners_from_gi(gi)
