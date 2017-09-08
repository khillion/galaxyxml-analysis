"""
Analyses of XMLs from a Galaxy (from directory created with get_xmls_from_galaxy.py)

Need to be improved:
* how many tools have a version in the tool tag ?
"""

###########  Import  ###########

import json
import os
import sys
import re
import argparse

from lxml import etree
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###########  Constant(s)  ###########

BARPLOTTITLE = "Graph sample"
BARPLOTFILENAME = "test.png"

###########  Function(s)  ###########


def init_xml_dict(xml_dict, tool_id):
    """
    Initialize a new dictionnary to an existing dictionnary

    xmls_infos: [DICT]
    tool_id: will be the key of the new dict [STRING]
    """
    xml_dict[tool_id] = {}
    xml_dict[tool_id]['Description'] = 0
    xml_dict[tool_id]['Citations'] = 0
    xml_dict[tool_id]['Help'] = 0
    xml_dict[tool_id]['edam_topics'] = 0
    xml_dict[tool_id]['edam_operations'] = 0
    return xml_dict


def check_field(tool, field):
    """
    tool: xml parsed with lxml.etree
    field: field to look for [STRING]

    check the presence of the <field> in the xml
    """
    if tool.getroot().find(field) is not None:
        return 1
    return 0


def check_macro_field(macro, field):
    """
    tool: macro.xml parsed with lxml.etree
    field: field to look for [STRING]

    check the presence of the <field> in the macro xml
    """
    for child in tool.getroot().getchildren():
        if child.find(field) is not None:
            return 1
    return 0


def check_description(tool):
    """
    tool: xml parsed with lxml.etree

    check the presence of a non-empty description
    """
    if tool.getroot().find('description') is not None:
        if tool.getroot().find('description').text is not None:
            description = tool.getroot().find('description').text
            if not re.match('^ {0,}$', description):  # empty description
                return 1
    return 0


def check_citations(tool):
    """
    tool: xml parsed with lxml.etree

    check the presence of citations:
      either the <citations> balises
      or the presence of words in the help (doi:, publication,reference and citation)
    """
    if check_field(tool, 'citations'):
        return 1
    elif tool.getroot().find('help') is not None:
        if (re.search('[P,p]ublication[s]*', tool.getroot().find('help').text)):
            return 1
        elif (re.search('[C,c]itation[s]*', tool.getroot().find('help').text)):
            return 1
        elif (re.search('[R,r]eference[s]*', tool.getroot().find('help').text)):
            return 1
        elif (re.search('doi:', tool.getroot().find('help').text)):
            return 1
    return 0


def list_installed_tools(download_report, repo):
    """
    download_report: report from get_xml_from_galaxy.py [DICT]
    repo: name of the repo where we want to get the list of tools [STRING]
    """
    list_tools = []
    for tool in download_report[repo]['tools']:
        list_tools.append(tool['name'])
    return list_tools


def load_macro(tool, macro_path):
    """
    Load macro content and attach it as a child node to the root of tool.
    """
    macro = etree.parse(macro_path)
    for exp in tool.findall("expand"):
        for mac in macro.findall("xml"):
            if exp.attrib.get('macro', '1') == mac.attrib.get('name', '2'):
                for child in mac:
                    # Add corresponding content to the tool
                    tool.getroot().append(child)
        # Remove expand from the tool
        tool.getroot().remove(exp)


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
    parser.add_argument('-t', '--title', help='Title of the graph', required=False)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    ###########################################################

    # Process outfile name and graph title
    if args.out_file:
        file_name = args.out_file + '.png'
    else:
        file_name = BARPLOTFILENAME
    if args.title:
        graph_title = args.title
    else:
        graph_title = BARPLOTTITLE

    # Load report
    json_down_report = open(args.download_report, 'r')
    download_report = json.load(json_down_report)

    # Get paths of all XML tools (key of dict with macro as value if it exists)
    tool_paths = []
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
                        tool_paths.append(file_path)

    # Get information about each XMLs
    xmls_infos = {}
    cpt_tool = 0  # For number of tool XMLs
    for xml in tool_paths:
        tool = etree.parse(xml)
        # Macro ?
        if tool.find('macros') is not None:
            for mac_file in tool.find('macros'):
                if mac_file.tag == 'import':
                    macro_path = os.path.dirname(xml) + "/" + mac_file.text
                    load_macro(tool, macro_path)
        cpt_tool += 1
        tool_id = tool.getroot().attrib['id']
        init_xml_dict(xmls_infos, tool_id)
        # Description ?
        xmls_infos[tool_id]['Description'] = check_description(tool)
        # Citations ?
        xmls_infos[tool_id]['Citations'] = check_field(tool, 'citations')
        # Citations or reference in help
        xmls_infos[tool_id]['Citations_info'] = check_citations(tool)
        # Help ?
        xmls_infos[tool_id]['Help'] = check_field(tool, 'help')
        # Edam operations ?
        xmls_infos[tool_id]['edam_operations'] = check_field(tool, 'edam_operations')
        # Edam topics ?
        xmls_infos[tool_id]['edam_topics'] = check_field(tool, 'edam_topics')

    # Make plots
    df_export = pd.DataFrame.from_dict(xmls_infos)
    total = df_export.T.sum(0)

    # Calculate number of XML with help + description + citations
    cpt_all_fields = 0
    for tool in xmls_infos:
        citation = xmls_infos[tool]['Citations']
        pres_help = xmls_infos[tool]['Help']
        description = xmls_infos[tool]['Description']
        if citation & pres_help & description:
            cpt_all_fields += 1
    # Add it to the graph (and also total number of tools)
    total = total.append(pd.Series([cpt_all_fields, cpt_tool], index=["H+D+C", "Total"]))
    #   Transform to percentage
    total_desc = total['Total']
    total = total/total_desc * 100

    # Make list of bar plot in the desired order
    barplot_values = [total['Help'], total['Description'], total['Citations'],
                      total['Citations_info'], total['H+D+C'], total['edam_operations'], total['edam_topics']]
    barplot_legend = ['Help', 'Description', 'Citations', 'Citations_info', 'H+D+C', 'edam_ope',
                      'edam_top']

    plt.bar([-0.3, 0.7, 1.7, 2.7, 3.7, 4.7, 5.7], barplot_values, width=0.6,
            alpha=0.8, color='#5dade2')
    plt.title(graph_title, fontsize=20)
    plt.ylabel("% of tool descriptions", fontsize=18)
    plt.xticks([-0.3, 0.7, 1.7, 2.7, 3.7, 4.7, 5.7], barplot_legend, rotation=45)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(file_name)

    # Get number of installed tools on galaxy from report
    print ('Total number analysed:', cpt_tool)
    cpt_install = 0
    for repo in download_report.keys():
        for tool in download_report[repo]['tools']:
            cpt_install += 1
    print("Total number installed on galaxy from toolshed:", cpt_install)
