# galaxyxml_analysis

This folder contains scripts used to retrieve Galaxy XML tools from a given instance and perform an analysis of their content.

## Requirements

In order to clone repositories from Galaxy Toolsheds, you need [mercurial](https://www.mercurial-scm.org/) on your machine.

All Python libraries required for the different scripts are listed in `requirements.txt`.

You also need to have an account on the Galaxy instance with an API key, as well as an account on the corresponding Toolshed(s).

## How does it work ?

### get\_xmls\_from\_galaxy.py

```bash
python get_xml_from_galaxy.py -k API_KEY -g GALAXY_URL -u USERNAME -o OUT_DIR
```

The script will clone all repositories containing tools installed on the given Galaxy instance.
It also generates a JSON file (`OUT_DIR/download_report.json`) for further analysis by other scripts (mainly reporting which
tools and versions are installed on the instance).

### analyse\_xmls.py

```bash
python analyse_xmls.py -r REPORT -d DIRECTORY -o GRAPH_FILE -t GRAPH_TITLE
```

This script performs an analysis of Galaxy tools by checking the presence of several tags and content (also inspecting macro content) and generates a histogram:

* `<help>`
* Non empty `<description>`
* `<citations>`
* `<edam_operations>`
* `<edam_topics>`

### get\_galaxy\_info.py

### counts\_param\_type.py
