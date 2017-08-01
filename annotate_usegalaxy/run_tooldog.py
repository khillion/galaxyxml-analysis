#! /usr/bin/env python

"""
Run annotation part of ToolDog on a list of Galaxy wrappers
"""

import os
import sys
import argparse

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Run ToolDog on a list a Galaxy wrappers.')
    parser.add_argument('-i', '--input_list', help='List of wrappers.', required=True)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    wrapper_list = args.input_list

    wrap_f = open(wrapper_list, 'r')
    for tool in wrap_f:
        if "#" in tool:
            continue
        tool.replace('\t', '')
        files = tool.split()
        input_xml = files[0]
        output_xml = 'new_xmls/' + input_xml.split('/')[-1]
        biotool_id = files[2]
        command = " ".join(["tooldog -g", biotool_id, "--existing_desc", input_xml, "-f", output_xml])
        print("Running", command, "...")
        os.system(command)
