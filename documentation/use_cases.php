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
                    <div class="col-lg-12" id="change_theme">
                        <h1> Casos de uso</h1>
                        <hr/>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="change_theme" name="change_theme">
                        <h2> Cambiar de tema </h2>
                        <p>
                            Aseguramos que el nuevo tema este colocado
                            en <code>src/themes</code><br/>
                            
                            Modificamos <code>settings.json</code>
                            Asegurádonos que el nombre se ajuste al nuevo tema en el
                            sitiio<br/>
                            
                            Instalamos el nuevo sitio en desarrollo
                        </p>
                        <pre>
$ fab environment:vagrant activate_theme
                        </pre>
                        <p>
                            Una vez comprobado que el tema funciona y realizar
                            los commits necesarios en git podemos hacer deployment de la
                            siguiente manera:
                        </p>
                        <pre>
$ fab environment:ambiente sync_files activate_theme
                        </pre>
                   </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="add_plugin" name="add_plugin">
                        <h2> Agregar plugin </h2>
                        <p>
                            Modificamos el archivo <code> settings.json </code>
                            agregando el plugin a agregar y lo instalamos en el entorno local
                        </p>
                        <pre>
$ fab environment:vagrant install_plugins
                        </pre>
                        <p>
                            Una vez se ha comprobado que funciona de manera correcta podemos
                            hacer deployment de la siguiente manera
                        </p>
                        <pre>
$ fab environment:ambiente install_plugins
                        </pre>
                    </div>
                </div>

                <div class="row">
                    <div class="col-lg-12" id="add_custom_plugin" name="add_custom_plugin">
                        <h2> Agregar plugin personalizado </h2>
                        <p>
                            Creamos la carpeta del plugin junto con su código en
                            <code> src/plugins</code>, lo agregamos al arreglo <code>custom_plugins</code> 
                            en el archivo <code>settings.json</code>y lo instalamos en el entorno
                            local de la siguiente manera:
                        </p>
                        <pre>
$ fab environment:ambiente install_plugins
                        </pre>
                        <p>
                            Una vez se ha comprobado que funciona de manera correcta podemos
                            hacer deployment de la siguiente manera
                        </p>
                        <pre>
$ fab environment:ambiente sync_files install_plugins
                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="backup" name="backup">
                        <h2> Respaldar información </h2>
                        <p> 
                            Para respaldar la información se ejecuta el comando
                            <code> export_data</code> que generá un archivo 
                            <code>src/database/data.sql</code> en el entorno selccionado.<br/>

                            Para descargar esta información a algún otro entorno se debe usar otra herramienta
                            como puede ser scp, por ejemplo:
                        </p>
                        <pre>
$ fab environment:production export_data
$ scp user@server:/home/user/wpworkflow/src/database/data.sql /home/local/respaldo.sql
                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="install_info" name="install_info">
                        <h2> Instalar información </h2>
                        <p>
                            Para instalar información en el servidor local
                            sólo debemos tener el archivo a cargar en <code>src/database/data.sql</code>
                            y ejecutar la instrucción <code> import_data </code>
                        </p>
                        <pre>
$ fab environment:vagrant reset_db import_data
                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="upgrade_wordpress" name="upgrade_wordpress">
                        <h2> Actualizar wordpress </h2>
                        <p>
                            Sólo debemos cambiar en el archivo <code>settings.json</code> la versión
                            de wordpress a la que queremos actualizar y ejecutamos:
                        </p>
                        <pre>
$ fab environment:vagrant wordpress_upgrade
                        </pre>
                        <p>
                            Una vez se ha comprobado que funciona de manera correcta podemos
                            hacer deployment de la siguiente manera
                        </p>
                        <pre>
$ fab environment:ambiente wordpress_upgrade
                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="use_apache2_nginx" name="use_apache2_nginx">
                        <h2> Usar apache2/nginx </h2>
                        <p>
                            Wordpress-workflow por default viene instalado con nginx, si se desea
                            probar el código en una instalación de apache se puede hacer ejecutando
                            el comando <code> set_webserver:server</code>. <br/>
                            Se debe de tomar en cuenta que esta configuración no es persistente y se deberá
                            ejecutar el comando cada vez que se encienda la máquina virtual. 
                        </p>
                        <p>
                            Para usar apache2
                        </p>
                        <pre>
$ fab environment:vagrant set_webserver:apache2
                        </pre>
                        <p>
                            Para activar nginx sin necesidad de reiniciar el entorno virtual:
                        </p>
                        <pre>
$ fab environment:vagrant set_webserver:nginx
                        </pre>
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
