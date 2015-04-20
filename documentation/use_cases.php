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
                        <h2> Change theme </h2>
                        <p>
                            Make sure that the new theme is placed in
                            <code>src/themes</code>.
                        </p>
                        <p>
                            Modify <code>settings.json</code> and make sure that
                            the name fits with the new theme in the site.
                        </p>
                        <p>
                            Then activate the new theme by running the following command:
                        </p>

                        <pre>
$ fab environment:vagrant activate_theme
                        </pre>
                        <p>
                            Once you have verified that the theme works and perform
                            the needed commits in git, you can do deployment as follows:
                        </p>
                        <pre>
$ fab environment:[environment_name] sync_files activate_theme
                        </pre>
                   </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="add_plugin" name="add_plugin">
                        <h2> Add plugin </h2>
                        <p>
                            Modify the <code> settings.json </code> file adding the new plugin,
                            then you need to install it in the local environment.
                        </p>
                        <p>
                            Once you are sure that the new plugin works correctly you can do
                            deployment with the next command:
                        </p>
                        <pre>
$ fab environment:[environment_name] install_plugins
                        </pre>
                    </div>
                </div>

                <div class="row">
                    <div class="col-lg-12" id="add_custom_plugin" name="add_custom_plugin">
                        <h2> Add a custom plugin </h2>
                        <p>
                            To use custom plugins, you need to add the code in <code>src/plugins</code> folder,
                            also you need to add it to the <code>custom_plugins</code> array inside of
                            <code>settings.json</code> file.
                        </p>

                        <p>
                            Then install it by running the following command:
                        </p>

                        <pre>
$ fab environment:[environment_name] install_plugins
                        </pre>
                        <p>
                            Once you have been verified that it works correctly you can do deployment as follows:
                        </p>
                        <pre>
$ fab environment:[environment_name] sync_files install_plugins
                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="backup" name="backup">
                        <h2>Backup information</h2>
                        <p> 
                            To make information backups, you need to run the
                            <code> export_data</code> command, that will generate a
                            <code>src/database/data.sql</code> file in the selected environment.

                            To download the information backup to any other environment, you should use a tool
                            as can be scp, for example:
                        </p>
                        <pre>
$ fab environment:production export_data
$ scp user@server:/home/user/wpworkflow/src/database/data.sql /home/local/respaldo.sql
                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="install_info" name="install_info">
                        <h2>Restore information</h2>
                        <p>
                            To restore information in the local server, you only need to have the backup file
                            in <code>src/database/data.sql</code> and excecute the <code> import_data </code>
                            command, as follows:
                        </p>
                        <pre>
$ fab environment:vagrant reset_db import_data
                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="upgrade_wordpress" name="upgrade_wordpress">
                        <h2> Update wordpress </h2>
                        <p>
                            You only need to change the <code>version</code> variable that is located inside
                            <code>settings.json</code> file to the wordpress version that you need to
                            update, then run the next command:
                        </p>
                        <pre>
$ fab environment:vagrant wordpress_upgrade
                        </pre>
                        <p>
                            Once you have been check that everything works correctly, you can
                            do deployment as follows:
                        </p>
                        <pre>
$ fab environment:[environment_name] wordpress_upgrade
                        </pre>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="use_apache2_nginx" name="use_apache2_nginx">
                        <h2> Usar apache2/nginx </h2>
                        <p>
                            Wordpress-workflow by default comes installed with nginx, if you want to
                            test the code with apache server, it can be done by running
                            the command <code> set_webserver:server</code>.
                        </p>
                        <p>
                            you must notice that this configuration is not permanent, and you should
                            run the command every time you need it, when the virtual machine turns on.
                        </p>
                        <p>
                            To use apache2
                        </p>
                        <pre>
$ fab environment:vagrant set_webserver:apache2
                        </pre>
                        <p>
                            To enable nginx without the need to restart the virtual environment:
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
