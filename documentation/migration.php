<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Wordpress-workflow Documentation</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="css/simple-sidebar.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <div id="wrapper">

        <!-- Sidebar -->
        <div id="sidebar-wrapper">
        <?php echo file_get_contents("menu.html") ?>
        </div>
        <!-- /#sidebar-wrapper -->

        <!-- Page Content -->
        <div id="page-content-wrapper">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
                        <h1>Migración de versión anterior </h1>
                        <p>
                            Si se estaba usando la versión de wordpress-workflow
                            que usaba <code> settings.py </code> se tienen que realizar 
                            algunos cambios para poder usar la nueva versión
                        </p>
                        <p>
                            Esta entrada supone que ya se tiene la estructura de carpetas
                            de wordpress-workflow, si no es el caso es mejor leer la documentación de
                            <a href="install.php">instalación</a>
                        </p>
                        <h2> Respaldar </h2>
                        <p>
                            Lo primero que tenemos que es respaldar el proyecto, así que cualquier cambio de código
                            deberá tener un commit y puesto en su repositorio. También se debe de respaldar la información
                            de base de datos si es que se tienen páginas o desarrollo no de código en el proyecto, esto lo
                            podemos hacer con el siguiente comando:
                        </p>
<pre>
$ fab vagrant export_data
</pre>
                        <p>
                            Lo que generará el archivo <code>src/database/data.sql</code> que usaremos
                            para regenerar la base de datos.
                        </p>
                        <p>
                            Debemos también guardar en un lugar seguro fuera del proyecto el archivo
                            <code>settings.py</code>
                        </p>
                        <h2> Actualización </h2>
                        <p>
                            Una vez seguros de que hemos respaldado la información necesaria vamos a
                            <strong> Borrar</strong> el antiguo entorno e instalar el nuevo de la siguiente manera:
                        </p>
                        <pre>
$ vagrant halt
$ vagrant destroy
$ rm -rf vagrant
$ git submodule add git@github.com:vinco/wordpress-workflow.git
$ cp wordpress-workflow/defaults/environments.json ./
$ cp wordpress-workflow/defaults/settings.json ./
$ rm Vagrantfile
$ rm fabfile.py
$ wordpress-workflow/startProject.sh
$ vagrant up
                        </pre>
                        <p>
                            Ahora copiaremos nuestro <code>settings.py</code> en los nuevos archivos
                            <code> settings.json environments.json</code>
                        </p>
                        <p>
                            Toda la información que iba en el <code>settings.py</code> en la variable 
                            <code>SITE_CONFIG</code> acerca de entornos deberá sera copiada al nuevo archivo
                            por ejemplo:
                        </p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-5">
                        <h3>settings.py</h3>
                        <pre>
