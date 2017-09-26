# Annotation of https://usegalaxy.org wrappers from https://bio.tools entries

## 25 September 2017

### Get https://bio.tools content

First, we recover all entries from https://bio.tools using `get_all_biotools.py` script which generates `all_biotools.json` file.

### Mapping between Galaxy wrappers and https://bio.tools entries

The second step is to perform mapping between Galaxy wrappers and entries on https://bio.tools.
You need to have downloaded all wrappers from the instance first (using: [get\_xmls\_from\_galaxy.py](https://github.com/khillion/galaxyxml-analysis/tree/master/galaxyxml_analysis)).
To do that, we used `xml_biotools_mapping.py` script.

```bash
python xml_biotools_mapping.py -d USEGALAXY -r USEGALAXY/download_report.json -b all_biotools.json -o
```

This generates a `mapping.tsv` file that needs to be manually curated prior to use.

### Manual curation of raw `mapping.tsv` file

Prior to run ToolDog to annotate every wrappers, we need to curate the `mapping.tsv` file.

#### Remove wrappers with no corresponding https://bio.tools entry

```bash
awk 'index($3, "[")' mapping.tsv
```

#### Maps wrapper to a unique entry

This step is done manually, to check which entry corresponds best to the wrapper.
For bedtools tools:
```bash
awk '{if($3~"bedtools") $3="bedtools";print}' FS="\t" OFS="\t" mapping.tsv
```
For emboss entries:
```bash
awk '{if($3~"emboss") $3="emboss";print}' FS="\t" OFS="\t" mapping.tsv
```

You end up with the `filtered\_mapping.tsv` file

### Running ToolDog on selected tools

All concerned wrappers were copied into `old_xmls` folder.
```bash
mkdir old_xmls
for i in `cut -f1 final_mapping.tsv`;do cp $i old_xmls;done
```
And paths are updated in the `filtered_mapping.tsv` to build `final_mapping.tsv`:
```bash
awk '{split($1,a,"/"); $1="old_xmls/"a[3]; print}' FS="\t" OFS="\t" filtered_mapping.tsv > final_mapping.tsv
```

Tools were annotated using [ToolDog](https://github.com/bio-tools/ToolDog). Results of annotation can be found in `new_xmls` folder.

#### Tools that could not be annotated (7 out of 224)

| Galaxy wrapper | Biotool entry | Reason |
| -------------- | ------------- | ------ |
| kraken.xml | kraken | Unable to load XML into `galaxyxml` because there is a param without `name` |
| rg_rnaStar.xml | star | Unable to load XML into `galaxyxml` because there is a param without `name` |
| kraken-filter.xml | kraken | Unable to load XML into `galaxyxml` because there is a param without `name` |
| fastq_combiner.xml | fastq_groomer_parallel-ip | TODO |
| closestBed.xml | bedtools | Unable to load XML into `galaxyxml` because there is a param without `name` |
| hisat2.xml | HISAT2 | Unable to load XML into `galaxyxml` because there is a param without `name` |
| diamond.xml | Diamond | Unable to load XML into `galaxyxml` because there is a param without `name` |

## 01 September 2017

Re-run analysis and counts number of tools based on different criteria (can be found in logs file):

| Title | Counts |
| ----- | ------ | 
| Total number of tools cloned from toolshed | 665 |
| Tool description with `<citations>` | 455 |
| `<citations>` with DOI | 405 |
| Entry found corresponding to DOI on bio.tools | 224 |
| Edam terms retrieved from bio.tools | 217 |

Only 106 wrappers have been annotated with ToolDog (can be found in `new_xmls` folder)
because wrappers that cannot be loaded into the `galaxyxml` model or EDAM with no uri in bio.tools.
