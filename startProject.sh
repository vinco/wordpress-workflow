#!/bin/bash
#
# startProject.sh
#
# creates the basic structure needed to develop a new wordpress project
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR"  ]]; then DIR="$PWD"; fi

# create every folder needed

echo "Creating directory structure"

if [[ ! -d "$DIR/../src" ]]; then
    mkdir $DIR/../src
fi

if [[ ! -d "$DIR/../src/themes" ]]; then
    mkdir $DIR/../src/themes
fi

if [[ ! -d "$DIR/../src/plugins" ]]; then
    mkdir $DIR/../src/plugins
fi

if [[ ! -d "$DIR/../src/init" ]]; then
    mkdir $DIR/../src/init
fi

if [[ ! -d "$DIR/../src/database" ]]; then
    mkdir $DIR/../src/database
fi

echo "Setting configuration files"

if [[ ! -f  "$DIR/../Vagrantfile" ]]; then
    ln -s $DIR/Vagrantfile $DIR/../Vagrantfile
fi

if [[ ! -f  "$DIR/../fabfile.py" ]]; then
    ln -s $DIR/fabfile.py $DIR/../fabfile.py
fi

if [[ ! -f  "$DIR/../environments.json" ]]; then
    cp $DIR/defaults/environments.json $DIR/../environments.json
fi

if [[ ! -f  "$DIR/../settings.json" ]]; then
    cp $DIR/defaults/settings.json $DIR/../settings.json
fi

echo "writing new values to .gitigonre"

if [[ ! -f  "$DIR/../.gitignore" ]]; then
    cat $DIR/defaults/git.gitignore >> $DIR/../.gitignore
else 
    while read line
    do
        if ! grep -q "$line"  "$DIR/../.gitignore"; then
            echo "$line" >> $DIR/../.gitignore
        fi
    done < $DIR/defaults/git.gitignore
fi


cd $DIR/../
vagrant up
