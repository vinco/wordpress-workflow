#!/bin/bash

# Wordpress-workflow provisioning script

apt-get update
apt-get install python-software-properties --assume-yes

# Configurations

PACKAGES="php7.0 mariadb-server libdbi-perl mariadb-client-10.0 php7.0-mysql apache2 tree vim curl git"
PACKAGES="$PACKAGES nginx-full php7.0-fpm php7.0-cgi spawn-fcgi php-pear php7.0-mcrypt "
PACKAGES="$PACKAGES php7.0-mbstring php7.0-curl php7.0-cli php7.0-gd php7.0-intl"
PACKAGES="$PACKAGES php7.0-xsl php7.0-zip fcgiwrap phpmyadmin"

APP_TOKEN="/home/vagrant/workflow-documentation/scripts/app_token"
PUBLIC_DIRECTORY="/home/vagrant/public_www"
PHPMYADMIN_DIRECTORY="/home/vagrant/public_www/phpmyadmin"

# Sets mysql pasword
debconf-set-selections <<< 'mariadb-server mysql-server/root_password password rootpass'
debconf-set-selections <<< 'mariadb-server mysql-server/root_password_again password rootpass'

# Sets configuration phpmyadmin pasword
debconf-set-selections <<< "phpmyadmin phpmyadmin/dbconfig-install boolean true"
debconf-set-selections <<< "phpmyadmin phpmyadmin/app-password-confirm password password"
debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/admin-pass password password"
debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/app-pass password password"
debconf-set-selections <<< "phpmyadmin phpmyadmin/reconfigure-webserver multiselect none"

echo "Installing packages $PACKAGES ..."

apt-get install $PACKAGES --assume-yes

# Makes apache not init in start
update-rc.d -f  apache2 remove
update-rc.d php5-fpm defaults

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

Installing composer
curl -sS https://getcomposer.org/installer | php
chmod +x composer.phar
mv composer.phar /usr/local/bin/composer

# Installing squizlabs/php_codesniffer & WordPress-Coding-Standards
composer create-project wp-coding-standards/wpcs:dev-master --no-dev
ln -s /home/vagrant/wpcs/vendor/bin/phpcs /usr/local/bin/phpcs
ln -s /home/vagrant/wpcs/vendor/bin/phpcbf /usr/local/bin/phpcbf

# Generates unique token for application
if [ ! -f "$APP_TOKEN" ]; then
    touch $APP_TOKEN
    echo $RANDOM > $APP_TOKEN
fi

# Create a symbolic link from the installation phpmyadmin
if [ ! -d "$PHPMYADMIN_DIRECTORY" ]; then
    ln -s /usr/share/phpmyadmin $PHPMYADMIN_DIRECTORY
fi

# Activates site

# Apache
cp /home/vagrant/templates/wordpress.apache /etc/apache2/sites-available/wordpress.conf
a2enmod actions
a2ensite wordpress
service apache2 stop

# Nginx
cp /home/vagrant/templates/www.conf /etc/php/7.0/fpm/pool.d/www.conf
cp /home/vagrant/templates/wordpress.nginx /etc/nginx/sites-available/wordpress
cp /home/vagrant/templates/nginx.conf /etc/nginx/nginx.conf
cp /home/vagrant/templates/nginx.conf /home/vagrant/nginx.conf
rm  /etc/nginx/sites-enabled/*
ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/
service php7.0-fpm restart
service nginx restart
export WP_ENV=vagrant

# Create mysql
mysql -u"root" -p"password" -e "CREATE USER 'wordpress'@'localhost' IDENTIFIED BY 'password'"
mysql -u"root" -p"password" -e "GRANT ALL PRIVILEGES ON * . * TO 'wordpress'@'localhost' WITH GRANT OPTION"
