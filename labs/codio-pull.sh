#!bin/bash

# TODO: see if this step can be avoided
# .guides is generated within Codio to generate an id
# rename .guides to .guides_tmp to avoid overlap with pulled .guides file
mv .guides .guides_tmp

# checkout only the desired lab 
git pull origin codio

# copy files from lab path to current directory
cp -r labs/$1/* .
cp -r labs/.guides .guides
cp -r labs/.codio-menu .codio-menu

# pull id from .guides_tmp into .guides and remove
python codio.py $1
rm -rf .guides_tmp
