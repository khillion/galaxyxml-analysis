#!/usr/bin/env python

"""
This script aims to clone repositories containing tools that are installed
in a given Galaxy instance. It only allows to get the last version of tools
that were installed from a toolshed.
"""

#  Import  #

import os
import argparse
import sys
from bioblend import galaxy
import hglib
import json

#  Constant(s)  #

MOTIF = "toolshed"
REPORT = "download_report.json"

#  Main  #

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Clone repositories containing tools that\
                                     are installed in a given Galaxy isntance. It only allows to\
                                     get tools that were installed from a toolshed.')
    parser.add_argument('-g', '--galaxy', help='Galaxy server URL', required=True)
    parser.add_argument('-k', '--api_key', help='API key from Galaxy', required=True)
    parser.add_argument('-u', '--user', help='User to use for cloning or repositories from toolshed(s)',
                        required=True)
    parser.add_argument('-o', '--out_dir', help='Output directory for cloning of repositories from \
                        toolshed(s). Default is ./download_tools', default="./download_tools")
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    galaxy_site = args.galaxy
    api_key = args.api_key
    user = args.user
    outdir = args.out_dir + "/"
    verbose = args.verbose

    ###########################################################

    # Create output directory
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
        if verbose:
            print ("Creating " + outdir + "...")

    gi = galaxy.GalaxyInstance(galaxy_site, api_key)

    cpt_all = 0
    cpt_toolshed = 0
    cpt_down_repos = 0
    dico_tools = {}

    for tool in gi.tools.get_tools():
        cpt_all += 1
        if MOTIF in tool['id']:
            cpt_toolshed += 1
            elements = tool['id'].split('/')
            # Save information in a dictionnary
            if not elements[3] in dico_tools.keys():
                dico_tools[elements[3]] = {}
                dico_tools[elements[3]]['tools'] = []
                dico_tools[elements[3]]['folder'] = elements[3]
                dico_tools[elements[3]]['repos_link'] = elements[0] + "/" + elements[1] + "/" + \
                                                        elements[2] + "/" + elements[3]
            dico_tools[elements[3]]['tools'].append({'name': elements[4], 'version': elements[5]})

    # Cloning repos from toolshed(s) with mercurial
    for repos in dico_tools.keys():
        tool = {}
        tool['link'] = dico_tools[repos]['repos_link']
        tool['folder'] = dico_tools[repos]['folder']
        if verbose:
            print ("Cloning " + tool['folder'] + " from " + tool['link'] + "...")
        hglib.clone("https://" + user + "@" + tool['link'], outdir + tool['folder'])
        cpt_down_repos += 1

    # Write report in JSON format
    json_dico = json.dumps(dico_tools)
    report = open(outdir + REPORT, 'w')
    report.write(json_dico)
    report.close()

    if verbose:
        print ("Total number of tools: " + str(cpt_all) + ".")
        print ("Number of tools installed from a toolshed: " + str(cpt_toolshed) + ".")
        print ("Number of cloned repos: " + str(cpt_down_repos) + ".")
