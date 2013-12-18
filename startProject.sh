#!/bin/bash
#
# startProject.sh
#
# creates the basic structure needed to develop a new wordpress project
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR"  ]]; then DIR="$PWD"; fi

# create every folder needed

echo "Creando estructura de directorios"

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
    cp -r $DIR/database/* $DIR/../src/database
fi
