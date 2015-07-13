# -*- coding: utf-8 -*-
import sys
import json
import os
from fabric.api import cd, env, run, task, require, sudo, local
from fabric.colors import green, red, white, yellow, blue
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.operations import get
from fabric import state
from fabutils import boolean

from fabutils.env import set_env_from_json_file
from fabutils.tasks import ursync_project, ulocal, urun


@task
def environment(env_name, debug=False):
    """
    Creates the configurations for the environment in which tasks will run.
    """
    schemas_dir = "wordpress-workflow/json_schemas/"
    state.output['running'] = boolean(debug)
    state.output['stdout'] = boolean(debug)
    print "Establishing environment " + blue(env_name, bold=True) + "..."
    try:
        set_env_from_json_file(
            'environments.json',
            env_name,
            schemas_dir + "environment_schema.json"
        )
        if env_name == "vagrant":
            result = ulocal('vagrant ssh-config | grep IdentityFile',
                            capture=True)
            env.key_filename = result.split()[1].replace('"', '')

    except ValueError:
        print red("environments.json has wrong format.", bold=True)
        sys.exit(1)

    try:
        set_env_from_json_file(
            'settings.json',
            schema_path=schemas_dir + "settings_schema.json"
        )

    except ValueError:

        print red("settings.json has wrong format.", bold=True)
        sys.exit(1)


@task
def bootstrap():
    """
    Creates the database, test information and enables rewrite.
    """
    require('dbname', 'dbuser', 'dbpassword', 'dbhost')
    print "Creating local environment."
    # Creates database
    run("""
        echo "DROP DATABASE IF EXISTS {dbname}; CREATE DATABASE {dbname};
        "|mysql --batch --user={dbuser} --password=\"{dbpassword}\" --host={dbhost}
        """.format(**env))
    # Enables apache module
    run('sudo a2enmod rewrite')
    wordpress_install()


@task
def create_config(debug=False):
    """
    Writes wordpress configurations
    """
    require('public_dir', 'dbname', 'dbuser', 'dbpassword')

    block_wordpress_php = """--extra-php <<PHP
                          define('DISALLOW_FILE_EDIT', true);
                          define('DISALLOW_FILE_MODS', true);
                          define('WP_AUTO_UPDATE_CORE', false);
                          """

    debug_php = ""
    if boolean(debug):
        debug_php = """
                    define('WP_DEBUG', true);
                    define('WP_DEBUG_LOG', true);
                    """

    env['extra_php'] = block_wordpress_php + debug_php

    print "Setting debug mode to: {0}".format(debug)

    if exists("{public_dir}wp-config.php".format(**env)):
        run("rm {public_dir}wp-config.php".format(**env))

    run("""
        wp core config --dbname={dbname} --dbuser={dbuser} \
        --dbpass=\"{dbpassword}\" --path={public_dir} --dbhost={dbhost} {extra_php}
        """.format(**env))


@task
def set_debug_mode(debug=False):
    """
    Changes debug mode, false by default
    """
    create_config(debug)


@task
def wordpress_install():
    """
    Downloads the wordpress version specified in settings.json and installs the database.
    """
    require('wpworkflow_dir', 'public_dir', 'dbname', 'dbuser', 'dbpassword')
    require('url', 'title', 'admin_user', 'admin_password', 'admin_email')

    print "Downloading wordpress..."
    #Downloads wordpress
    run('wp core download --version={version} --path={public_dir} '
        '--locale={locale} --force'.format(**env))

    print "Creating wordpress configurations..."
    #creates config
    create_config()

    print "Installing wordpress..."
    #Installs into db
    run('wp core install --url="{url}" --title="{title}" '
        '--admin_user="{admin_user}" --admin_password="{admin_password}" '
        ' --admin_email="{admin_email}" --path={public_dir}'.format(**env))

    print "Installing wordpress-workflow..."
    #Creates simbolic link to themes
    run('rm -rf {public_dir}wp-content/themes &&  '
        'ln -s {wpworkflow_dir}themes {public_dir}wp-content'.format(**env))

    install_plugins()
    activate_theme()


@task
def activate_theme():
    """
    Activates the selected theme in the current wordpress installation.
    """
    require('public_dir', 'theme')

    print "Activating theme " + blue(env.theme, bold=True) + "..."
    with cd(env.public_dir):
        run('wp theme activate {0}'.format(env.theme))


