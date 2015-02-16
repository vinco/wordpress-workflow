# encoding: utf-8
import re, json
from fabric.api import cd, env, local, run, task, require
from fabric.contrib.project import rsync_project
from fabric.colors import green, red
with open('settings.json') as json_data:
    config = json.load(json_data)
    json_data.close()

@task
def enviro(ambiente):
    '''
    Carga los datos del ambiente definido en settings.json (local,staging o production).
    '''
    # validate ambiente variable
    if ambiente in ['local','staging','production']:
        print 'Cargando configuración de ambiente: '+ambiente
        try:
            env.user = config['SITE_CONFIG']['environments'][ambiente]['ssh_user']
            env.hosts = config['SITE_CONFIG']['environments'][ambiente]['ssh_hosts']
            print green('Credenciales de SSH '+ambiente+' configurados user : '+env.user+' host: '+env.hosts[0])
        except:# si no hay un usuario ssh definido, es local y se usa la llave creada por vagrant
            # Usuario
            env.user = 'vagrant'
            # Se conecta al ssh local
            env.hosts = ['127.0.0.1:2222']
            # Llave ssh creada por Vagrant
            result = local('vagrant ssh-config | grep IdentityFile', capture=True)
            env.key_filename = result.split()[1].replace('"', '')
            print green('Llave SSH Local configurada')

        # Directorio del sitio wordpress
        env.site_dir = config['SITE_CONFIG']['environments'][ambiente]['site_dir']
        print green('Directorio del sitio configurado: '+env.site_dir)
        # Directorio del proyecto (themes,plugins,etc.) 
        env.wordpress_dir = config['SITE_CONFIG']['environments'][ambiente]['wordpress_dir']
        print green('Directorio del proyecto configurado: '+env.wordpress_dir)
        env.env = ambiente
        

        env.title = config['SITE_CONFIG']['environments'][ambiente]['title'],



        # verificar las carpetas del ambiente 
        envverify()
        # definir los variables de WP-Admin
        env.admin_user = config['SITE_CONFIG']['environments'][ambiente]['admin_user']
        env.admin_password = config['SITE_CONFIG']['environments'][ambiente]['admin_password']
        env.admin_email = config['SITE_CONFIG']['environments'][ambiente]['admin_email']
        print green('Usuario de WP-Admin configurado')

        # definir los variables de MySql
        env.dbname = config['SITE_CONFIG']['environments'][ambiente]['dbname']
        env.dbuser = config['SITE_CONFIG']['environments'][ambiente]['dbuser']
        env.dbpassword = config['SITE_CONFIG']['environments'][ambiente]['dbpassword']
        env.dbhost = config['SITE_CONFIG']['environments'][ambiente]['dbhost']
        print green('Variables de MySql configurados')

    else:# El ambiente no existe
        print red('El ambiente '+ambiente+' no existe.')


@task
def envverify():
    '''
    Verifica que las carpetas dadas de alta en el ambiente esten bien formadas
    '''
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
    '''
    Crea la base de datos, información de prueba y activa rewrite
    '''
    require('env')
    # Crea la base de datos
    run('''
        echo "DROP DATABASE IF EXISTS {0}; CREATE DATABASE {0};
        "|mysql --batch --user={1} --password={2} --host=localhost
        '''.
        format(
           env.dbname,
           env.dbuser,
           env.dbpassword,
           env.dbhost
        ))
    #Activa modulo de apache
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
        config['SITE_CONFIG']['version'],
        env.wordpress_dir,
        config['SITE_CONFIG']['locale'],
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
        config['SITE_CONFIG']['environments'][env.env]['url'],
        config['SITE_CONFIG']['environments'][env.env]['title'],
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
    Activa el tema seleccionado en la instalacion de wordpress
    '''
    require("wordpress_dir")

    with cd(env.wordpress_dir):
        run('''
            wp theme activate {0}
            '''.format(
            config['SITE_CONFIG']['theme']
            ))


@task
def install_plugins():
    '''
    Instala plugins e inicializa segun el archivo settings
    '''
    require("wordpress_dir")
    require("site_dir")

    for custom_plugin in config['CUSTOM_PLUGINS_CONFIG']:
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
        for plugin in config['PLUGINS_CONFIG']:
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
def export_data():
    require("site_dir")
    require("wordpress_dir")
    require("env")
    run('''
       mysqldump -u {dbuser} -p{dbpassword} {dbname} --host={dbhost} --no-create-info  > {sitedir}database/data.sql
       '''.format(
       sitedir=env.site_dir, **SITE_CONFIG[env.env]
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
        env.dbname,
        env.dbuser,
        env.dbpassword,
        env.dbhost,
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

@task
def wordpress_upgrade():
    '''
    Descarga la nueva version de wordpress escrita en settings y hace el upgrade
    '''
    require("wordpress_dir")
    require("site_dir")
    require('env')
    with cd(env.wordpress_dir):
        current_ver = run(''' wp core version''')
        request_ver = SITE_CONFIG['version']
    if request_ver > current_ver:
        #Upgrades wordpress based on settings.py options
        run('''
            wp core update --version={0} --path={1} --locale={2} 
            '''.format(
            SITE_CONFIG['version'],
            env.wordpress_dir,
            SITE_CONFIG['locale']
            ))
        print green('Upgrade a versión '+ request_ver + ' exitoso.')
    else:
        print red("La version de wordpress en settings.py ("+ request_ver + ") debe ser mayor que la versión actual (" + current_ver + ")")

@task
def wordpress_downgrade():
    '''
    Descarga la nueva version de wordpress escrita en settings y hace el downgrade
    '''
    require("wordpress_dir")
    require("site_dir")
    require('env')
    with cd(env.wordpress_dir):
        current_ver = run(''' wp core version''')
        request_ver = SITE_CONFIG['version']
    if request_ver < current_ver:
        #Upgrades wordpress based on settings.py options
        run('''
            wp core update --version={0} --path={1} --locale={2} --force
            '''.format(
            SITE_CONFIG['version'],
            env.wordpress_dir,
            SITE_CONFIG['locale']
            ))
        print green('Downgrade a versión '+ request_ver + ' exitoso.')
    else:
        print red("La version de wordpress en settings.py ("+ request_ver + ") debe ser inferior a la versión actual (" + current_ver + ")")

    

    




