# General configurations for wordpress-workflow
SITE_CONFIG = {
    'version': '3.9.1',
    'locale': 'es_ES',
    'theme': 'yourtheme',

    'dev': {
        'url': 'wordpress-workflow.local',
        'title': 'New Project',
        #Admin config
        'admin_user': 'admin',
        'admin_password': 'password',
        'admin_email': 'admin@email.com',
        #database config 
        'dbname': 'wordpress_workflow',
        'dbuser': 'root',
        'dbpassword': 'password',
        'dbhost': 'localhost'
    }

    'staging': {
        'url': 'staging.development.com',
        'title': 'New Project',
        #Admin config
        'admin_user': 'admin',
        'admin_password': 'password',
        'admin_email': 'admin@email.com',
        #database config 
        'dbname': 'wordpress_workflow',
        'dbuser': 'root',
        'dbpassword': 'password',
        'dbhost': 'localhost'
    }
}



                        </pre>
                    </div>
                    <div class="col-lg-7">
                        <h3>environments.json</h3>
                        <pre>
{
    "vagrant": {
        "url": "wordpress.local",
        <strong>"user": "vagrant",
        "group": "vagrant",
        "hosts": ["127.0.0.1:2222"],
        "public_dir": "/home/vagrant/public_www/",
        "wpworkflow_dir": "/home/vagrant/wordpress-workflow/",
        "command_prefixes": [],</strong>
        "title": "New Project",
        "admin_user": "admin",
        "admin_password": "password",
        "admin_email": "admin@email.com",
        "dbname": "wordpress_workflow",
        "dbuser": "root",
        "dbpassword": "password",
        "dbhost": "localhost"
    },
    "staging": {
        "url": "staging.development.com",
        <strong>"user": "staging-user",
        "group": "staging-group",
        "hosts": ["staging.development.com"],
        "public_dir": "/staging.development.com/public/",
        "wpworkflow_dir":"/staging.development.com/wpworkflow/",
        "command_prefixes": [
            "/staging.development.com/env/wp-cli/bin/activate"
        ],</strong>
        "title": "New Project",
        "admin_user": "admin",
        "admin_password": "password",
        "admin_email": "admin@email.com",
        "dbname": "wordpress_workflow",
        "dbuser": "root",
        "dbpassword": "password",
        "dbhost": "localhost"
    }
}
</pre>
        
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12">
                        <p>
                            Nótese que no mucho ha cambiado, sólo se ha organizado
                            un poco mejor. La mayoría de los datos ya los teníamos
                            en la versión anterior, sólo se han cambiado algunos nombres
                            para hacerlos más descriptivos.<br/>
                            Por ejemplo <code>site_dir</code> se convierte en <code>wpworkflow_dir</code>
                            así como <code>wordpress_dir</code> se convierte en <code> public_dir</code>
                        <p>
                        <p>
                            Algunos puntos a tomar en cuenta es que se está usando un validador JSON
                            por lo que debe de tomar en cuenta el estándar:
                        </p>
                        <ul>
                            <li>Usar sólo doble comilla</li>
                            <li>Los datos números y booleanos van sin comillas</li>
                            <li>No puede existir comas "sobrantes"</li>
                        </ul>
                        <p>
                            Se recomienda el uso de un validador JSON como puede ser 
                            <a href="http://jsonlint.com/">JSONLint</a>
                        </p>
                        <h3> Settings.json </h3>
                        <p>
                            Ahora copiaremos los datos de configuración restantes
                            de settings.py a settings.json. Quedaría de la siguiente manera
                        </p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-5">
                        <h3>settings.py</h3>
                        <pre>
# General configurations for wordpress-workflow
SITE_CONFIG = {
    'version': '3.9.1',
    'locale': 'es_ES',
    'theme': 'yourtheme',
}
# 3rd party plugins

PLUGINS_CONFIG = (
    {
        'name': 'wordpress-seo',
        'active': True,
        'version': 'stable'
    },
    {
        'name': 'contact-form-7',
        'active': True,
        'version': 'stable'
    },
    {
        'name': 'wp-super-cache',
        'active': True,
        'version': 'stable'
    },
)

# Own plugins
CUSTOM_PLUGINS_CONFIG = (
    {
        'name': 'jetpack',
        'active': True
    },
)
                        </pre>
                    </div>
                    <div class="col-lg-5">
                        <h3>settings.json</h3>
                        <pre>

{
    "version": "3.9.1",
    "locale": "es_ES",
    "theme": "yourtheme",
    "plugins":[
        {
            "name": "wordpress-seo",
            "active": true,
            "version": "stable"
        },
        {
            "name": "contact-form-7",
            "active": true,
            "version": "stable"
        },
        {
            "name": "wp-super-cache",
            "active": true,
            "version": "stable"
        },
    ],
    "custom_plugins" :[
        {
            "name": "jetpack",
            "active": true
        }
    ]
}




                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12">
                        <h2> Terminando </h2>
                        <p> 
                            Por último debemos generar nuestro nuevo
                            sitio, limpiar archivos no necesarios e importar la
                            información que habíamos reparado.
                            Todo esto se puede hacer de la siguiente manera
                        </p>
                        <pre>
$ rm settings.py
$ fab environment:vagrant bootstrap resetdb import_data
                        </pre>
                        <p>
                            Y eso es todo
                        </p>
                    </div>
                </div>

            </div>
        </div>
        <!-- /#page-content-wrapper -->

    </div>
    <!-- /#wrapper -->

    <!-- jQuery -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>


</body>

</html>