@task
def install_plugins():
    """
    Installs plugins and initialize according to the settings.json file.
    """
    require('public_dir', 'wpworkflow_dir')

    check_plugins()
    print "Installing plugins..."
    for custom_plugin in env.get("custom_plugins", []):
        print "Installing : " + blue(custom_plugin['name'], bold=True) + "..."
        with cd(env.public_dir):
            run("""
                if ! wp plugin is-installed {0};
                then
                    ln -s {1}plugins/{0} {2}wp-content/plugins/;
                fi
                """.format(
                custom_plugin['name'],
                env.wpworkflow_dir,
                env.public_dir
                ))

            activate = "activate"
            if not custom_plugin['active']:
                activate = "deactivate"

            run("""
                wp plugin {0} {1}
                """.format(
                activate,
                custom_plugin['name']
                ))
    # Installs 3rd party plugins
    with cd(env.public_dir):
        for plugin in env.get("plugins", []):
            print "Installing : " + blue(plugin['name'], bold=True) + "..."
            version = ""
            activate = "activate"

            if plugin['version'] != 'stable':
                version = ' --version=' + plugin['version']

            run("""
                if ! wp plugin is-installed {0};
                then
                    wp plugin install {0} {1};
                fi
                """.format(
                plugin['name'],
                version
                ))

            if not plugin['active']:
                activate = "deactivate"

            run("""
                wp plugin {0} {1}
                """.format(
                activate,
                plugin['name']
                ))


@task
def change_domain():
    """
    Changes the project's domain according to the url configuration from
    environment.json
    """
    require('url')

    print ("Making actions to change project's url to: "
        + blue(env.url, bold=True) + "...")

    with cd(env.public_dir):
        print "Reloading vagrant virtual machine..."
        local("vagrant halt")
        local("vagrant up")

        print "Changing project url configuration..."
        run("""
            wp option update home http://{url} &&\
            wp option update siteurl http://{url}
            """.format(**env))


@task
def import_data(file_name="data.sql"):
    """
    Imports the database to given file name. database/data.sql by default.
    """
    require('wpworkflow_dir', 'dbuser', 'dbpassword', 'dbhost')
    require('admin_user', 'admin_password', 'admin_email', 'url')

    env.file_name = file_name

    print "Importing data from file: " + blue(file_name, bold=True) + "..."
    run("""
        mysql -u {dbuser} -p\"{dbpassword}\" {dbname} --host={dbhost} <\
        {wpworkflow_dir}database/{file_name} """.format(**env))

    with cd(env.public_dir):

        # Changes the domain
        run("""
            wp option update home http://{url} &&\
            wp option update siteurl http://{url}
            """.format(**env))

        # changes the user
        run("""
            wp user update {admin_user} --user_pass=\"{admin_password}\"\
            --user_email={admin_email}
            """.format(**env))


@task
def export_data(file_name="data.sql", just_data=False):
    """
    Exports the database to given file name. database/data.sql by default.
    """
    require('wpworkflow_dir', 'dbuser', 'dbpassword', 'dbname', 'dbhost')

    export = True

    env.file_name = file_name
    if just_data:
        env.just_data = "--no-create-info"
    else:
        env.just_data = " "

    if exists('{wpworkflow_dir}database/{file_name}'.format(**env)):
        export = confirm(
            yellow(
                '{wpworkflow_dir}database/{file_name} '.format(**env)
                +
                'already exists, Do you want to overwrite it?'
            )
        )

    if export:
        print "Exporting data to file: " + blue(file_name, bold=True) + "..."
        run(
            """
            mysqldump -u {dbuser} -p\"{dbpassword}\" {dbname} --host={dbhost}\
            {just_data} > {wpworkflow_dir}database/{file_name}
            """.format(**env)
        )
    else:
        print 'Export canceled by user'
        sys.exit(0)


@task
def resetdb():
    """
    Drops the database and recreate it.
    """
    require('dbname', 'dbuser', 'dbpassword', 'dbhost')
    print "Dropping database..."
    run("""
        echo "DROP DATABASE IF EXISTS {dbname};
        CREATE DATABASE {dbname};
        "|mysql --batch --user={dbuser} --password=\"{dbpassword}\" --host={dbhost}
        """.format(**env))


@task
def reset_all():
    """
    Deletes all the wordpress installation and starts over.
    """
    require('public_dir')
    print "Deleting directory content: " + blue(env.public_dir, bold=True) + "..."
    run("""rm -rf {0}*""".format(env.public_dir))
    resetdb()


