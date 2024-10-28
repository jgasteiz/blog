#! /bin/bash

# Generate the site
python ./generator/generate.py

# Publish the site, using today's date as the commit message
message="Publish $(date + '%Y-%m-%d %H:%M:%S')"
git add --all
git commit -m $message
git push origin master
cd ./public
git add --all
git commit -m $message
git push origin master
cd ..