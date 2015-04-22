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

    <div id="wrapper">

        <!-- Sidebar -->
        <div id="sidebar-wrapper">
        <?php 
            include("menu.php"); 
        ?>
        </div>
        <!-- /#sidebar-wrapper -->

        <!-- Page Content -->
        <div id="page-content-wrapper">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
                        <h1>Commands</h1>
                        <hr/>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12" id="environment" name="environment">
                        <h2>environment</h2>
                        <p>
                            Creates the configurations for the environment in which tasks will run, 
                            <strong>you should always use this command before any other one.</strong>
                        </p>
                        <pre>
$ fab <strong>environment:env_name,[debug]</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <ol>
                            <li><strong>env_name</strong> <i>(string)</i> environment name to create configurations</li>
                            <li><strong>debug</strong> <i>(boolean)</i> defines if fabric output should be displayed, <i>defaulty False</i></li>
                        </ol>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab <strong>environment:vagrant</strong>
$ fab <strong>environment:stage,True</strong>
$ fab <strong>environment:production,true</strong>
                        </pre>

                        <h4>Common combinations</h4>
                        <p><code>environment</code> command is required to excecute most commands, general syntax is as follows:</p>
                        
                        <pre>
$ fab <strong>environment:env_name,[debug]</strong> task1 task2 ... task3
                        </pre>
                        <p>for example:</p>
                        <pre>
$ fab <strong>environment:vagrant</strong> wordpress_upgrade
$ fab <strong>environment:staging,True</strong> sync_files install_plugins
                        </pre>


                   </div>
                   <div class="col-lg-12" id="bootstrap" name="bootstrap">
                        <h2>bootstrap</h2>
                        <p>
                            Creates the database, test information and enables rewrite.
                        </p>
                        <pre>
$ fab environment:[env_name][,debug] <strong>bootstrap</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <p>None</p>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab environment:vagrant <strong>bootstrap</strong>
                        </pre>

                   </div>
                    <div class="col-lg-12" id="crete_config" name="crete_config">
                        <h2>crete_config</h2>
                        <p>
                            Writes wordpress configurations
                        </p>
                        <pre>
$ fab <strong>environment:env_name,[debug]</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <ol>
                            <li><strong>env_name</strong> <i>(string)</i> environment name to create configurations</li>
                            <li><strong>debug</strong> <i>(boolean)</i> defines if fabric output should be displayed, <i>defaulty False</i></li>
                        </ol>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab <strong>environment:vagrant</strong>
$ fab <strong>environment:stage,True</strong>
$ fab <strong>environment:production,true</strong>
                        </pre>

                        <h4>Common combinations</h4>
                        <p><code>environment</code> command is required to excecute most commands, general syntax is as follows:</p>
                        
                        <pre>
$ fab <strong>environment:env_name,[debug]</strong> task1 task2 ... task3
                        </pre>
                        <p>for example:</p>
                        <pre>
$ fab <strong>environment:vagrant</strong> wordpress_upgrade
$ fab <strong>environment:staging,True</strong> sync_files install_plugins
                        </pre>


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
