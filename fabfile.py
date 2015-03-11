# -*- coding: utf-8 -*-
import sys
import json
from fabric.api import cd, env, run, task, require
from fabric.colors import green, red, white, yellow
from fabric.contrib.console import confirm

from fabutils.env import set_env_from_json_file
from fabutils.tasks import ursync_project, ulocal


@task
def environment(env_name):
    """
    Crea la configuración para el entorno en el que correrán las tareas.
    """
    schemas_dir = "wordpress-workflow/json_schemas/"
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
        print red("El archivo environments.json está mal formado.", bold=True)
        sys.exit(1)

    try:
        set_env_from_json_file(
            'settings.json',
            schema_path=schemas_dir + "settings_schema.json"
        )

    except ValueError:

        print red("El archivo settings.json está mal formado.", bold=True)
        sys.exit(1)


@task
def bootstrap():
    """
    Crea la base de datos, información de prueba y activa rewrite
    """
    require('dbname', 'dbuser', 'dbpassword', 'dbhost')
    # Crea la base de datos
    run("""
        echo "DROP DATABASE IF EXISTS {dbname}; CREATE DATABASE {dbname};
        "|mysql --batch --user={dbuser} --password={dbpassword} --host={dbhost}
        """.format(**env))
    # Activa modulo de apache
    run('sudo a2enmod rewrite')
    wordpress_install()


@task
def wordpress_install():
    """
    Descarga la version de wordpress escrita en settings en instala la base
    de datos.
    """
    require('wpworkflow_dir', 'public_dir', 'dbname', 'dbuser', 'dbpassword')
    require('url', 'title', 'admin_user', 'admin_password', 'admin_email')

    #Downloads wordpress
    run('wp core download --version={version} --path={public_dir} '
        '--locale={locale} --force'.format(**env))

    #creates config
    run('wp core config --dbname={dbname} --dbuser={dbuser} '
        '--dbpass={dbpassword} --path={public_dir}'.format(**env))

    #Installs into db
    run('wp core install --url="{url}" --title="{title}" '
        '--admin_user="{admin_user}" --admin_password="{admin_password}" '
        ' --admin_email="{admin_email}" --path={public_dir}'.format(**env))

    #Creates simbolic link to themes
    run('rm -rf {public_dir}wp-content/themes &&  '
        'ln -s {wpworkflow_dir}themes {public_dir}wp-content'.format(**env))

    activate_theme()
    install_plugins()


@task
def activate_theme():
    """
    Activa el tema seleccionado en la instalacion de wordpress
    """
    require('public_dir', 'theme')

    with cd(env.public_dir):
        run('wp theme activate {0}'.format(env.theme))


@task
def install_plugins():
    """
    Instala plugins e inicializa segun el archivo settings
    """
    require('public_dir', 'wpworkflow_dir')

    clean_plugins()
    for custom_plugin in env.get("custom_plugins", []):
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
def import_data():
    """
    Importa la informacion de database/data.sql
    """
    require('wpworkflow_dir', 'dbuser', 'dbpassword', 'dbhost')
    require('admin_user', 'admin_password', 'admin_email', 'url')

    run("""
        mysql -u {dbuser} -p{dbpassword} {dbname} --host={dbhost} <
        {wpworkflow_dir}database/data.sql """.format(**env))

    with cd(env.wordpress_dir):  # Changes the domain
        run("""
            wp option update home http://{url} &&
            wp option update siteurl http://{url}
            """.format(**env))
        #changes the user
        run("""
            wp user update {admin_user} --user_pass={admin_password}
            --user_email={admin_email}
            """.format(**env))


@task
def export_data():
    """
    Exporta la base de datos a database/data.sql
    """
    require('wpworkflow_dir', 'dbuser', 'dbpassword', 'dbname', 'dbhost')
    run("""
       mysqldump -u {dbuser} -p{dbpassword} {dbname} --host={dbhost}
       --no-create-info  > {wpworkflow_dir}database/data.sql """.format(**env))


