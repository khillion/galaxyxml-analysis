# galaxyxml-analysis

Repository to gather script to retrieve and analyse Galaxy XML tools from a given instance and perform analysis of their content.

## Requirements

* bioblend
* hglib

You also need to have an account on the Galaxy instance with an API key as well
as an account on the corresponding toolshed.

## How it works ?

### get\_xml\_from\_galaxy.py

```
python3 get_xml_from_galaxy.py -k API_KEY -g GALAXY_URL -u TOOLSHED_USERNAME
```

The script will clone all repositories containing tools installed on the given Galaxy instance.
It also generates a JSON report for further analysis by other scripts (mainly reminding which
tools are installed on the instance).
