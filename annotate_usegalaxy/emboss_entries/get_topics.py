#! /usr/bin/env python

"""
Check EDAM_topics for a list of given bio.tools entries
"""

import requests


LIST = "/home/khillion/Playground/emboss_biotools/list_emboss.tsv"

print("#bio.tools-ID\tedam_topics\tlink")
entries = open(LIST, 'r')
for entry in entries:
    entry = entry.strip()
    query = "https://bio.tools/api/" + entry
    req = requests.get(query)
    print(entry, req.json()['topic'], query, sep="\t")
