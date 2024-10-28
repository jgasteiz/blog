#! /bin/bash

# Generate the site
python ./generator/generate.py
NOW=`date '+%FT%H:%M:%S'`
git add --all
git commit -m "Publish $NOW"
git push origin master
cd ./public
git add --all
git commit -m "Publish $NOW"
git push origin master
cd ..