# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  environments_json_path = "environments.json"
  vagrant_config = (JSON.parse(File.read(environments_json_path)))['vagrant']

  config.vm.box = "ubuntu/xenial32"
  config.vm.box_url = "https://app.vagrantup.com/ubuntu/boxes/xenial32"
  config.vm.box_version = "20180224.0.0"

  #provisioning
  config.vm.provision "shell", path: "wordpress-workflow/provision/preprovision.sh"
  config.vm.provision "file", source:"wordpress-workflow/provision/templates/", destination: "/home/vagrant/"
  config.vm.provision "shell", path: "wordpress-workflow/provision/provision.sh"

  # Private IP
  config.vm.network :private_network, ip: "192.168.33.77"

  # Hosts
  config.vm.hostname = "www.wordpress-workflow.local"
  config.hostsupdater.aliases = ["wordpress-workflow.local", vagrant_config['url']]

  # Shared folders.
  config.vm.synced_folder "src", "/home/vagrant/wordpress-workflow",
    owner: "vagrant",
    group: "www-data",
    mount_options: ["dmode=775,fmode=764"]
  config.vm.synced_folder "wordpress-workflow/documentation", "/home/vagrant/workflow-documentation"

  # Provider
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
  end

end
