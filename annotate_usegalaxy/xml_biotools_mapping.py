#! /usr/bin/env python

"""
Perform mapping of XML to bio.tools entry using citation information.
"""

###########  Import  ###########

import json
import os
import sys
import argparse
import requests
from collections import defaultdict

from lxml import etree

###########  Constant(s)  ###########

OUTFILE = "mapping.tsv"

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


###########  Main  ###########

if __name__ == "__main__":

    ## Parse arguments
    parser = argparse.ArgumentParser(description='List information about a Galaxy server')
    parser.add_argument('-r', '--download_report', help='Download report (.json)',
                        required=True)
    parser.add_argument('-d', '--directory', help='Directory containing all repositories ' +
                        'from toolsheds', required=True)
    parser.add_argument('-b', '--biotools', help='All entries from biotools (.json) ',
                        required=True)
    parser.add_argument('-o', '--out_file', help='Name of the output file without extension',
                        required=False)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    ###########################################################

    # Process outfile name and graph title
    if args.out_file:
        outfile_name = args.out_file + '.json'
    else:
        outfile_name = OUTFILE

    # Load report
    json_down_report = open(args.download_report, 'r')
    download_report = json.load(json_down_report)

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

    # Generates mapping doi -> bio.tools entry from all bio.tools
    doi_to_biot = defaultdict(list)
    # - load all entries from bio.tools
    with open(args.biotools, 'r') as f:
        biotools = json.load(f)
    # - build mapping
    for tool in biotools:
        for publication in tool['publication']:
            if publication['doi'] is not None:
                doi_to_biot[publication['doi']].append(tool['id'])
            else:
                if publication['pmid'] is not None:
                    id_query = publication['pmid']
                elif publication['pmcid'] is not None:
                    id_query = publication['pmcid']
                req = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=" + id_query
                try:
                    xml_req = etree.fromstring(requests.get(req).text)
                except:
                    pass
                if xml_req.find('record') is not None:
                    try:
                        doi_to_biot[xml_req.find('record').attrib['doi']].append(tool['id'])
                        print("successfully got doi from " + id_query)
                    except:
                        print("Could not find doi corresponding to " + id_query)

    # Build list XML doi biotools_id
    final_list = "#XML\tdoi\tbiotools_id\n"
    for xml in tool_paths.keys():
        tool = etree.parse(xml)
        if tool.find('citations') is not None:
            citations = tool.find('citations')
            for citation in citations:
                if citation.attrib.get('type', None) == 'doi':
                    doi = citation.text
                else:
                    continue
                if doi_to_biot[doi]:
                    final_list += xml + "\t" + doi + "\t" + str(doi_to_biot[doi]) + "\n"

    with open(outfile_name, 'w') as of:
        of.write(final_list)
