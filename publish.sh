#! /bin/bash

# Generate the site
python ./generator/generate.py
date=$(date + '%Y-%m-%d %H:%M:%S')
git add --all
git commit -m "Publish $date"
git push origin master
cd ./public
git add --all
git commit -m $message
git push origin master
cd ..