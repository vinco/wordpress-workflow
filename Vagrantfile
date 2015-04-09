# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  #provisioning
  config.vm.provision "shell", path: "wordpress-workflow/provision/preprovision.sh"
  config.vm.provision "file", source:"wordpress-workflow/provision/templates/", destination: "/home/vagrant/templates/"
  config.vm.provision "shell", path: "wordpress-workflow/provision/provision.sh"

  # Private IP  
  config.vm.network :private_network, ip: "192.168.33.77"

  # Hosts
  config.vm.hostname = "www.wordpress-workflow.local"
  config.hostsupdater.aliases = ["wordpress-workflow.local", "wordpress.local"]

  # Shared folders.
  config.vm.synced_folder "src", "/home/vagrant/wordpress-workflow"
  config.vm.synced_folder "wordpress-workflow/documentation", "/home/vagrant/workflow-documentation"

  # Provider
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
  end

end
