# encoding: utf-8
from fabric.api import cd, env, local, run, task, require
from settings import SITE_CONFIG

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

    # Directorio del sitio tuguia
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
        )
    )
    # Activa modulo de apache
    run('a2enmod rewrite')
    wordpress_install()


@task
def wordpress_install():
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
        )
    )
    #creates config
    run('''
        wp core config --dbname={0} --dbuser={1} \
            --dbpass={2} --path={3}
        '''.format(
        SITE_CONFIG[env.env]['dbname'],
        SITE_CONFIG[env.env]['dbuser'],
        SITE_CONFIG[env.env]['dbpassword'],
        env.wordpress_dir
        )
    )
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
        )
    )
    #Creates simbolic link to themes
    run('''
       rm -rf {1}wp-content/themes &&
       ln -s {0}themes {1}wp-content
       '''.format(
        env.site_dir,
        env.wordpress_dir
        )
    )
    activate_theme()

@task
def activate_theme():
    require("wordpress_dir")

    with cd(env.wordpress_dir):
        run('''
            wp theme activate {0}
            '''.format(
            SITE_CONFIG['theme']
            )
            )


@task
def resetdb():
    '''Elimina la base de datos y la vuelve a crear'''
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
