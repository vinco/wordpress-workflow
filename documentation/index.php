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
        <?php include("menu.php") ?>
        </div>
        <!-- /#sidebar-wrapper -->

        <!-- Page Content -->
        <div>
        <div id="page-content-wrapper">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
                        <h1 name="wordpress-workflow">Wordpress-workflow</h1>
                        <p>
                            Wordpress-workflow is a tool that has been designed to keep the code of wordpress projects isolated
                            of the core and source files from third party plugins.
                        </p>
                        <h1>Objective</h1>
                        <p>
                            Provide tools and procedures to carry out a proper versions control made in wordpress
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

                        <h1>Environments</h1>
                        <p>
                            The environments are the servers where information will be displayed, each one should have a
                            unique name assigned in the <code>environments.json</code> file.
                        </p>

                        <p>This file contains the description of the environments where your project will be running. 
                        By default, it is populated with the <code>vagrant</code> environment that defines all the required paramaters 
                        to interact with the development Vagrant VM.</p>

                        <p>You must append the definition of your live devel, staging, production and any environment that 
                        you require. Initially <code>environments.json</code> should have the following structure:</p>

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
                            Note that:
                        </p>

                        <ul>
                            <li>You must define a user, group and an array of hosts for your environment.</li>
                            <li>Every directory path must end with a slash (/).</li>
                            <li>You can define an array of command prefixes that should be activated before a 
                            command is run in an environment. You must only list the path to your prefix scripts.</li>
                        </ul>

                        <p>
                            To run a task in an environment you must call the facbric's environment task specifying 
                            with a colon the name of the environment.
                        </p>

                        <pre>
<i># To run a task in the Vagrant VM</i>
$ fab environment:vagrant ...

<i># To run a task in the statging environment</i>
$ fab environment:devel ...
                        </pre>


                        <h1>Settings</h1>
                        <p> 
                            Wordpress general settings are located in <code>settings.json</code>, this file contains 
                            the general project configuration, you need to set it before installing wordpress or 
                            running the fabric commands, the file looks as follows:
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

                        <p>
                            You need to have the <code>theme</code> in <code>src/themes/</code> 
                            otherwise the installation will fail.
                        </p>

                        <p>
                            Every plugin you specify in <code>plugins</code> must be an official 
                            plugin in wordpress.org/plugins, and will be installed for you.
                        </p>
                        
                        <p>
                            Any plugin in <code>custom_plugins</code> must be placed on <code>src/plugins/</code> 
                            sinces the plugins won't be downloaded and are intended for your code.
                        </p>
                        
                        <p>
                            (You can set the version and locale to whatever you need for your project)
                        </p>


                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12">
                        <h1> Actions </h1>

                        <p>
                            Wordpress-workflow has a set of tools that can be used for 
                            development and deployment of wordpress projects.
                        </p>

                        <p>
                            Tasks are executed by first selecting the environment
                            and after as many tasks as are necessary to achieve the
                            objective.
                        </p>

                        <p>
                            <strong>General syntax</strong>
                        </p>

                        <code>
                            $ fab environment:[environment_name] task1 task2 ... task3
                        </code>
                        
                        <p>
                        <br/>
                            For example to update the wordpress version
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

                        <p>
                            You can see all the available actions by running the following command
                            in the project's root:
                        </p>

                        <p>
                            <code>fab --list </code>
                        </p>

                        <p>Available commands:</p>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Command</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tr>
                                <td><a href="commands.php#environment">environment</a></td>
                                <td>Creates the configurations for the environment in which tasks will run.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#bootstrap">bootstrap</a></td>
                                <td>Creates the database, test information and enables rewrite.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#create_config">create_config</a></td>
                                <td>Writes wordpress configurations</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#set_debug_mode">set_debug_mode</a> </td>
                                <td>Changes debug mode, false by default</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#wordpress_install">wordpress_install</a></td>
                                <td>Downloads the wordpress version specified in settings.json and installs the database.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#activate_theme">activate_theme</a> </td>
                                <td>Activates the selected theme in the current wordpress installation.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#install_plugins">install_plugins</a></td>
                                <td>Installs plugins and initialize according to the settings.json file.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#change_domain">change_domain</a> </td>
                                <td>Changes the project's domain according to the url configuration from environment.json</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#import_data">import_data</a> </td>
                                <td>Imports the database from given file name. database/data.sql by default.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#export_data">export_data</a></td>
                                <td>Exports the database to given file name. database/data.sql by default.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#resetdb">resetdb</a></td>
                                <td>Drops the database and recreate it.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#reset_all">reset_all</a></td>
                                <td>Deletes all the wordpress installation and starts over.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#sync_files">sync_files</a> </td>
                                <td>Sync modified files and establish necessary permissions in selected environment.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#wordpress_upgrade">wordpress_upgrade</a> </td>
                                <td>Downloads the new wordpress version specified in settings.json and upgrade it.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#wordpress_downgrade">wordpress_downgrade</a></td>
                                <td>Downloads the new specified wordpress version in settings.json and downgrade it</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#set_webserver">set_webserver</a></td>
                                <td>Changes project's web server, nginx or apache2 available, nginx by default.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#upgrade_plugin">upgrade_plugin</a></td>
                                <td>Updates a plugin to specified version in settings.json.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#check_plugins">check_plugins</a></td>
                                <td>Verifies installed versions of plugins.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#clean_plugins">clean_plugins</a></td>
                                <td>Checks for installed plugins and removes the unused.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#make_tarball">make_tarball</a> </td>
                                <td>Generates a tallbar to upload to servers without ssh.</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#backup">backup</a></td>
                                <td>Generates a backup copy of database and uploads</td>
                            </tr>
                            <tr>
                                <td><a href="commands.php#wordpress_workflow_upgrade">wordpress_workflow_upgrade</a></td>
                                <td>Upgrades wordpress-workflow</td>
                            </tr>
                        </table>
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
