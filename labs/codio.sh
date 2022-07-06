#!bin/bash

# checkout only the desired lab 
git init
git remote add -f origin git@github.coecis.cornell.edu:hwr26/engri-1101-labs.git
git config core.sparseCheckout true
echo "labs/$1" >> .git/info/sparse-checkout
git pull origin master

# move files from lab path to current directory
mv labs/$1/* .
rm -rf labs

