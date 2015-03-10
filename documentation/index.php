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
                        <h1 name="wordpress-workflow">Wordpress-workflow</h1>
                        <p>
                            Workpress-workflow es una herramienta que se ha diseñado para mantener separado la generación
                            de código propio de los proyectos de wordpress del core y archivos fuentes de plugins de
                            terceros.
                        </p>
                        <h1>Objetivo</h1>
                        <p>
                            Proporcionar las herramientas y procedimientos para poder llevar un correcto control de versiones
                            y cambios de proyectos hechos en wordpress.
                        </p>
                        <p>
                            El paquete está mantenido por Vinco Orbis y las sugerencias y reportes de errores deberán ser hechos a
                            <a href="https://github.com/vinco/wordpress-workflow">https://github.com/vinco/wordpress-workflow</a>
                            como un nuevo issue.
                        </p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12">
                        <h1> Estructura </h1>
                        <p>
                            Wordpress-workflow una vez instalado deberá tener la siguiente estructura:
                        </p>
                        <pre>
.
├── src
│   ├── database
│   ├── init
│   ├── plugins
│   └── themes
├── Vagrantfile
├── fabfile.py 
├── environments.json
├── settings.json
└── wordpress-workflow
                        </pre>
                        <p> 
                            Todo el código que se genere para el proyecto deberá ir en la carpeta src, esta carpeta
                            es la que se sincroniza con los servidores por lo que es muy importante mencionar que
                            <strong> Cualquier código en otra sección no será sincronizado con los servidores </strong>
                        </p>
                        <p>
                          Sólo se deberá escribir el código de los plugins que escribamos, si es un plugin que se usa
                          pero se encuentra listado como plugin de wordpress no deberemos agregar el código a la carpeta
                        </p>   
                        <h1> Ambientes y configuraciones </h1>
                        <p>
                            Los ambientes son los servidores en donde se mostrará la información, cada uno deberá tener un nombre asignado
                            en el archivo <code>environments.json</code> que tienen la siguiente estructura:
                        </p>
                        <pre>
{
    "vagrant": {
        "url": "wordpress.local",

        "user": "vagrant",
        "group": "vagrant",
        "hosts": ["127.0.0.1:2222"],
        "public_dir": "/home/vagrant/public_www/",
        "wpworkflow_dir": "/home/vagrant/wordpress-workflow/",
        "command_prefixes": [],

        "title": "wordpress workflow",
        "admin_user": "admin",
        "admin_password": "password",
        "admin_email": "changeme@changeme.com",
        "dbname": "wordpress_workflow",
        "dbuser": "root",
        "dbpassword": "password",
        "dbhost": "localhost"
    },
    "staging": {
        ...
    },
    ...
}
                        </pre>
                        <p> 
                            Las configuraciones generales de wordpress están en <code> settings.json </code>
                            y son las siguientes:
                        </p>
                        <pre>
{
    "version": "4.1.1",
    "locale": "es_ES",
    "theme": "twentyfourteen",
    "plugins": [
        {
            "name": "wordpress-seo",
            "active": true,
            "version": "stable"
        }
    ],
    "custom_plugins" : [
        {
            "name": "myPlugin",
            "active": true
        }
    ]

}
                        </pre>


                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12">
                        <h1> Acciones </h1>
                        <p>
                            Wordpress-workflow tiene un conjunto de herramientas
                            que deberán ser usadas para actividades cotidianas del
                            desarrollo y puesta en producción, para ver la lista completa
                            se debe usar el siguiente comando en la raíz del proyecto:
                            <br/>
                            <code>fab --list </code>
                        </p>
                        <pre>
Available commands:

activate_theme       Activa el tema seleccionado en la instalacion de wordpress
bootstrap            Crea la base de datos, información de prueba y activa rewrite
environment          Crea la configuración para el entorno en el que correrán las tareas.
export_data          Exporta la base de datos a database/data.sql
import_data          Importa la informacion de database/data.sql
install_plugins      Instala plugins e inicializa segun el archivo settings
reset_all            Borra toda la instación de wordpress e inicia de cero
resetdb              Elimina la base de datos y la vuelve a crear
set_webserver        Cambia el servidor web del proyecto, opciones nginx o apache2
sync_files           Sincroniza los archivos modificados y establece los permisos necesarios en
wordpress_downgrade  Descarga la nueva version de wordpress escrita en settings y
wordpress_install    Descarga la version de wordpress escrita en settings en instala la base
wordpress_upgrade    Descarga la nueva version de wordpress escrita en settings y hace el upgrade
                        </pre>
                        <p>
                            Las tareas se ejecutan seleccionando primero el entorno
                            y después tantas tareas como sean necesarias para lograr el
                            objectivo, por ejemplo para actualizar la versión de wordpress
                            en el entorno de desarrollo. 
                        </p>
                        <code>
                            fab environment:vagrant wordpress_upgrade
                        </code>
                        <p>
                            <br/>
                            O para instalar un nuevo plugin personalizado en staging:
                        </p>
                        <code>
                            fab environment:staging sync_files install_plugins
                        </code>

                        <p>
                            <br/>
                            Para más ejemplos revisar la
                            <a href="#"> Sección de casos de uso </a>
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
