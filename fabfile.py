# encoding: utf-8
import re, json
from fabric.api import cd, env, local, run, task, require
from fabric.contrib.project import rsync_project
from fabric.colors import green, red

@task
def enviro(env_key):
    '''
    Loads environment data from settings.json configuration file (local, staging, production).
    '''
    # import the json file
    try:
        with open('settings.json') as json_data:
            config = json.load(json_data)
            json_data.close()
    except:
        print red("Error reading the file settings.json. Please verify that the file exists.")

    # validate ambiente variable
    if env_key in ['local','staging','production']:
        # Define basic environment variables
        print 'Loading environment configuration for: ' + env_key
        env.env = env_key
        env.title = config['SITE_CONFIG']['environments'][env_key]['title']
        env.url = config['SITE_CONFIG']['environments'][env_key]['url']
        env.version = config['SITE_CONFIG']['version']
        env.locale = config['SITE_CONFIG']['locale']
        env.theme = config['SITE_CONFIG']['theme']
        env.plugins = config['PLUGINS_CONFIG']
        env.custom_plugins = config['CUSTOM_PLUGINS_CONFIG']

        # Wordpress site directory path
        env.site_dir = config['SITE_CONFIG']['environments'][env_key]['site_dir']
        print green('Site directory configured as: ' + env.site_dir)
        # Project directory path (themes,plugins,etc.) 
        env.wordpress_dir = config['SITE_CONFIG']['environments'][env_key]['wordpress_dir']
        print green('Project directory configured as: ' + env.wordpress_dir)
        # Validate proper format of directory paths
        envverify()

        #Load SSH Configuration 
        try:
            env.user = config['SITE_CONFIG']['environments'][env_key]['ssh_user']
            env.hosts = config['SITE_CONFIG']['environments'][env_key]['ssh_hosts']
            print green('SSH Credentials loaded as (user : ' + env.user + ' host: ' + env.hosts[0]) + ')'
        except:# If no ssh user is defined, the default vagrant settings are used
            # User
            env.user = 'vagrant'
            # Connects to local SSH (routed to VM through port)
            env.hosts = ['127.0.0.1:2222']
            # Loads Vagrant ssh key pair
            result = local('vagrant ssh-config | grep IdentityFile', capture=True)
            env.key_filename = result.split()[1].replace('"', '')
            print green('Local SSH key pair loaded')

        # Define WP-Admin credentials
        env.admin_user = config['SITE_CONFIG']['environments'][env_key]['admin_user']
        env.admin_password = config['SITE_CONFIG']['environments'][env_key]['admin_password']
        env.admin_email = config['SITE_CONFIG']['environments'][env_key]['admin_email']
        print green('WP-Admin User Configured')

        # Define MySql credentials
        env.dbname = config['SITE_CONFIG']['environments'][env_key]['dbname']
        env.dbuser = config['SITE_CONFIG']['environments'][env_key]['dbuser']
        env.dbpassword = config['SITE_CONFIG']['environments'][env_key]['dbpassword']
        env.dbhost = config['SITE_CONFIG']['environments'][env_key]['dbhost']
        print green('MySQL credentials configured')

    else:# El ambiente no existe
        print red('The environment ' + env_key + ' does not exist.')


@task
def envverify():
    '''
    Verifies that the directories provided in settings are well formed
    '''
    require('site_dir')
    require('wordpress_dir')
    ok = True

    if not re.search('/$', env.site_dir):
        print red('The variable for site_dir in your settings.json must be a folder (Include trailing / )')
        ok = False

    if not re.search('/$', env.wordpress_dir):
        ok = False
        print red('The variable for wordpress_dir in your settings.json must be a folder (Include trailing / )')

    if env.wordpress_dir == env.site_dir:
        ok = False
        print red('The site_dir and wordpress_dir cannot be the same.')

    if ok:
        print green('Environment directories are configured correctly.')


@task
def bootstrap():
    '''
    Creates the database with test data, activates apache rewrite module, and starts wordpress install
    '''
    require('env')
    # Crea la base de datos
    run('''
        echo "DROP DATABASE IF EXISTS {0}; CREATE DATABASE {0};
        "|mysql --batch --user={1} --password={2} --host={3}
        '''.
        format(
           env.dbname,
           env.dbuser,
           env.dbpassword,
           env.dbhost
        ))
    # Activa modulo de apache
    run('a2enmod rewrite')
    wordpress_install()


@task
def wordpress_install():
    '''
    Downloads specified version of WordPress, creates wp-config file, installs into db, and sets up themes and plugins
    '''
    require("wordpress_dir")
    require("site_dir")
    require('env')
    #Downloads wordpress
    run('''
        wp core download --version={0} --path={1} --locale={2} --force
        '''.format(
        env.version,
        env.wordpress_dir,
        env.locale,
        ))
    #creates config
    run('''
        wp core config --dbname={0} --dbuser={1} \
            --dbpass={2} --path={3}
        '''.format(
        env.dbname,
        env.dbuser,
        env.dbpassword,
        env.wordpress_dir,
        ))
    #Installs into db
    run('''
        wp core install --url="{0}" --title="{1}" \
        --admin_user="{2}" --admin_password="{3}" \
        --admin_email="{4}" --path={5}
        '''.format(
        env.url,
        env.title,
        env.admin_user,
        env.admin_password,
        env.admin_email,
        env.wordpress_dir,
        ))
    #Creates simbolic link to themes and plugins
    run('''
       rm -rf {1}wp-content/themes &&
       ln -s {0}themes {1}wp-content
       '''.format(
        env.site_dir,
        env.wordpress_dir
        ))
    run('''
        rm -rf {0}wp-content/plugins
        '''.format(
        env.site_dir
        ))

    activate_theme()
    install_plugins()


