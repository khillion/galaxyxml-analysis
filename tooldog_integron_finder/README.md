# Test of tooldog on one entry from https://bio.tools

Here are stored the result of the following commands using `ToolDog v0.3.1`:

```bash
pip install tooldog
tooldog -g integron_finder --inout_biotools > integron_finder.xml
tooldog -c integron_finder --inout_biotools > integron_finder.cwl
```
