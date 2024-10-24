#!/bin/bash

# Deploy to github pages
# The arguments are the commit comment

str="'$*'"

if [ -d /$HOME/MauricioD13.github.io ]; then

    hugo -d $HOME/MauricioD13.github.io/

    cd $HOME/MauricioD13.github.io/

    touch CNAME

    echo "tech-mauricio.me" > CNAME

    git add .

    git commit -m "$str"

    git push origin main

else

    echo "MauricioD13.github.io repo is not in the $HOME location, download it and try again"

fi