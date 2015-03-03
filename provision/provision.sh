#!/bin/bash

# Wordpress-workflow provisioning script

apt-get update


# Configurations

PACKAGES="php5 mysql-client mysql-server php5-mysql apache2 tree vim curl"
PUBLIC_DIRECTORY="/home/vagrant/public_www"

# Sets mysql pasword
debconf-set-selections <<< 'mysql-server mysql-server/root_password password password'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password password'

echo "Installing packages $PACKAGES ..."

apt-get install $PACKAGES --assume-yes

# Wordpress client and public folder
if [ ! -d "$PUBLIC_DIRECTORY" ]; then
    mkdir $PUBLIC_DIRECTORY
fi

chown -R vagrant $PUBLIC_DIRECTORY
chgrp -R vagrant $PUBLIC_DIRECTORY

echo "Installing wp-cli"
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar 
chmod +x wp-cli.phar
mv wp-cli.phar /usr/local/bin/wp

# Activates site
mv /home/vagrant/wordpress /etc/apache2/sites-available/
a2dissite default
a2ensite wordpress
service apache2 restart
