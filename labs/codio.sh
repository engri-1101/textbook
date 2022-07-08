#!bin/bash

# TODO: see if this step can be avoided
# .guides is generated within Codio to generate an id
# rename .guides to .guides_tmp to avoid overlap with pulled .guides file
mv .guides .guides_tmp

# checkout only the desired lab 
git init
git remote add -f origin git@github.coecis.cornell.edu:hwr26/engri-1101-labs.git
git config core.sparseCheckout true
echo "labs/$1" >> .git/info/sparse-checkout
git pull origin codio

# move files from lab path to current directory
mv labs/$1/* .
rm -rf labs

# pull id from .guides_tmp into .guides and remove
python codio.py
rm .guides_tmp
