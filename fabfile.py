# -*- coding: utf-8 -*-
import sys
import json
import os
from fabric.api import cd, env, run, task, require
from fabric.colors import green, red, white, yellow, blue
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric import state

from fabutils.env import set_env_from_json_file
from fabutils.tasks import ursync_project, ulocal, urun


@task
def environment(env_name):
    """
    Crea la configuración para el entorno en el que correrán las tareas.
    """
    schemas_dir = "wordpress-workflow/json_schemas/"
    state.output['running'] = False
    state.output['stdout'] = False
    print "Estableciendo ambiente " + blue(env_name, bold=True)
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
    print "Creando entorno local"
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

    print "Descargando wordpress"
    #Downloads wordpress
    run('wp core download --version={version} --path={public_dir} '
        '--locale={locale} --force'.format(**env))

    print "Creando configuraciones de wordpress"
    #creates config
    run('wp core config --dbname={dbname} --dbuser={dbuser} '
        '--dbpass={dbpassword} --path={public_dir}'.format(**env))

    print "Instalando wordpress"
    #Installs into db
    run('wp core install --url="{url}" --title="{title}" '
        '--admin_user="{admin_user}" --admin_password="{admin_password}" '
        ' --admin_email="{admin_email}" --path={public_dir}'.format(**env))

    print "Instalando wordpress-workflow"
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

    print "Activando tema " + blue(env.theme, bold=True)
    with cd(env.public_dir):
        run('wp theme activate {0}'.format(env.theme))


@task
def install_plugins():
    """
    Instala plugins e inicializa segun el archivo settings
    """
    require('public_dir', 'wpworkflow_dir')

    check_plugins()
    print "Instalando plugins"
    for custom_plugin in env.get("custom_plugins", []):
        print "Procesando: " + blue(custom_plugin['name'], bold=True)
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
            print "Procesando: " + blue(plugin['name'], bold=True)
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
def import_data(file_name="data.sql"):
    """
    Importa la informacion de database/data.sql
    """
    require('wpworkflow_dir', 'dbuser', 'dbpassword', 'dbhost')
    require('admin_user', 'admin_password', 'admin_email', 'url')

    env.file_name = file_name

    print "Importando datos del archivo: " + blue(file_name, bold=True)
    run("""
        mysql -u {dbuser} -p{dbpassword} {dbname} --host={dbhost} <\
        {wpworkflow_dir}database/{file_name} """.format(**env))

    with cd(env.public_dir):  # Changes the domain
        run("""
            wp option update home http://{url} &&\
            wp option update siteurl http://{url}
            """.format(**env))
        #changes the user
        run("""
            wp user update {admin_user} --user_pass={admin_password}\
            --user_email={admin_email}
            """.format(**env))


@task
def export_data(file_name="data.sql", just_data=False):
    """
    Exporta la base de datos a database/data.sql
    """
    require('wpworkflow_dir', 'dbuser', 'dbpassword', 'dbname', 'dbhost')

    env.file_name = file_name
    if just_data:
        env.just_data = "--no-create-info"
    else:
        env.just_data = " "

    print "Exportando datos al archivo: " + blue(file_name, bold=True)
    run("""
       mysqldump -u {dbuser} -p{dbpassword} {dbname} --host={dbhost}\
       {just_data} > {wpworkflow_dir}database/{file_name} """.format(**env))


@task
def resetdb():
    """
    Elimina la base de datos y la vuelve a crear
    """
    require('dbname', 'dbuser', 'dbpassword', 'dbhost')
    print "Eliminando base de datos"
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
    print "Elmininando contenido de la carpeta: " + blue(env.public_dir, bold=True)
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

    print "Servidor de desarrollo puesto en " + blue(webserver, bold=True)


@task
def upgrade_plugin(plugin_name=None):
    """
    Actualiza un plugin hasta la versión especificada en settings.json
    """
    require('public_dir')
    if not plugin_name:
        print red("Se requiere del nombre del plugin a actualizar")
        sys.exit(0)

    installed_plugins = json.loads(
        run('wp plugin list --format=json --path={0}'.  format(env.public_dir))
    )
    installed_plugin = search_plugin(plugin_name, installed_plugins)
    plugin = search_plugin(plugin_name)
    if plugin:
        print (
            u'Actualizando plugin ' + plugin_name + u' de versión ' +
            installed_plugin['version'] + u' a versión ' + plugin['version']
        )
        run('wp plugin update {0} --version={1} --path={2}'.
            format(plugin_name, plugin['version'], env.public_dir))
        print green("Plugin " + plugin_name + " actualizado")


