# Wordpress workflow

This project intends to give a standarized way to develop pages on wordpress. It never aims to develop plugins for diferent wordpress versions, to do that
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

In linux it should look something like this:

```
$ mkdir my-new-project
$ cd my-new-project
$ git init
$ git clone https://github.com/vinco/wordpress-workflow.git vagrant
$ vagrant/startProject.sh

```

## settings.json

This file contains the general project configuration, you need to set it before
installing wordpress or running the fabric commands

For your local environment, be sure to set the [url] of your site to "wordpress.local" in settings.json

```
"environments": {
            "local":{
                    "url": "wordpress.local",
                    "title": "WP Project",
        ...
```

Make sure that any custom plugins specified in your settings.json actually exist in /src/plugins or this will cause errors when installing wordpress

```
   "CUSTOM_PLUGINS_CONFIG" : [
       {
            "name": "plugin-name" 
            "active: TRUE"
       }
```

Before you can run the install command you need to set your theme or create a new custom theme folder in your local /src/themes/ directory.
Then set your custom theme in the settings.json or use the default that comes with your version of WordPress as follows:

```
"SITE_CONFIG" :{
    "version": "4.1",
    "locale": "es_ES",
    "theme": "twentyfourteen"
```
(You can set the version and locale to whatever you need for your project)

Now you can install wordpress on your vagrant machine by running the following command:

```
$ fab enviro:local bootstrap
```
This will Create the database, install the version of wordpress you specified, install and activate all plugins, and set the theme. 
If you get any errors durring the setup processes you will have to fix the error and then run "$ fab enviro:local reset_all" which will clean up the failed installation and automatically re-run bootstrap.


# Access

You can now browse to http://wordpress.local where you can find you installation of wordpress.
Use the username and password from your settings.json file to access the admin desktop http://wordpress.local/wp-admin

## fabfile.py

This file contains the core functionality of wpflow, it has tasks that can be
executed both in vagrant virtual machine as well as in the server (Q.A., Dev, Production)
these tasks need to be executed in the general form:

``$ fab environment task1 task2 ... task3``

For example if you want to sync files to staging and the install plugins the command would be

```
$ fab enviro:staging deploy install_plugins

Available commands:

enviro              Selects the environment configuration you wish to use (local,staging,production).
envverify           Verifies that the directories provided in settings are well formed
bootstrap           Creates the database with test data, activates apache rewrite module, and starts wordpress install
wordpress_install   Downloads specified version of WordPress, creates wp-config file, installs into db, and sets up themes and plugins
activate_theme      Activates theme specified in settings.json for wordpress installation
install_plugins     Installs all plugins and initializes per the settings.json parameters
import_data         Imports data from database/data.sql
export_data         Exports current database to database/data.sql
resetdb             Deletes database and recreates it
reset_all           Deletes entire wordpress installation and database and re-installs from scratch
deploy              Syncs modified files and activates plugins in the enviroment specified
wordpress_upgrade   Downloads new version specified in settings.json and upgrades WordPress
wordpress_downgrade Downloads new version specified in settings.json and downgrades WordPress

```

You can list the available tasks by running ``fab --list``


# Workflow

The default structure in your root directory will be as follows:

 ```
 . 
 ├── fabfile.py 
 ├── settings.json
 ├── src
 │   ├── database
 │   ├── init
 │   ├── plugins
 │   └── themes
 ├── vagrant
 │
 └── Vagrantfile
 ```

## Folders

All of your development should be placed in the src/ folders:

src/database: All .sql files should be placed here
src/init:     At the moment this should be empty
src/plugins:  All the plugins you're developing or modifying, note that
              any wordpress plugins not made by you should not be in here
src/themes:   All the themes needed for your project, if you're not using it
              it should not be here 

