# encoding: utf-8
from fabric.api import cd, env, local, run, task, require
from settings import SITE_CONFIG

USER = 'root'
PASSWORD = 'password'
HOST = 'localhost'
DATABASE = 'wordpress_workflow'


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
    env.wp = '/home/vagrant/.wp-cli/bin/wp'


@task
def bootstrap():
    '''
    Crea la base de datos, información de prueba y activa rewrite
    '''
    require('site_dir')
    # Crea la base de datos
    run('''
        echo "CREATE DATABASE {0}; 
        "|mysql --batch --user={1} --password={2} --host={3}
        '''.format(DATABASE, USER, PASSWORD, HOST)
    )
    # Activa modulo de apache
    run('a2enmod rewrite')
    wordpress_install()


@task
def wordpress_install():
    require("wordpress_dir")
    require("wp")
    #Downloads wordpress
    run('''
        {0} core download --version={1} --path={2} --locale={3} --force
        '''.format(
        env.wp,
        SITE_CONFIG['version'],
        env.wordpress_dir,
        SITE_CONFIG['locale']
        )
    )
    #creates config
    run('''
        {0} core config --dbname={1} --dbuser={2} \
            --dbpass={3} --path={4}
        '''.format(
        env.wp,
        SITE_CONFIG['dev']['dbname'],
        SITE_CONFIG['dev']['dbuser'],
        SITE_CONFIG['dev']['dbpass'],
        env.wordpress_dir
        )
    )
    #Installs into db
    run('''
        {0} core install --url="{1}" --title="{2}" \
        --admin_user="{3}" --admin_password="{4}" \
        --admin_email="{5}" --path={6}
        '''.format(
        env.wp,
        SITE_CONFIG['dev']['url'],
        SITE_CONFIG['dev']['title'],
        SITE_CONFIG['dev']['admin_user'],
        SITE_CONFIG['dev']['admin_password'],
        SITE_CONFIG['dev']['admin_email'],
        env.wordpress_dir
        )
    )


@task
def resetdb():
    '''Elimina la base de datos y la vuelve a crear'''
    require('site_dir')
    run('''
        echo "DROP DATABASE IF EXISTS {0};
        CREATE DATABASE {0};
        "|mysql --batch --user={1} --password={2} --host={3}
        '''.format(DATABASE, USER, PASSWORD, HOST)
    )
