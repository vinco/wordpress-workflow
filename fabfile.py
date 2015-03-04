# -*- coding: utf-8 -*-
import os
import re

from fabric.api import cd, env, run, task, require
from fabric.colors import green, red, white

from fabutils.env import set_env
from fabutils.tasks import ursync_project

from settings import SITE_CONFIG, PLUGINS_CONFIG, CUSTOM_PLUGINS_CONFIG


@task
def environment(env_name):
    """
    Crea la configuración para el entorno en el que correrán las tareas.
    """
    set_env(env_name, os.path.realpath(os.path.join(
        os.path.dirname(__file__), 'environments.json'
    )))


@task
def envverify():
    """
    Verifica que las carpetas dadas de alta en el ambiente esten bien formadas
    """
    require('site_dir')
    require('wordpress_dir')
    ok = True

    if not re.search('/$', env.site_dir):
        print red('La variable de entorno env.site_dir debe ser un folder (Terminar en / )')
        ok = False

    if not re.search('/$', env.wordpress_dir):
        ok = False
        print red('La variable de entorno env.wordpress_dir debe ser un folder (Terminar en / )')

    if env.wordpress_dir == env.site_dir:
        ok = False
        print red('Los directorios site_dir y wordpress_dir no pueden ser el mismo')

    if ok:
        print green('El entorno tiene bien configurados los directorios')


@task
def bootstrap():
    """
    Crea la base de datos, información de prueba y activa rewrite
    """
    require('env')
    # Crea la base de datos
    run("""
        echo "DROP DATABASE IF EXISTS {0}; CREATE DATABASE {0};
        "|mysql --batch --user={1} --password={2} --host={3}
        """.
        format(
            SITE_CONFIG[env.env]['dbname'],
            SITE_CONFIG[env.env]['dbuser'],
            SITE_CONFIG[env.env]['dbpassword'],
            SITE_CONFIG[env.env]['dbhost']
        ))
    # Activa modulo de apache
    run('sudo a2enmod rewrite')
    wordpress_install()


@task
def wordpress_install():
    """
    Descarga la version de wordpress escrita en settings en instala la base
    de datos.
    """
    require('env', 'site_dir', 'wordpress_dir')

    #Downloads wordpress
    run('wp core download --version={0} --path={1} --locale={2} '
        '--force'.format(
            SITE_CONFIG['version'],
            env.wordpress_dir,
            SITE_CONFIG['locale']
        ))
    #creates config
    run('wp core config --dbname={0} --dbuser={1} --dbpass={2} '
        '--path={3}'.format(
            SITE_CONFIG[env.env]['dbname'],
            SITE_CONFIG[env.env]['dbuser'],
            SITE_CONFIG[env.env]['dbpassword'],
            env.wordpress_dir
        ))
    #Installs into db
    run('wp core install --url="{0}" --title="{1}" --admin_user="{2}" '
        '--admin_password="{3}" --admin_email="{4}" --path={5}'.format(
            SITE_CONFIG[env.env]['url'],
            SITE_CONFIG[env.env]['title'],
            SITE_CONFIG[env.env]['admin_user'],
            SITE_CONFIG[env.env]['admin_password'],
            SITE_CONFIG[env.env]['admin_email'],
            env.wordpress_dir
        ))
    #Creates simbolic link to themes
    run('rm -rf {1}wp-content/themes && ln -s {0}themes {1}wp-content'.format(
        env.site_dir, env.wordpress_dir))

    activate_theme()
    install_plugins()


@task
def activate_theme():
    """
    Activa el tema seleccionado en la instalacion de wordpress
    """
    require("wordpress_dir")

    with cd(env.wordpress_dir):
        run('wp theme activate {0}'.format(
            SITE_CONFIG['theme']))