@task
def sync_files():
    """
    Sync modified files and establish necessary permissions in selected environment.
    """
    require('group', 'wpworkflow_dir', 'public_dir')

    print white("Uploading code to server...", bold=True)
    ursync_project(
        local_dir='./src/',
        remote_dir=env.wpworkflow_dir,
        delete=True,
        default_opts='-chrtvzP'
    )

    print white("Estableciendo permisos...", bold=True)
    run('chmod -R o-rwx {0}'.format(env.wpworkflow_dir))
    run('chmod -R o-rwx {0}'.format(env.public_dir))
    run('chgrp -R {0} {1}'.format(env.group, env.wpworkflow_dir))
    run('chgrp -R {0} {1}'.format(env.group, env.public_dir))

    print green(u'Successfully sync.')


@task
def wordpress_upgrade():
    """
    Downloads the new wordpress version specified in settings.json and upgrade it.
    """
    require('public_dir', 'wpworkflow_dir', 'version', 'locale')
    with cd(env.public_dir):
        current_ver = run(""" wp core version""")
        request_ver = env.version

    if request_ver > current_ver:
        run("""
            wp core update --version={version} --path={public_dir}
            --locale={locale} """.format(**env))

        print green('Upgrade to versión ' + request_ver + ' sucessfull.')

    else:
        print red("""
                  Current wordpress version in settings.json {0}
                  must be later than current version {1}
                  """.format(request_ver, current_ver))


@task
def wordpress_downgrade():
    """
    Downloads the new specified wordpress version in settings.json and downgrade it
    """
    require('version', 'public_dir', 'locale')

    with cd(env.public_dir):
        current_ver = run(""" wp core version""")
        request_ver = env.version

    if request_ver < current_ver:
        run("""
            wp core update --version={version} --path={public_dir}
            --locale={locale} --force """.format(**env))

        print green('Downgrade to versión ' + request_ver + ' success.')
    else:
        print red("""
                  The wordpress version in settings.json {0}
                  must be earlier than current version {1}
                  """.format(request_ver, current_ver))


@task
def set_webserver(webserver="nginx"):
    """
    Changes project's web server, nginx or apache2 available, nginx by default.
    """
    require('public_dir')

    if webserver == "apache2":
        sudo("service nginx stop")
        sudo("a2enmod rewrite")
        with open('wordpress-workflow/defaults/htaccess') as htaccess:
            urun(" echo '{0}' > {1}.htaccess".
                 format(htaccess.read(), env.public_dir))

        sudo("service apache2 start", pty=False)

    else:
        sudo("service apache2 stop")
        if exists("{0}.htaccess".format(env.public_dir)):
            urun("rm {0}.htaccess".format(env.public_dir))
        sudo("service nginx start")

    print "Web server switched to " + blue(webserver, bold=True) + "."


@task
def upgrade_plugin(plugin_name=None):
    """
    Updates a plugin to specified version in settings.json.
    """
    require('public_dir')
    if not plugin_name:
        print red("Plugin name required to update.")
        sys.exit(0)

    installed_plugins = json.loads(
        run('wp plugin list --format=json --path={0}'.  format(env.public_dir))
    )
    installed_plugin = search_plugin(plugin_name, installed_plugins)
    plugin = search_plugin(plugin_name)
    if plugin:
        print (
            u'Updating plugin ' + plugin_name + u' from version ' +
            installed_plugin['version'] + u' to versión ' + plugin['version'] + "."
        )
        run('wp plugin update {0} --version={1} --path={2}'.
            format(plugin_name, plugin['version'], env.public_dir))
        print green("Plugin " + plugin_name + " updated") + "."


@task
def check_plugins():
    """
    Verifies installed versions of plugins.
    """
    require('public_dir')
    clean_plugins()
    installed_plugins = json.loads(
        run('wp plugin list --format=json --path={0}'.  format(env.public_dir))
    )
    # Verifies wich plugins have `stable` to give a warning
    stable_plugins = []
    for plugin in env.get("plugins", []):
        if plugin['version'] == 'stable':
            stable_plugins.append(plugin)
    if stable_plugins:
        print yellow(
            u'Plugins with no version specified have been found.'
            u' This is not an error but it is highly recomended to'
            u' specify the required version in settings.json\n'
        )
        for plugin in stable_plugins:
            installed_plugin = search_plugin(plugin['name'], installed_plugins)
            if(installed_plugin):
                version = installed_plugin['version']
            else:
                version = 'Not installed'
            print yellow(
                'Plugin: ' + plugin['name'] + u', Version '
                u'installed: ' + version
            )
    # Verifies upgrade-able
    upgrade = run('wp plugin update --dry-run --all --path={0}'.
                  format(env.public_dir))
    if upgrade != "No plugin updates available.":
        print yellow(
            u'Plugins that can be updated have been found'
            u' this can be done by changing the version in settings.json'
            u' and running the following command'
            u' `fab environment:environment_name upgrade_plugin:plugin_name`'
        )
        print yellow(upgrade)


