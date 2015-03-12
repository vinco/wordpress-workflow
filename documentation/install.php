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
                        <h1> Instalación </h1>
                        <p>
                            La instalación es muy sencilla, sólo se debe de crear la carpeta donde llevaremos el proyecto
                            y agregar como submódulo wordpress workflow. Justo después se debe ejecutar el script de shell
                            startProject.sh que se encarga de generar la estructura básica del proyecto.
                        </p>
                        <p>
                            <strong> Todos los comandos deben ser ejecutados como usuario normal, nunca como root </strong>
                        </p>
                        <pre>
$ mkdir new-project
$ cd new-project
$ git init
$ git submodule add git@github.com:vinco/wordpress-workflow.git
$ wordpress-workflow/startProject.sh
                        </pre>
                        <p>
                            Después de esto se debe de colocar el tema que usará en el proyecto en la carpeta src/themes
                        </p>
                        <p>
                            Wordpress-workflow viene integrado ya con el ambiente default de desarrollo <code> vagrant </code>
                            por lo que no se deberá modificar hasta que sea necesario generar un nuevo ambiente.
                        </p>
                        <p>
                            Se debe modificar el archivo de configuración <code>settings.json</code>
                            con la información específica del proyecto. <br/>
                            La variable <code>plugins</code> deberá contener los plugins que deseamos usar
                            directamente y sin modificaciones desde la página de wordpress. <br/>
                            La variable <code>custom_plugins</code> contiene los plugins que nosotros hemos modificado
                            o que no se encuentran en el repositorio oficial de wordpress y deberán estar
                            disponibles en <code>src/plugins/</code>
                        </p>
                        <p>
                            Una vez modificados los archivos a nuestra convenencia sólo se debe iniciar la instalación de wordpress
                            ejecutando la tarea <code>bootstrap</code>
                        </p>
                        <pre>
$ fab environment:vagrant bootstrap
                        </pre>
                        <p>
                            Una vez hecho esto el proyecto estará disponible en <code>http://wordpress.local</code>
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
