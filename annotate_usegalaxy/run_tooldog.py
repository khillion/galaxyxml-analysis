#! /usr/bin/env python

"""
Run annotation part of ToolDog on a list of Galaxy wrappers
"""

import os
import sys
import argparse
from lxml import etree
from subprocess import call

SEP = "\t"


def get_edam(tool, edam_type):
    edam_list = []
    if tool.find(edam_type) is not None:
        for term in tool.find(edam_type):
            edam_list.append(term.text)
    return edam_list


def get_topics(tool):
    return get_edam(tool, 'edam_topics')


def get_operations(tool):
    return get_edam(tool, 'edam_operations')


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Run ToolDog on a list a Galaxy wrappers.')
    parser.add_argument('-i', '--input_list', help='List of wrappers.', required=True)
    parser.add_argument('-r', '--report', help='Name of report (default: tooldog_reports.tsv.',
                        default='tooldog_report.tsv')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    wrapper_list = args.input_list

    # Preparing report and header
    report = []
    report.append(SEP.join(["#XML", "DOI", "bio.tools-ID", "ToolDog-Status",
                           "fetched-edam_topics", "fetched-edam_operations"]))

    wrap_f = open(wrapper_list, 'r')
    for tool in wrap_f:
        if "#" in tool:
            continue
        tool.replace('\t', '')
        files = tool.split()
        input_xml = files[0]
        output_xml = 'new_xmls/' + input_xml.split('/')[-1]
        biotool_id = files[2]
        command = ["tooldog", "-g", biotool_id, "--existing_desc", input_xml,
                   "-f", output_xml, "-v", "-l", "--log_level", "DEBUG"]
        print("Running", command, "...")
        tooldog_status = call(command)
        # Add edam operations and topics to report
        try:
            new_desc = etree.parse(output_xml)
            report.append("\t".join(files + [str(tooldog_status), str(get_topics(new_desc)), str(get_operations(new_desc))]))
        except:
            report.append("\t".join(files + [str(tooldog_status), "[]", "[]"]))
            pass

    with open(args.report, "w") as out_file:
        print("\n".join(report), end="", file=out_file)
