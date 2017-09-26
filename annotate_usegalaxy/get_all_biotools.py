#!/usr/bin/env python

"""
Get all content of bio.tools in JSON through the API.
"""

import requests
import datetime
import json

OUTFILE = "all_biotools.json"

# First need to determine how many tools there are in the registry
req_tools = requests.get("https://bio.tools/api/t")
nb_tools = req_tools.json()['count']
tool_per_page = len(req_tools.json()['list'])
print(tool_per_page)
print("Nb of tools to download from https://bio.tools: " + str(nb_tools))

# 25 tools per result page, so need to loop
full_list_tools = []
for i in range(1, (nb_tools-1)//tool_per_page + 2):
    req_tools = requests.get("https://bio.tools/api/t?page=" + str(i))
    full_list_tools += req_tools.json()['list']
    if i % 10 == 0:
        print(str(i*tool_per_page) + " tools downloaded...")

print(str(len(full_list_tools)) + " have been successfully downloaded.")

with open(OUTFILE, 'w') as outfile:
    json.dump(full_list_tools, outfile)
