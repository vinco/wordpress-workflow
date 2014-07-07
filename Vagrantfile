# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise32"

  config.omnibus.chef_version = :latest


  # Port fowarding 
  config.vm.network :forwarded_port, guest: 8000, host: 8000
  
  # Private IP  
  config.vm.network :private_network, ip: "192.168.33.77"

  # Hosts
  config.vm.hostname = "www.wordpress-workflow.local"
  config.hostsupdater.aliases = ["wordpress-workflow.local", "wordpress.local"]


  # Shared folders.
  config.vm.synced_folder "src", "/home/vagrant/wordpress-workflow"


  # Provision
  config.vm.provision :chef_solo do |chef|
    chef.custom_config_path = "./vagrant/Vagrantfile.chef"
    chef.cookbooks_path = "./vagrant/cookbooks"
    chef.json = {
      "mysql" => {
        "server_root_password" => "password",
       "server_repl_password" => "password",
        "server_debian_password" => "password"
      }
	}
    chef.run_list = [
        "recipe[wordpress]"
    ]
  end

end
