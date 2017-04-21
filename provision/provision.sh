#!/bin/bash

# Wordpress-workflow provisioning script

apt-get update
apt-get install python-software-properties --assume-yes
# Install php5.6
sudo apt-get purge `dpkg -l | grep php| awk '{print $2}' |tr "\n" " "`
add-apt-repository ppa:ondrej/php
apt-get update


# Configurations

PACKAGES="php5.6 mariadb-server libdbi-perl mariadb-client-10.0 php5.6-mysql apache2 tree vim curl git"
PACKAGES="$PACKAGES nginx-full php5.6-fpm php5.6-cgi spawn-fcgi php-pear php5.6-mcrypt "
PACKAGES="$PACKAGES php5.6-mbstring php5.6-curl php5.6-cli php5.6-gd php5.6-intl"
PACKAGES="$PACKAGES php5.6-xsl php5.6-zip fcgiwrap phpmyadmin"

APP_TOKEN="/home/ubuntu/workflow-documentation/scripts/app_token"
PUBLIC_DIRECTORY="/home/ubuntu/public_www"
PHPMYADMIN_DIRECTORY="/home/ubuntu/public_www/phpmyadmin"

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

chown -R ubuntu $PUBLIC_DIRECTORY
chgrp -R ubuntu $PUBLIC_DIRECTORY

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
ln -s /home/ubuntu/wpcs/vendor/bin/phpcs /usr/local/bin/phpcs
ln -s /home/ubuntu/wpcs/vendor/bin/phpcbf /usr/local/bin/phpcbf

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
cp /home/ubuntu/templates/wordpress.apache /etc/apache2/sites-available/wordpress
cp /home/ubuntu/templates/httpd.conf /etc/apache2/conf.d/httpd.conf
a2enmod actions
a2dissite default
a2ensite wordpress
service apache2 stop

# Nginx
cp /home/ubuntu/templates/wordpress.nginx /etc/nginx/sites-available/wordpress
cp /home/ubuntu/templates/www.conf /etc/php/5.6/fpm/pool.d/www.conf
cp /home/ubuntu/templates/nginx.conf /etc/nginx/nginx.conf
cp /home/ubuntu/templates/nginx.conf /home/ubuntu/nginx.conf
rm  /etc/nginx/sites-enabled/*
ln -s /etc/nginx/sites-available/wordpress /etc/nginx/sites-enabled/
service php5.6-fpm restart
service nginx restart
export WP_ENV=vagrant

# Create mysql
mysql -u"root" -p"password" -e "CREATE USER 'wordpress'@'localhost' IDENTIFIED BY 'password'"
mysql -u"root" -p"password" -e "GRANT ALL PRIVILEGES ON * . * TO 'wordpress'@'localhost' WITH GRANT OPTION"
