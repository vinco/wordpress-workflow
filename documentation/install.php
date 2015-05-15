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
        <link href="css/bootstrap.css" rel="stylesheet">

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
        <nav class="navbar navbar-inverse navbar-fixed-top">
          <div class="container-fluid">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
              
              <a class="navbar-brand" href="index.php">
                <img src="images/wwb.png" alt="">
                <span>Wordpress-<strong>Workflow</strong></span>
              </a>
            </div>
          </div><!-- /.container-fluid -->
        </nav>
        <div id="wrapper">

        <!-- Sidebar -->
        <div id="sidebar-wrapper">
        <?php include("menu.php") ?>
        </div>
        <!-- /#sidebar-wrapper -->

        <!-- Page Content -->
        <div id="page-content-wrapper">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
                        <h1> Installation </h1>
                        <hr>
                        <p>
                            The installation is very simple, you only should create the folder where we will take the project
                            and add wordpress-workflow as a submodule. Just after that you must run the shell script
                            <code>startProject.sh</code> that is responsible for generating the basic structure of the project.
                        </p>
                        <p>
                            <strong> All commands must be executed as a regular user, never as root </strong>
                        </p>
                        <pre>
$ mkdir new-project
$ cd new-project
$ git init
$ git submodule add git@github.com:vinco/wordpress-workflow.git
$ wordpress-workflow/startProject.sh
                        </pre>
                        <p>
                            After this, you must place the theme that you will use in the project in the folder <code>src/theme</code>
                        </p>
                        <p>
                            Wordpress-workflow comes already integrated with a default development environment called <code> vagrant </code>
                            so you must not modify it until it is necessary to generate a new environment.
                        </p>
                        <p>
                            You must modify the configuration file <code>settings.json</code>
                            with the specific project information. <br>

                            The variable <code>plugins</code> must contain the plugins that we want to use
                            directly and without modifications from the page of wordpress. <br>
                            The variable <code>custom_plugins</code> contains the plugins that we have modified
                            or that are not in the official repository of wordpress and should be
                            available in <code>src/plugins/</code>
                        </p>
                        <p>
                            Once you have changed the files to our convenience, you should only start the installation of wordpress 
                            running the <code>bootstrap</code> task
                        </p>
                        <pre>
$ fab environment:vagrant bootstrap
                        </pre>
                        <p>
                            At this point the project should be available in <code>http://wordpress.local</code>
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
