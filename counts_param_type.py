#! /usr/bin/env python

"""
Statistics about type for <param>

This script need to be modified to be more general and gets a tag as an argument
and make statistics about attributes for a given tags.

Idea can be extended of course.
"""

###########  Import  ###########

import json
import os
import sys
import re
import argparse
from collections import defaultdict

from lxml import etree

###########  Function(s)  ###########


def list_installed_tools(download_report, repo):
    """
    download_report: report from get_xml_from_galaxy.py [DICT]
    repo: name of the repo where we want to get the list of tools [STRING]
    """
    list_tools = []
    for tool in download_report[repo]['tools']:
        list_tools.append(tool['name'])
    return list_tools


def count_type_param(children, stat_dict):
    """
    """
    for child in children:
        if child.tag == 'param':
            stat_dict[child.tag] += 1
            stat_dict[child.attrib.get('type', 'not_found')] += 1
        elif child.getchildren():
            count_type_param(child.getchildren(), stat_dict)

###########  Main  ###########

if __name__ == "__main__":

    ## Parse arguments
    parser = argparse.ArgumentParser(description='List information about a Galaxy server')
    parser.add_argument('-r', '--download_report', help='Download report (.json)',
                        required=True)
    parser.add_argument('-d', '--directory', help='Directory containing all repositories ' +
                        'from toolsheds', required=True)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    ###########################################################

    # Load report
    json_down_report = open(args.download_report, 'r')
    download_report = json.load(json_down_report)

    # Get paths of all XML tools (key of dict with macro as value if it exists)
    tool_paths = {}
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            if file.endswith(".xml"):
                file_path = root + '/' + file
                tool = etree.parse(file_path)
                if tool.getroot().tag == 'tool':
                    repo = root.split('/', 1)[1].split('/')[0]
                    installed_tools = list_installed_tools(download_report, repo)
                    if tool.getroot().attrib['id'] in installed_tools:
                        if tool.getroot().find('macros') is None:
                            tool_paths[file_path] = 0
                        else:
                            macro = tool.getroot().find('macros')[0].text
                            tool_paths[file_path] = root + '/' + macro

    # Get information about each XMLs
    param_stats = defaultdict(int)
    cpt_tool = 0  # For number of tool XMLs
    for xml in tool_paths.keys():
        tool = etree.parse(xml)
        cpt_tool += 1
        tool_id = tool.getroot().attrib['id']
        if tool.getroot().find('inputs') is not None:
            count_type_param(tool.getroot().find('inputs').getchildren(), param_stats)

    # Get number of installed tools on galaxy from report
    print ('Total number analysed:', cpt_tool)
    for k, v in param_stats.items():
        print(k, ':', v)