@task
def check_plugins():
    """
    Verifica las versiones instaladas de los plugins
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
            u'Se han encontrado plugins en `settings.json` que no tienen'
            u' versión especificada. Esto no es un error pero puede atraer'
            u' problemas. Se recomienda especificar la versión en el archivo\n'
        )
        for plugin in stable_plugins:
            installed_plugin = search_plugin(plugin['name'], installed_plugins)
            if(installed_plugin):
                version = installed_plugin['version']
            else:
                version = 'No instalado'
            print yellow(
                'Plugin: ' + plugin['name'] + u', Versión '
                u'instalada: ' + version
            )
    # Verifies upgrade-able
    upgrade = run('wp plugin update --dry-run --all --path={0}'.
                  format(env.public_dir))
    if upgrade != "No plugin updates available.":
        print yellow(
            u'Se han encontrado plugins que pueden ser actualizados'
            u' esto se puede hacer cambiando la versión en settings.json'
            u' y ejecutando el comando'
            u'  `fab environment:ambiente upgrade_plugin:plugin_name`'
        )
        print yellow(upgrade)


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
    print "Verificando plugins instalados"
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
def search_plugin(plugin_searched, search_list=None):
    """
    Busca un plugin en settings.json
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
def make_tarball(target_environment="test", tar_name="wordpress-dist"):
    """
    Genera un tarball para subir a servidores sin ssh
    """
    environment('vagrant')
    env.tmp_dir = "/home/vagrant/wordpress-dist/"
    env.tmp_dir_name = "wordpress-dist"
    env.host_string = env.hosts[0]

    check_plugins()

    if not os.path.exists('./dist/'):
        print "Creando carpeta dist"
        os.makedirs('./dist/')

    # Creates necesary dirs
    print "Creando estructura de directorios "
    if exists(env.tmp_dir):
        urun('rm -rf {tmp_dir}'.format(**env))

    urun('mkdir {tmp_dir}'.format(**env))

    # Downloads
    print "Descargando y generando configuracion wordpress"
    #Downloads wordpress
    urun('wp core download --version={version} --path={tmp_dir} '
         '--locale={locale} --force'.format(**env))
    #creates config
    with open('environments.json', 'r') as json_file:
        db_config = json.load(json_file)[target_environment]
        db_config['tmp_dir'] = env.tmp_dir
        urun('wp core config --dbname={dbname} --dbuser={dbuser} '
             '--dbpass={dbpassword} --skip-check --path={tmp_dir}'.format(**db_config))

    # Configure temp database
    create_database_command = '''
         echo "
             CREATE DATABASE {dbname};
             CREATE USER '{dbuser}'@'localhost' IDENTIFIED BY '{dbpassword}';
             GRANT ALL PRIVILEGES ON *.* TO '{dbuser}'@'localhost';
             FLUSH PRIVILEGES;
         "'''.format(**db_config)
    print "Configurando base de datos temporal"
    urun(
        create_database_command +
        '|mysql --batch --user={dbuser} --password={dbpassword}'.format(**env)
    )
    # Install wodpress
    print "Instalando wordpress temporal"
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
            print "Descargando plugin: " + blue(plugin['name'], bold=True)
            urun(""" wp plugin install {0} """.format(plugin['name']))
    # Copy custom plugins
    for plugin in env.get("custom_plugins", []):
        env.plugin = plugin['name']
        print "Copiando plugin: " + blue(plugin['name'], bold=True)
        urun(
            """
            cp -rf {wpworkflow_dir}plugins/{plugin} \
            {tmp_dir}wp-content/plugins
            """.format(**env)
        )
    # Download all require plugins
    print "Generando empaquetado"
    env.tar_name = tar_name
    with cd(env.tmp_dir + ".."):
        urun('tar -czf {wpworkflow_dir}{tar_name}.tar.gz {tmp_dir_name}/*'
             .format(**env))
        os.rename(
            './src/{tar_name}.tar.gz'.format(**env),
            './dist/{tar_name}.tar.gz'.format(**env)
        )
    # Delete temp database
    print "Limpiando datos temporales"
    clean_database_command = '''
        echo "
            DROP USER '{dbuser}'@'localhost';
            DROP DATABASE {dbname};
        "'''.format(**db_config)
    urun(
        clean_database_command +
        '|mysql --batch --user={dbuser} --password={dbpassword}'.format(**env)
    )
    urun('rm -rf {tmp_dir}'.format(**env))
    print green("Empequetado generado en dist/{tar_name}.tar.gz".format(**env))
