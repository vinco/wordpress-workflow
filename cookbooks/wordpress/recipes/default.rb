# Recipes

include_recipe "apt"
include_recipe "build-essential"
include_recipe "mysql::server"
include_recipe "apache2"
include_recipe "curl"


# Install Basic Packages

%w{libapache2-mod-php5 php5 mysql-server mysql-client
zsh git-core build-essential tree vim-nox
libapache2-mod-auth-mysql php5-mysql php5-mcrypt php5-gd php5-curl
php-codesniffer 
}.each do
|pkg|
  package pkg do
    action :install
  end
end

# Configure zsh
bash "Configurar zsh con oh-my-zsh!" do
    code <<-EOH
git clone git://github.com/jairtrejo/oh-my-zsh.git /home/vagrant/.oh-my-zsh
cp /home/vagrant/.oh-my-zsh/templates/zshrc.zsh-template /home/vagrant/.zshrc
usermod -s /bin/zsh vagrant
EOH
end

# Creates folder for apache
bash "Configure wordpress dir" do
    code <<-EOH
mkdir /home/vagrant/wordpress
chown vagrant /home/vagrant/wordpress
chgrp vagrant /home/vagrant/wordpress
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
php wp-cli.phar --info
mv wp-cli.phar /usr/local/bin/wp
chmod +x /usr/local/bin/wp
EOH
end

# Defines host
web_app "wordpress-workflow" do
  server_name "wordpress.local"
  server_aliases ["www.wordpress.local"]
  docroot "/home/vagrant/www"
  allow_override "All"
end


