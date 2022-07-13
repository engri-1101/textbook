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
echo "labs/.guides" >> .git/info/sparse-checkout
echo "labs/.codio-menu" >> .git/info/sparse-checkout
echo "labs/distribute.py" >> .git/info/sparse-checkout
git pull origin codio

# copy files from lab path to current directory
cp -r labs/$1/* .
cp -r labs/.guides .guides
cp -r labs/.codio-menu .codio-menu

# pull id from .guides_tmp into .guides and remove
python codio.py $1
rm -rf .guides_tmp
