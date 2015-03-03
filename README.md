# Wordpress workflow

This project intents to give a standarized way to develop pages on wordpress. 

# Requirements

    * Vagrant 2
    * Fabric
    * Vagrant hostsupdater 

## vagrant plugins

In order to install the needed vagrant plugins run these commands

```
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

## settings.py

This file contains the general project configuration, you need to set it before
installing wordpress or running the fabric commands

Be sure to set the [url] of your site to "wordpress.local" in settings.py

```
'dev': {
        'url': 'wordpress.local',
        'title': 'New Project',
        ...
```

also comment out or remove the example custom plugin 'jetpak' as this will cause errors when installing wordpress

```
    # 'name': 'jetpack',
    # 'active': True
```

Before you can run the install command you need to download your theme or create a new custom theme folder in your local /src/themes/ directory.
For example if you want to use the worpress default "Twenty Fourteen" theme you would download and extract the theme as /src/themes/twentyfourteen
then in your settings.py file set your site config as follows:

```
SITE_CONFIG = {
    'version': '4.1.1',
    'locale': 'es_ES',
    'theme': 'twentyfourteen',
```
(You can set the version and locale to whatever you need for your project)

Now you can install wordpress on your vagrant machine by running the following command:

```
$ fab vagrant bootstrap
```
This will Create the database, install the version of wordpress you specified, activate all plugins, and set the theme. 
If you get any errors durring the setup processes you will have to fix the error and then run "$ fab vagrant reset_all" which will clean up the failed installation and automatically re-run bootstrap.


# Access

You can now browse to http://wordpress.local where you can find you installation of wordpress.
Use the username and password from your settings.py file to access the admin desktop http://wordpress.local/wp-admin

## fabfile.py

This file contains the core functionality of wpflow, it has tasks that can be
executed both in vagrant virtual machine as well as in the server (Q.A., Dev, Production)
these tasks need to be executed in the general form:

``$ fab environment task1 task2 ... task3``

For example if you want to sync files to dev and the install plugins the command would be

```
$ fab dev deploy install_plugins

Available commands:

activate_theme     Activates wordpress theme given in settings
bootstrap          Sets up wordpress installation for the first time
deploy             Syncs files to enviroment
envverify          Verifies the environment is created correctly
export_data        Exports current database to database/data.sql
import_data        Imports database from database/data.sql
install_plugins    Installs plugins and activates them according to settings
reset_all          Deletes all wordpress installment and runs bootstrap
resetdb            Drops database and creates it again (without data or structure)
vagrant            Local development environment (Vagrant virtual machine).
wordpress_install  Downloads wordpress version written in settings and creates database
```

You can list the available enviroments and task by running ``fab --list``


# Workflow

The default structure in your root directory will be as follows:

 ```
 . 
 ├── fabfile.py 
 ├── settings.py
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