@task
def clean_plugins():
    """
    Checks for installed plugins and removes the unused.
    """
    require('public_dir')
    installed_plugins = json.loads(
        run('wp plugin list --format=json --path={0}'.  format(env.public_dir))
    )
    plugins_to_delete = []
    print "Verifying installed plugins..."
    for installed_plugin in installed_plugins:
        if not search_plugin(installed_plugin['name']):
            plugins_to_delete.append(installed_plugin['name'])
    if plugins_to_delete:
        print yellow(
            u'There are plugins installed on wordpress '
            u'that are not specified in settings.json. '
            u'These plugins must be uninstalled before installing, '
            u'updating, or syncing new plugins.\n'
            u'The following list shows plugins that are not specified '
            u'in settings.json:'
        )
        count = 1
        for plugin in plugins_to_delete:
            print yellow(str(count) + ".- " + plugin)
            count = count + 1
        if confirm(yellow('Do you want to delete these plugins?')):
            for plugin in plugins_to_delete:
                run('wp plugin deactivate {0} --path={1}'.
                    format(plugin, env.public_dir))
                run('wp plugin uninstall {0} --path={1}'.
                    format(plugin, env.public_dir))
        else:
            sys.exit(0)


def search_plugin(plugin_searched, search_list=None):
    """
    Looks for a plugin in settings.json.
    """
    if search_list:
        for plugin in search_list:
            if plugin['name'] == plugin_searched:
                return plugin
        return None

    for plugin in env.get("plugins", []):
        if plugin['name'] == plugin_searched:
            return plugin

    for plugin in env.get("custom_plugins", []):
        if plugin['name'] == plugin_searched:
            return plugin

    return False


@task
def make_tarball(target_environment, tar_name="wordpress-dist"):
    """
    Generates a tallbar to upload to servers without ssh.
    """
    environment('vagrant')
    env.tmp_dir = "/home/vagrant/wordpress-dist/"
    env.tmp_dir_name = "wordpress-dist"
    env.host_string = env.hosts[0]

    check_plugins()

    if not os.path.exists('./dist/'):
        print "Creating dist folder..."
        os.makedirs('./dist/')

    # Creates necesary dirs
    print "Creating directory structure..."
    if exists(env.tmp_dir):
        urun('rm -rf {tmp_dir}'.format(**env))

    urun('mkdir {tmp_dir}'.format(**env))

    # Downloads
    print "Downloading and generating wordpress configuration..."
    #Downloads wordpress
    urun('wp core download --version={version} --path={tmp_dir} '
         '--locale={locale} --force'.format(**env))
    #creates config
    with open('environments.json', 'r') as json_file:
        db_config = json.load(json_file)[target_environment]
        db_config['tmp_dir'] = env.tmp_dir
        urun('wp core config --dbname={dbname} --dbuser={dbuser} '
             '--dbpass=\"{dbpassword}\" --skip-check --path={tmp_dir}'.format(**db_config))

    # Configure temp database
    create_database_command = '''
         echo "
             CREATE DATABASE {dbname};
             CREATE USER '{dbuser}'@'localhost' IDENTIFIED BY '{dbpassword}';
             GRANT ALL PRIVILEGES ON *.* TO '{dbuser}'@'localhost';
             FLUSH PRIVILEGES;
         "'''.format(**db_config)

    print "Configurating temporary database..."
    urun(
        create_database_command +
        '|mysql --batch --user={dbuser} --password=\"{dbpassword}\"'.format(**env)
    )

    # Install wodpress
    print "Installing temporary wordpress..."
    urun('wp core install --url="{url}" --title="{title}" '
         '--admin_user="{admin_user}" --admin_password="{admin_password}" '
         ' --admin_email="{admin_email}" --path={tmp_dir}'.format(**db_config))

    # Cleans default wordpress files
    urun('rm -rf {tmp_dir}wp-content/themes/*'.format(**env))
    urun('rm -rf {tmp_dir}wp-content/plugins/*'.format(**env))
    # Copy theme
    urun('cp -rf {wpworkflow_dir}themes/* {tmp_dir}wp-content/themes/'.
         format(**env))

    # Download all require plugins
    with cd(env.tmp_dir):
        for plugin in env.get("plugins", []):
            print "Downloading plugin: " + blue(plugin['name'], bold=True)
            urun(""" wp plugin install {0} """.format(plugin['name']))
    # Copy custom plugins
    for plugin in env.get("custom_plugins", []):
        env.plugin = plugin['name']
        print "Copying plugin: " + blue(plugin['name'], bold=True)
        urun(
            """
            cp -rf {wpworkflow_dir}plugins/{plugin} \
            {tmp_dir}wp-content/plugins
            """.format(**env)
        )
    # Download all require plugins
    print "Generating packaging..."
    env.tar_name = tar_name
    with cd(env.tmp_dir + ".."):
        urun('tar -czf {wpworkflow_dir}{tar_name}.tar.gz {tmp_dir_name}/*'
             .format(**env))
        os.rename(
            './src/{tar_name}.tar.gz'.format(**env),
            './dist/{tar_name}.tar.gz'.format(**env)
        )
    # Delete temp database
    print "Cleaning temporary data..."
    clean_database_command = '''
        echo "
            DROP USER '{dbuser}'@'localhost';
            DROP DATABASE {dbname};
        "'''.format(**db_config)
    urun(
        clean_database_command +
        '|mysql --batch --user={dbuser} --password=\"{dbpassword}\"'.format(**env)
    )
    urun('rm -rf {tmp_dir}'.format(**env))
    print green("Packaging generated in dist/{tar_name}.tar.gz".format(**env))


