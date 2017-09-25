# Test of tooldog on one entry from https://bio.tools

```bash
pip install tooldog
tooldog -g integron_finder --inout_biotools > integron_finder.xml
tooldog -c integron_finder --inout_biotools > integron_finder.cwl
```
