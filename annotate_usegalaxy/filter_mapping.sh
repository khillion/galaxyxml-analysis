#!/bin/bash

out=$(echo ${1%.tsv}.tmp)
grep '\[' $1 > $out

# Number of tools with entry on bio.tools
echo "-- Number of tools with one or several corresponding entries on bio.tools: $(wc -l $out)"

echo "Manual curation is now necessary to make the correct mapping between wrapper and bio.tools entry."
