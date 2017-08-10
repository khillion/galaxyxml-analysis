import requests
import json

OUTFILE = "tools.json"

def fetch(p="", c=[]):
    try:
        url = "https://bio.tools/api/t" + p
        json = requests.get(url).json()

        return fetch(json['next'], (c + json['list']))

    except:
        return c

tools = fetch()

with open(OUTFILE, 'w') as outfile:
    json.dump(tools, outfile)
