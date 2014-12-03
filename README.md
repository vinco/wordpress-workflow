# Wordpress workflow

This project intents to give a standarized way to develop pages on wordpress. It never aims to develop plugins for diferent wordpress versions, to do that
you should go and checkout https://github.com/10up/varying-vagrant-vagrants wonderfull project. Actually this project is a mod of varying vagrant vagrants

# Requirements

    * Vagrant 2
    * Fabric
    * Vagrant omnibus
    * Vagrant hostsupdater 

## vagrant plugins

In order to install the needed vagrant plugins run these commands

```
$ vagrant plugin install vagrant-omnibus
$ vagrant plugin install vagrant-hostsupdater

```

# Setup

    1 create a folder wich will contain your wordpress project
    2 init your repository
    2 clone this repo in your project's root folder
    3 run the vagrant/startProject.sh
    4 run vagrant up in the vagrant folder

In linux you should something like this:

```
$ mkdir my-new-project
$ cd my-new-project
$ git init
$ git clone https://github.com/vinco/wordpress-workflow.git vagrant
$ vagrant/startProject.sh

```

# Workflow

All your work should be place in src/themes and src/plugins.

# Access

In your browser go to http://wordpress-workflow.local there you can find you installation of wordpress
