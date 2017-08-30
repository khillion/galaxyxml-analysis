# Annotation of https://usegalaxy.org wrappers from https://bio.tools entries

## 3 August 2017

First step is to perform mapping between Galaxy wrappers and entries on https://bio.tools.
To do that, we used `xml_biotools_mapping.py` script (you need to download first all XMLs with `get_xmls_from_galaxy.py`.

This generates a `mapping.tsv` file that needs to be manually curated prior to use. `final_mapping.tsv` file is finally used to perform annotations of all XMLs.

All concerned wrappers were copied into `old_xmls` folder and were annotated using [ToolDog](https://github.com/bio-tools/ToolDog). Results of annotation can be found in `new_xmls` folder.

## 30 August 2017

Re-run analysis and counts number of tools based on different criteria (can be found in logs file):

| Title | Counts |
| ----- | ------ | 
| Total number of tools cloned from toolshed | XX |
| Tool description with `<citations>` | XX |
| `<citations>` with DOI | XX |
| Entry found corresponding to DOI on bio.tools | XX |
| Edam terms retrieved from bio.tools | XX |