@task
def activate_theme():
    '''
    Activates theme specified in settings.json for wordpress installation
    '''
    require("wordpress_dir")

    with cd(env.wordpress_dir):
        run('''
            wp theme activate {0}
            '''.format(
            env.theme
            ))


@task
def install_plugins():
    '''
    Installs all plugins and initializes per the settings.json parameters
    '''
    require("wordpress_dir")
    require("site_dir")

    for custom_plugin in env.custom_plugins:
        with cd(env.wordpress_dir):
            run('''
                if ! wp plugin is-installed {0};
                then
                    ln -s {1}plugins/{0} {2}wp-content/plugins/;
                fi
                '''.format(
                custom_plugin['name'],
                env.site_dir,
                env.wordpress_dir
                ))

            activate = "activate"
            if not custom_plugin['active']:
                activate = "deactivate"

            run('''
                wp plugin {0} {1}
                '''.format(
                activate,
                custom_plugin['name']
                ))
    # Installs 3rd party plugins
    with cd(env.wordpress_dir):
        for plugin in env.plugins:
            version = ""
            activate = "activate"

            if plugin['version'] != 'stable':
                version = ' --version=' + plugin['version']

            run('''
                if ! wp plugin is-installed {0};
                then
                    wp plugin install {0} {1};
                fi
                '''.format(
                plugin['name'],
                version
                ))

            if not plugin['active']:
                activate = "deactivate"

            run('''
                wp plugin {0} {1}
                '''.format(
                activate,
                plugin['name']
                ))

@task
def import_data():
    '''
    Imports data from database/data.sql
    '''
    require("site_dir")
    require("wordpress_dir")
    require("env")
    run('''
        mysql -u {0} -p{1} {2} --host={3} < {4}database/data.sql
        '''.format(
        env.dbuser,
        env.dbpassword,
        env.dbname,
        env.dbhost,
        env.site_dir
        ))
    with cd(env.wordpress_dir):  # Changes the domain
        run('''
            wp option update home http://{0} &&
            wp option update siteurl http://{0}
            '''.format(
            env.url
        ))
        #changes the user
        run('''
            wp user update {0} --user_pass={1} --user_email={2}
            '''.format(
            env.admin_user,
            env.admin_password,
            env.admin_email
            ))

@task
def export_data():
    '''
    Exports data to database/data.sql
    '''
    require("site_dir")
    require("wordpress_dir")
    require("env")
    run('''
       mysqldump -u {dbuser} -p{dbpassword} {dbname} --host={dbhost} --no-create-info  > {sitedir}database/data.sql
       '''.format(
       sitedir=env.site_dir, **env.env
       ))

@task
def resetdb():
    '''
    Deletes database and recreates it
    '''
    require('site_dir')
    require('env')
    run('''
        echo "DROP DATABASE IF EXISTS {0};
        CREATE DATABASE {0};
        "|mysql --batch --user={1} --password={2} --host={3}
        '''.format(
        env.dbname,
        env.dbuser,
        env.dbpassword,
        env.dbhost,
        )
        )


@task
def reset_all():
    '''
    Deletes entire wordpress installation and database and re-installs from scratch
    '''
    require('wordpress_dir')
    run('''rm -rf {0}*'''.format(env.wordpress_dir))
    resetdb()
    bootstrap()


@task
def deploy():
    '''
    Syncs modified files and activates plugins in the enviroment specified
    '''
    require("wordpress_dir")
    require("site_dir")
    require("env")
    rsync_project(
        remote_dir=env.site_dir,
        local_dir='src/',
        delete=False
    )
    install_plugins()
    print green('Deploy was successful.')


@task
def wordpress_upgrade():
    '''
    Downloads new version specified in settings.json and upgrades WordPress
    '''
    require("wordpress_dir")
    require("site_dir")
    require('env')
    with cd(env.wordpress_dir):
        current_ver = run(''' wp core version''')
        request_ver = env.version
    if request_ver > current_ver:
        #Upgrades wordpress based on settings.py options
        run('''
            wp core update --version={0} --path={1} --locale={2} 
            '''.format(
            env.version,
            env.wordpress_dir,
            env.locale
            ))
        print green('Upgrade to version ' + request_ver + ' was successful.')
    else:
        print red("The WordPress version in settings.py ("+ request_ver + ") must be greater than actual version (" + current_ver + ")")

@task
def wordpress_downgrade():
    '''
    Downloads new version specified in settings.json and downgrades WordPress
    '''
    require("wordpress_dir")
    require("site_dir")
    require('env')
    with cd(env.wordpress_dir):
        current_ver = run(''' wp core version''')
        request_ver = env.version
    if request_ver < current_ver:
        #Upgrades wordpress based on settings.py options
        run('''
            wp core update --version={0} --path={1} --locale={2} --force
            '''.format(
            env.version,
            env.wordpress_dir,
            env.locale
            ))
        print green('Downgrade to version ' + request_ver + ' was successful.')
    else:
        print red("The WordPress version in settings.py (" + request_ver + ") must be less than actual version (" + current_ver + ")")