@task
def install_plugins():
    """
    Instala plugins e inicializa segun el archivo settings
    """
    require("wordpress_dir")
    require("site_dir")

    for custom_plugin in CUSTOM_PLUGINS_CONFIG:
        with cd(env.wordpress_dir):
            run("""
                if ! wp plugin is-installed {0};
                then
                    ln -s {1}plugins/{0} {2}wp-content/plugins/;
                fi
                """.format(
                custom_plugin['name'],
                env.site_dir,
                env.wordpress_dir
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
    with cd(env.wordpress_dir):
        for plugin in PLUGINS_CONFIG:
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
    require("site_dir")
    require("wordpress_dir")
    require("env")
    run("""
        mysql -u {0} -p{1} {2} --host={3} < {4}database/data.sql
        """.format(
        SITE_CONFIG[env.env]['dbuser'],
        SITE_CONFIG[env.env]['dbpassword'],
        SITE_CONFIG[env.env]['dbname'],
        SITE_CONFIG[env.env]['dbhost'],
        env.site_dir
        ))
    with cd(env.wordpress_dir):  # Changes the domain
        run("""
            wp option update home http://{0} &&
            wp option update siteurl http://{0}
            """.format(
            SITE_CONFIG[env.env]['url']
            ))
        #changes the user
        run("""
            wp user update {0} --user_pass={1} --user_email={2}
            """.format(
            SITE_CONFIG[env.env]['admin_user'],
            SITE_CONFIG[env.env]['admin_password'],
            SITE_CONFIG[env.env]['admin_email']
            ))


@task
def export_data():
    require("site_dir")
    require("wordpress_dir")
    require("env")
    run("""
       mysqldump -u {dbuser} -p{dbpassword} {dbname} --host={dbhost} --no-create-info  > {sitedir}database/data.sql
       """.format(
       sitedir=env.site_dir, **SITE_CONFIG[env.env]
       ))


@task
def resetdb():
    """
    Elimina la base de datos y la vuelve a crear
    """
    require('site_dir')
    require('env')
    run("""
        echo "DROP DATABASE IF EXISTS {0};
        CREATE DATABASE {0};
        "|mysql --batch --user={1} --password={2} --host={3}
        """.format(
        SITE_CONFIG[env.env]['dbname'],
        SITE_CONFIG[env.env]['dbuser'],
        SITE_CONFIG[env.env]['dbpassword'],
        SITE_CONFIG[env.env]['dbhost']
        )
        )


@task
def reset_all():
    """
    Borra toda la instación de wordpress e inicia de cero
    """
    require('wordpress_dir')
    run("""rm -rf {0}*""".format(env.wordpress_dir))
    resetdb()
    bootstrap()


@task
def deploy():
    """
    Sincroniza los archivos modificados y establece los permisos necesarios en
    el entorno señalado.
    """
    require('group', 'site_dir', 'wordpress_dir')

    print white("Subiendo código al servidor...", bold=True)
    ursync_project(
        local_dir='./src/',
        remote_dir=env.site_dir,
        delete=True,
        default_opts='-chrtvzP'
    )

    print white("Estableciendo permisos...", bold=True)
    run('chmod -R o-rwx {0}'.format(env.site_dir))
    run('chmod -R o-rwx {0}'.format(env.wordpress_dir))
    run('chgrp -R {0} {1}'.format(env.group, env.site_dir))
    run('chgrp -R {0} {1}'.format(env.group, env.wordpress_dir))

    print green('Deploy exitoso.')


@task
def wordpress_upgrade():
    """
    Descarga la nueva version de wordpress escrita en settings y hace el upgrade
    """
    require("wordpress_dir")
    require("site_dir")
    require('env')
    with cd(env.wordpress_dir):
        current_ver = run(""" wp core version""")
        request_ver = SITE_CONFIG['version']
    if request_ver > current_ver:
        #Upgrades wordpress based on settings.py options
        run("""
            wp core update --version={0} --path={1} --locale={2}
            """.format(
            SITE_CONFIG['version'],
            env.wordpress_dir,
            SITE_CONFIG['locale']
            ))
        print green('Upgrade a versión '+ request_ver + ' exitoso.')
    else:
        print red("La version de wordpress en settings.py ("+ request_ver + ") debe ser mayor que la versión actual (" + current_ver + ")")


@task
def wordpress_downgrade():
    """
    Descarga la nueva version de wordpress escrita en settings y hace el downgrade
    """
    require("wordpress_dir")
    require("site_dir")
    require('env')
    with cd(env.wordpress_dir):
        current_ver = run(""" wp core version""")
        request_ver = SITE_CONFIG['version']
    if request_ver < current_ver:
        #Upgrades wordpress based on settings.py options
        run("""
            wp core update --version={0} --path={1} --locale={2} --force
            """.format(
            SITE_CONFIG['version'],
            env.wordpress_dir,
            SITE_CONFIG['locale']
            ))
        print green('Downgrade a versión '+ request_ver + ' exitoso.')
    else:
        print red("La version de wordpress en settings.py ("+ request_ver + ") debe ser inferior a la versión actual (" + current_ver + ")")


