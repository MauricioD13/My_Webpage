#!/bin/bash

# Deploy to github pages
# The arguments are the commit comment

str="'$*'"

#if [[ -z "${VIRTUAL_ENV}" ]]; then
#    dependency=$( pip freeze | grep -i semgrep )
#    if [[ -z dependency ]]; then
        
#else


cd ../

if [ -d /$HOME/MauricioD13.github.io ]; then

    hugo -d $HOME/MauricioD13.github.io/

    cd $HOME/MauricioD13.github.io/

    git add .

    git commit -m "$str"

    git push origin main

else

    echo "MauricioD13.github.io repo is not in the $HOME location, download it and try again"

fi