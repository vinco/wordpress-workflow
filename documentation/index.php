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
                            Wordpress-workflow is a tool that has been designed to keep the code of wordpress projects isolated
                            of the core and source files from third party plugins.
                        </p>
                        <h1>Objetivo</h1>
                        <p>
                            Provide tools and procedures to carry out a proper versions control and changes made in wordpress
                            projects.
                        </p>
                        <p>
                            The package is maintained by Vinco Orbis, suggestions and bug reports must be made to
                            <a href="https://github.com/vinco/wordpress-workflow">https://github.com/vinco/wordpress-workflow</a>
                            as a new issue.
                        </p>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12">
                        <h1> Structure </h1>
                        <p>
                            Once installed Wordpress-workflow should have the following structure:
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
                            All the code that is generated for the project should go in the src folder, this folder is
                            the one that syncs with the servers so it is very important to mention that <strong>Any
                            code in other section will not be synchronized with the servers</strong>.
                        </p>
                        <p>
                          There are only two situations in which the code of the plugins should be added to the repository
                        </p>   
                        <ol>
                           <li>The plugin is ours</li>
                           <li>It is a custom third party plugin</li>
                        </ol>

                        <h1>Settings and environments</h1>
                        <p>
                            The environments are the servers where information will be displayed, each one should have a
                            unique name assigned in the <code>environments.json</code> file, which has the following structure:
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
                            Wordpress general settings are located in settings.json and looks as follows:
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
                        <h1> Actions </h1>
                        <p>
                            Wordpress-workflow has a set of tools
                            that should be used for day to day activities of the
                            development and deployment, to see the complete list
                            you should use the following command in the project root:
                            <br/>
                            <code>fab --list </code>
                        </p>
                        <pre>
Available commands:

activate_theme       Activates the selected theme in the current wordpress installation.
bootstrap            Creates the database, test information and enables rewrite.
environment          Creates the configurations for the environment in which tasks will run.
export_data          Exports the database to given file name. database/data.sql by default.
import_data          Imports the database to given file name. database/data.sql by default.
install_plugins      Installs plugins and initialize according to the settings.json file.
reset_all            Deletes all the wordpress installation and starts over.
resetdb              Drops the database and recreate it.
set_webserver        Changes project's web server, nginx or apache2 available, nginx by default.
sync_files           Sync modified files and establish necessary permissions in selected environment.
wordpress_downgrade  Downloads the new specified wordpress version in settings.json and downgrade it
wordpress_install    Downloads the wordpress version specified in settings.json and installs the database.
wordpress_upgrade    Downloads the new wordpress version specified in settings.json and upgrade it.
                        </pre>
                        <p>
                            The tasks are executed by first selecting the environment
                            and after as many tasks as are necessary to achieve the
                            objective, for example to update the wordpress version
                            in the development environment.
                        </p>
                        <code>
                            fab environment:vagrant wordpress_upgrade
                        </code>
                        <p>
                            <br/>
                            Or to install a new custom pluging in staging environment:
                        </p>
                        <code>
                            fab environment:staging sync_files install_plugins
                        </code>

                        <p>
                            <br/>
                            for more examples, take a look at the 
                            <a href="#">use cases section </a>
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
