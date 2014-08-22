# encoding: utf-8
from fabric.api import cd, env, local, run, task, require
from fabric.contrib.project import rsync_project
from fabric.colors import green
from settings import SITE_CONFIG, PLUGINS_CONFIG, CUSTOM_PLUGINS_CONFIG


@task
def vagrant():
    '''
    Ambiente local de desarrollo (máquina virtual Vagrant).
    '''
    # Usuario
    env.user = 'vagrant'
    # Se conecta al ssh local
    env.hosts = ['127.0.0.1:2222']

    # Llave ssh creada por Vagrant
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1].replace('"', '')

    # Directorio del sitio wordpress
    env.site_dir = '/home/vagrant/wordpress-workflow/'
    env.wordpress_dir = '/home/vagrant/www/'
    env.env = 'dev'


@task
def bootstrap():
    '''
    Crea la base de datos, información de prueba y activa rewrite
    '''
    require('env')
    # Crea la base de datos
    run('''
        echo "DROP DATABASE IF EXISTS {0}; CREATE DATABASE {0};
        "|mysql --batch --user={1} --password={2} --host={3}
        '''.
        format(
            SITE_CONFIG[env.env]['dbname'],
            SITE_CONFIG[env.env]['dbuser'],
            SITE_CONFIG[env.env]['dbpassword'],
            SITE_CONFIG[env.env]['dbhost']
        ))
    # Activa modulo de apache
    run('a2enmod rewrite')
    wordpress_install()


@task
def wordpress_install():
    '''
    Descarga la version de wordpress escrita en settings en instala la base de datos
    '''
    require("wordpress_dir")
    require("site_dir")
    require('env')
    #Downloads wordpress
    run('''
        wp core download --version={0} --path={1} --locale={2} --force
        '''.format(
        SITE_CONFIG['version'],
        env.wordpress_dir,
        SITE_CONFIG['locale']
        ))
    #creates config
    run('''
        wp core config --dbname={0} --dbuser={1} \
            --dbpass={2} --path={3}
        '''.format(
        SITE_CONFIG[env.env]['dbname'],
        SITE_CONFIG[env.env]['dbuser'],
        SITE_CONFIG[env.env]['dbpassword'],
        env.wordpress_dir
        ))
    #Installs into db
    run('''
        wp core install --url="{0}" --title="{1}" \
        --admin_user="{2}" --admin_password="{3}" \
        --admin_email="{4}" --path={5}
        '''.format(
        SITE_CONFIG[env.env]['url'],
        SITE_CONFIG[env.env]['title'],
        SITE_CONFIG[env.env]['admin_user'],
        SITE_CONFIG[env.env]['admin_password'],
        SITE_CONFIG[env.env]['admin_email'],
        env.wordpress_dir
        ))
    #Creates simbolic link to themes
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
    Activa el tema seleccionado en la instalacion de wordpress
    '''
    require("wordpress_dir")

    with cd(env.wordpress_dir):
        run('''
            wp theme activate {0}
            '''.format(
            SITE_CONFIG['theme']
            ))


@task
def install_plugins():
    '''
    Instala plugins e inicializa segun el archivo settings
    '''
    require("wordpress_dir")
    require("site_dir")

    for custom_plugin in CUSTOM_PLUGINS_CONFIG:
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
        for plugin in PLUGINS_CONFIG:
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
    Importa la informacion de database/data.sql
    '''
    require("site_dir")
    require("wordpress_dir")
    require("env")
    run('''
        mysql -u {0} -p{1} {2} --host={3} < {4}database/data.sql
        '''.format(
        SITE_CONFIG[env.env]['dbuser'],
        SITE_CONFIG[env.env]['dbpassword'],
        SITE_CONFIG[env.env]['dbname'],
        SITE_CONFIG[env.env]['dbhost'],
        env.site_dir
        ))
    with cd(env.wordpress_dir):  # Changes the domain
        run('''
            wp option update home http://{0} &&
            wp option update siteurl http://{0}
            '''.format(
            SITE_CONFIG[env.env]['url']
            ))
        #changes the user
        run('''
            wp user update {0} --user_pass={1} --user_email={2}
            '''.format(
            SITE_CONFIG[env.env]['admin_user'],
            SITE_CONFIG[env.env]['admin_password'],
            SITE_CONFIG[env.env]['admin_email']
            ))


@task
def resetdb():
    '''
    Elimina la base de datos y la vuelve a crear
    '''
    require('site_dir')
    require('env')
    run('''
        echo "DROP DATABASE IF EXISTS {0};
        CREATE DATABASE {0};
        "|mysql --batch --user={1} --password={2} --host={3}
        '''.format(
        SITE_CONFIG[env.env]['dbname'],
        SITE_CONFIG[env.env]['dbuser'],
        SITE_CONFIG[env.env]['dbpassword'],
        SITE_CONFIG[env.env]['dbhost']
        )
        )


@task
def reset_all():
    '''
    Borra toda la instación de wordpress e inicia de cero
    '''
    require('wordpress_dir')
    run('''rm -rf {0}*'''.format(env.wordpress_dir))
    resetdb()
    bootstrap()


@task
def deploy():
    '''
    Sincroniza los archivos modificados y activa los plugins al entorno señalado
    '''
    require("wordpress_dir")
    require("site_dir")
    rsync_project(
        remote_dir=env.site_dir,
        local_dir='src/',
        delete=False
    )
    print green('Deploy exitoso.')
