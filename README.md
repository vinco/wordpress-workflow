# WordPress Workflow

This project intents to give a standarized way to develop pages on wordpress. 


## Requirements

+ [Vagrant](http://www.vagrantup.com/)
+ [Vagrant hostsupdater](https://github.com/cogitatio/vagrant-hostsupdater)
+ [Python](http://www.python.org/)
+ [Fabric](http://www.fabfile.org/)
+ [fabutils](https://github.com/vinco/fabutils)


## Setup

1. Create a directory wich will contain your wordpress project

    ```bash
    $ mkdir my-new-project
    $ cd my-new-project
    ```

2. Init your repository

    ```bash
    $ git init
    ```

3. Clone this repo in your project's root directory

    ```bash
    $ git submodule add https://github.com/vinco/wordpress-workflow.git
    ```

4. Run the `startProject.sh` script to create the WordPress Workflow scaffolding

    ```bash
    $ wordpress-workflow/startProject.sh
    ```

## Workflow

After runing the setup, the default structure in your root directory will be as follows:

```bash
 . 
 ├── environments.json
 ├── settings.json
 ├── fabfile.py
 ├── src
 │   ├── database
 │   ├── init
 │   ├── plugins
 │   └── themes
 └── Vagrantfile
```

### environments.json

This file contains the description of the environments where your project will
be running. By default, it is populated with the `vagrant` environment that
defines all the required paramaters to interact with the development Vagrant VM.

You must append the definition of your live devel, staging, production and any
environment that you require.

```json
# environments.json
{
    "vagrant": {
        "...": "..."
    },
    "devel": {
        "user": "my-user",
        "group": "www-data",
        "hosts": ["my-host.com"],
        "site_dir": "/srv/www/my-site.com/public/",
        "wordpress_dir": "/srv/www/my-site.com/workflow/",
        "command_prefixes": [
            "/srv/www/my-site-com/env/activate"
        ]
    }
}
```

Note that:

+ You must define a user, group and an array of hosts for your environment.
+ Every directory path must end with a slash (/).
+ You can define an array of command prefixes that should be activated before a
  command is run in an environment. You must only list the path to your prefix scripts.

To run a task in an environment you must call the facbric's `environment` task
specifying with a colon the name of the environment.

```bash
# To run a task in the Vagrant VM
$ fab environment:vagrant ...

# To run a task in the statging environment
$ fab environment:devel ...
```


### settings.json

This file contains the general project configuration, you need to set it before
installing wordpress or running the fabric commands.

```json
{
    "version": "4.1.1",
    "locale": "es_ES",
    "theme": "yourtheme",
    "plugins": [
        {
            "name": "wordpress-seo",
            "active": true,
            "version": "stable"
        }
    ],
    "custom_plugins" : [
        {
            "name": "myPlugin",
            "active": true
        }
    ]

}

```

You need to have the `theme` in `src/themes/` otherwise the installation will fail.

Every plugin you specify in `plugins` must be a official plugin in wordpress.org/plugins,
and will be installed for you.

Any plugin in `custom_plugins` must be placed on `src/plugins/` sinces the plugins
won't be downloaded and are intended for your code.

(You can set the version and locale to whatever you need for your project)

Now you can install wordpress on your vagrant machine by running the following command:

```
$ fab environment:vagrant bootstrap
```

This will Create the database, install the version of wordpress you specified, activate all plugins, and set the theme. 
If you get any errors durring the setup processes you will have to fix the error and then run "$ fab vagrant reset_all" which will clean up the failed installation and automatically re-run bootstrap.


### fabfile.py

This file contains the core functionality of wpflow, it has tasks that can be
executed both in vagrant virtual machine as well as in the server (Q.A., Dev, Production)
these tasks need to be executed in the general form:

```bash
$ fab environment:name task1 task2 ... task3
```

For example if you want to sync files to devel and the install plugins the command would be

```bash
$ fab environment:devel deploy install_plugins
```

Available commands:
```
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


### Directories

All of your development should be placed in the src/ directories:

src/database: All .sql files should be placed here
src/init:     At the moment this should be empty
src/plugins:  All the plugins you're developing or modifying, note that
              any wordpress plugins not made by you should not be in here
src/themes:   All the themes needed for your project, if you're not using it
              it should not be here 


## Access

You can now browse to http://wordpress.local where you can find you installation of wordpress.
Use the username and password from your settings.py file to access the admin desktop http://wordpress.local/wp-admin

## Documentation

Just after `startProject.sh` has finished you can enter to http://wordpress-workflow.local to see the entire
project documentation.
