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
cd /home/vagrant/
sudo vagrant
wget https://raw.github.com/wp-cli/wp-cli.github.com/master/installer.sh 
chmod +x ./installer.sh
export HOME=/home/vagrant/
./installer.sh > ./wp.log
rm ./installer
echo "alias wp='/root/.wp-cli/bin/wp' ">> /home/vagrant/.zshrc
EOH
end

# Defines host
web_app "wordpress-workflow" do
  server_name "wordpress-workflow.local"
  server_aliases ["www.wordpress-workflow.local"]
  docroot "/home/vagrant/www"
  allow_override "All"
end


