"""
Query https://bio.tools with name of tool wrappers downloaded.
"""

###########  Import  ###########

import json
import os
import sys
import re
import argparse

from lxml import etree
import requests

###########  Constant(s)  ###########

OUTFILE = "mapping.json"

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


def get_all_tools(download_report):
    """
    download_report: report from get_xml_from_galaxy.py [DICT]
    """
    list_tools = []
    for key, value  in download_report.items():
        for tool in value['tools']:
            list_tools.append(tool)
    return list_tools


def query_biotools(name):
    """
    perform query on https://bio.tools using bio.tools API
    it returns all tool ID found for the query
    """
    biotool_query = "https://bio.tools/api/tool/?q=" + name
    http_query = requests.get(biotool_query)
    json_query = http_query.json()
    id_list = []
    for tool in json_query['list']:
        id_list.append(tool['id'])
    return(id_list)
    

###########  Main  ###########

if __name__ == "__main__":

    ## Parse arguments
    parser = argparse.ArgumentParser(description='List information about a Galaxy server')
    parser.add_argument('-r', '--download_report', help='Download report (.json)',
                        required=True)
    parser.add_argument('-d', '--directory', help='Directory containing all repositories ' +
                        'from toolsheds', required=True)
    parser.add_argument('-o', '--out_file', help='Name of the output file without extension',
                        required=False)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    ###########################################################

    # Process outfile name and graph title
    if args.out_file:
        file_name = args.out_file + '.json'
    else:
        file_name = OUTFILE

    # Load report
    json_down_report = open(args.download_report, 'r')
    download_report = json.load(json_down_report)

    tools = get_all_tools(download_report)
    for tool in tools:
        print(tool['name'], query_biotools(tool['name']))

    """
    # Get paths of all XML tools (key of dict with macro as value if it exists)
    tool_paths = {}
    for root, dirs, files in os.walk(args.directory):
        for file in files:
            if file.endswith(".xml") and file[0] != '.':
                file_path = root + '/' + file
                try:
                    tool = etree.parse(file_path)
                except etree.XMLSyntaxError:
                    continue
                if tool.getroot().tag == 'tool':
                    repo = root.split('/', 1)[1].split('/')[0]
                    installed_tools = list_installed_tools(download_report, repo)
                    if tool.getroot().attrib['id'] in installed_tools:
                        if tool.getroot().find('macros') is None:
                            tool_paths[file_path] = 0
                        else:
                            macro = tool.getroot().find('macros')[0].text
                            tool_paths[file_path] = root + '/' + macro
    """