@task
def backup(tarball_name='backup', just_data=False):
    """
    Generates a backup copy of database and uploads
    """
    require('wpworkflow_dir', 'public_dir')

    env.tarball_name = tarball_name

    export_data(tarball_name + '.sql', just_data)

    print 'Preparing backup directory...'

    if not os.path.exists('./backup/'):
        os.makedirs('./backup/')

    if exists('{wpworkflow_dir}backup/'):
        run('rm -rf {wpworkflow}backup/')

    if not exists('{wpworkflow_dir}backup/'.format(**env)):
        run('mkdir {wpworkflow_dir}backup/'.format(**env))

    if not exists('{wpworkflow_dir}backup/database/'.format(**env)):
        run('mkdir {wpworkflow_dir}backup/database/'.format(**env))

    if not exists('{wpworkflow_dir}backup/uploads/'.format(**env)):
        run('mkdir {wpworkflow_dir}backup/uploads/'.format(**env))

    run(
        'mv {wpworkflow_dir}/database/{tarball_name}.sql '.format(**env)
        +
        '{wpworkflow_dir}/backup/database/'.format(**env)
    )

    print 'Copying uploads...'
    run('cp -r {public_dir}wp-content/uploads/* {wpworkflow_dir}backup/uploads/'.
        format(**env))

    print 'Creating tarball...'
    with cd(env.wpworkflow_dir):
        urun('tar -czf {tarball_name}.tar.gz backup/*'.format(**env))

    print 'Downloading backup...'
    download = True
    if os.path.exists('./backup/{tarball_name}.tar.gz'.format(**env)):
        download = confirm(
            yellow(
                './backup/{tarball_name}.tar.gz'.format(**env)
                +
                ' already exists, Do you want to overwrite it?'
            )
        )

    if download:
        get(
            '{wpworkflow_dir}{tarball_name}.tar.gz'.format(**env),
            './backup/{tarball_name}.tar.gz'.format(**env)
        )
    else:
        print red('Backup canceled by user')

    print 'Cleaning working directory...'
    run('rm -rf {wpworkflow_dir}backup/'.format(**env))
    run('rm {wpworkflow_dir}{tarball_name}.tar.gz'.format(**env))

    if download:
        print green(
            'Backup succesfully created at'
            +
            ' ./backup/{tarball_name}.tar.gz'.  format(**env)
        )


@task
def wordpress_workflow_upgrade(repository='origin', branch='master'):
    """
    Upgrades wordpress-workflow
    """
    #upgrades code to current master
    os.chdir('wordpress-workflow')
    ulocal('git fetch origin')
    ulocal('git pull {0} {1}'.format(repository, branch))

    os.chdir('../')
    #Updates vagrant provision
    ulocal('wordpress-workflow/startProject.sh')
    ulocal('vagrant provision')
    print green('wordpress-workflow upgraded', bold=True)