@task
def resetdb():
    """
    Elimina la base de datos y la vuelve a crear
    """
    require('dbname', 'dbuser', 'dbpassword', 'dbhost')

    run("""
        echo "DROP DATABASE IF EXISTS {dbname};
        CREATE DATABASE {dbname};
        "|mysql --batch --user={dbuser} --password={dbpassword} --host={dbhost}
        """.format(**env))


@task
def reset_all():
    """
    Borra toda la instación de wordpress e inicia de cero
    """
    require('public_dir')
    run("""rm -rf {0}*""".format(env.public_dir))
    resetdb()


@task
def sync_files():
    """
    Sincroniza los archivos modificados y establece los permisos necesarios en
    el entorno señalado.
    """
    require('group', 'wpworkflow_dir', 'public_dir')

    print white("Subiendo código al servidor...", bold=True)
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

    print green(u'Sincronización exitosa.')


@task
def wordpress_upgrade():
    """
    Descarga la nueva version de wordpress escrita en settings y hace el upgrade
    """
    require('public_dir', 'wpworkflow_dir', 'version', 'locale')
    with cd(env.public_dir):
        current_ver = run(""" wp core version""")
        request_ver = env.version

    if request_ver > current_ver:
        run("""
            wp core update --version={version} --path={public_dir}
            --locale={locale} """.format(**env))

        print green('Upgrade a versión ' + request_ver + ' exitoso.')

    else:
        print red("""
                  La version de wordpress en settings {0}
                  debe ser mayor que la versión actual {1}
                  """.format(request_ver, current_ver))


@task
def wordpress_downgrade():
    """
    Descarga la nueva version de wordpress escrita en settings y
    hace el downgrade
    """
    require('version', 'public_dir', 'locale')

    with cd(env.public_dir):
        current_ver = run(""" wp core version""")
        request_ver = env.version

    if request_ver < current_ver:
        run("""
            wp core update --version={version} --path={public_dir}
            --locale={locale} --force """.format(**env))

        print green('Downgrade a versión ' + request_ver + ' exitoso.')
    else:
        print red("""
                  La version de wordpress en settings.py {0}
                  debe ser inferior a la versión actual {1}
                  """.format(request_ver, current_ver))


@task
def set_webserver(webserver="nginx"):
    """
    Cambia el servidor web del proyecto, opciones nginx o apache2
    """
    if webserver == "apache2":
        run("sudo service php5-fpm stop")
        run("sudo service nginx stop")
        run("sudo service apache2 start")
    else:
        run("sudo service apache2 stop")
        run("sudo service php5-fpm start")
        run("sudo service nginx start")


@task
def clean_plugins():
    """
    Verifica si hay plugins instalados no usados y los elimina
    """
    require('public_dir')
    installed_plugins = json.loads(
        run('wp plugin list --format=json --path={0}'.  format(env.public_dir))
    )
    plugins_to_delete = []
    for installed_plugin in installed_plugins:
        if not search_plugin(installed_plugin['name']):
            plugins_to_delete.append(installed_plugin['name'])
    if plugins_to_delete:
        print yellow(
            u'Se encontraron plugins no especificados en settings.json, '
            u'que sin embargo están instalados en wordpress. '
            u'Estos plugins deberán ser desinstalados antes de poder '
            u'instalar, actualizar o sincronizar nuevos plugins\n'
            u'Lista de plugins que no están presentes en settings.json'
        )
        count = 1
        for plugin in plugins_to_delete:
            print yellow(str(count) + ".- " + plugin)
            count = count + 1
        if confirm(yellow('Desea borrar estos plugins?')):
            for plugin in plugins_to_delete:
                run('wp plugin deactivate {0} --path={1}'.
                    format(plugin, env.public_dir))
                run('wp plugin uninstall {0} --path={1}'.
                    format(plugin, env.public_dir))
        else:
            sys.exit(0)


@task
def search_plugin(plugin_searched):
    """
    Busca un plugin en settings.json
    """
    for plugin in env.get("plugins", []):
        if plugin['name'] == plugin_searched:
            return True

    for plugin in env.get("custom_plugins", []):
        if plugin['name'] == plugin_searched:
            return True

    return False
