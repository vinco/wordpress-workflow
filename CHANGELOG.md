
# Version 0.4.0 (2018-01-10)
    * Fix text valiator of pull-request in danger #55
    * Update to php 7.0
# Version 0.3.8 (2017-12-17)
    * Fix text validator of pull-request in danger.
# Version 0.3.7 (2017-12-17)
    * Add task configure_circle_ci to wordpress workflow.
# Version 0.3.6 (2017-08-14)
    * Add task import_backup to wordpress workflow.

# Version 0.3.5 (2017-08-09)
    * Add task version to show wordpress workflow version.

# Version 0.3.4 (2017-08-09)
    * Rename site-available wordpress file to wordpress.conf.
    * Fix template enviroment.json, set corret value from user.
    * Remove provision/templates/httpd.conf

# Version 0.3.3 (2017-08-04)
    * Make it optional to set permissions when synchronizing
    * Change vagrant box to "ubuntu/xenial32"
    
# Version 0.3.2 (2016-08-17)
    * Add prefix table wordpress
    * Fix permissions uploads folder
    
# Version 0.3.1 (2016-07-01)
    * Add verification checksums from core files
    * Fixes password with dollar sign
    * Fix error locale to upgrade and downgrade wordpress
    * Add confirm task to delete database
    * Set group www-data to vagrant share files
    * Add task to install only one plugin
    * Add possibility to create custom tasks

# Version 0.3.0 (2015-06-13)
    * Add code verification
    * Fixes password quotation

# Version 0.2.5 (2015-04-28)
    * Improves documentation
    * Adds change_domain command

# Version 0.2.4 (2015-04-20)
    * Adds gitignore entries
    * Add warning to bakcup overwrite
    * Adds upgrade command

# Version 0.2.3 (2015-04-13)

    * Fixes nginx cache files
    * Fixes nginx buffer_size
    * Adds backup method

# Version 0.2.2 (2015-03-25)

    * Fixes bug in set_webserver
    * Disables theme editor in wp-admin
    * Disables plugin updater in wp-admin

# Version 0.2.1 (2015-03-23)

    * Changes tasks description to english
    * Fixes [issue #14] (https://github.com/vinco/wordpress-workflow/issues/14)
    * Adds method set_debug_mode

# Version 0.2.0 (2015-03-17)

    * Replaces Chef with shell script
    * Makes messages prettier
    * Adds clean_plugins task
    * Adds check_plugins task
    * Makes environment a json file
    * Makes settings a json file
    * Adds documentation in wordpres-workflow.local

# Version 0.1.0

    * Initial release
