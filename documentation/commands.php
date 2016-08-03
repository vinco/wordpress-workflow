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
                            <strong>most of cases you will need to use this command before other one.</strong>
                        </p>
                        <pre>
$ fab <strong>environment:<span class="args">env_name[,debug]</strong></span>
                        </pre>

                        <h4>Arguments</h4>
                        <ol>
                            <li><strong><span class="args">env_name</span></strong> <i>(string)</i> environment name to create configurations 
                                <i>(<strong>Required</strong>).</i></li>
                            <li><strong><span class="args">debug</span></strong> <i>(boolean)</i> defines if fabric output should be displayed, 
                                <i>(False by default).</i></li>
                        </ol>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab <strong>environment:<span class="args">vagrant</span></strong>
$ fab <strong>environment:<span class="args">stage,True</span></strong>
$ fab <strong>environment:<span class="args">production,true</span></strong>
                        </pre>

                        <p><code>environment</code> command is required to excecute most commands, general syntax is as follows:</p>
                        
                        <pre>
$ fab <strong>environment:<span class="args">env_name[,debug]</span></strong> task1 task2 ... task3
                        </pre>
                        <p>for example:</p>
                        <pre>
$ fab <strong>environment:<span class="args">vagrant</span></strong> wordpress_upgrade
$ fab <strong>environment:<span class="args">staging,True</span></strong> sync_files install_plugins
                        </pre>


                   </div>
                   <div class="col-lg-12 anchor" id="bootstrap" name="bootstrap">
                        <h2>bootstrap</h2>
                        <p>
                            Creates the database, test information and enables rewrite.
                        </p>
                        <pre>
$ fab environment:env_name[,debug] <strong>bootstrap</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <p>None</p>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab environment:vagrant <strong>bootstrap</strong>
                        </pre>

                   </div>
                    <div class="col-lg-12 anchor" id="create_config" name="create_config">
                        <h2>create_config</h2>
                        <p>
                            Writes wordpress configurations
                        </p>
                        <pre>
$ fab environment:env_name[,debug] <strong>create_config<span class="args">[:debug]</span></strong>
                        </pre>

                        <h4>Arguments</h4>
                        <ol>
                            <li><strong><span class="args">debug</span></strong> <i>(boolean)</i> defines if wordpress should be configurated as debug mode 
                                <i>(False by default).</i></li>
                        </ol>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab environment:vagrant <strong>create_config</strong>
$ fab environment:vagrant <strong>create_config:<span class="args">True</span></strong>
$ fab environment:vagrant <strong>create_config:<span class="args">False</span></strong>
                        </pre>
                   </div>
                    <div class="col-lg-12 anchor" id="set_debug_mode" name="set_debug_mode">
                        <h2>set_debug_mode</h2>
                        <p>
                            Changes debug mode
                        </p>
                        <pre>
$ fab environment:env_name[,debug] <strong>set_debug_mode<span class="args">[:debug]</span></strong>
                        </pre>

                        <h4>Arguments</h4>
                        <ol>
                            <li><strong><span class="args">debug</span></strong> <i>(boolean)</i> defines if wordpress should be configurated as debug mode 
                                <i>(False by default)</i>.</li>
                        </ol>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab environment:vagrant <strong>set_debug_mode</strong>
$ fab environment:vagrant <strong>set_debug_mode:<span class="args">True</span></strong>
$ fab environment:vagrant <strong>set_debug_mode:<span class="args">False</span></strong>
                        </pre>
                   </div>
                    <div class="col-lg-12 anchor" id="wordpress_install" name="wordpress_install">
                        <h2>wordpress_install</h2>
                        <p>
                            Downloads the wordpress version specified in <code>settings.json</code> and installs the database.
                        </p>
                        <pre>
$ fab environment:env_name[,debug] <strong>wordpress_install</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <p>None</p>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab environment:vagrant <strong>wordpress_install</strong>
                        </pre>
                   </div>
                   <div class="col-lg-12 anchor" id="activate_theme" name="activate_theme">
                        <h2>activate_theme</h2>
                        <p>
                            Activates the selected theme in the current wordpress installation.
                        </p>
                        <pre>
$ fab environment:env_name[,debug] <strong>activate_theme</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <p>None</p>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab environment:vagrant <strong>activate_theme</strong>
                        </pre>
                   </div>
                   <div class="col-lg-12 anchor" id="install_plugins" name="install_plugins">
                        <h2>install_plugins</h2>
                        <p>
                            Installs plugins and initialize according to the <code>settings.json</code> file. Also this function does can install a specific plugin when pass plugin name as argument.
                        </p>
                        <pre>
$ fab environment:env_name[,debug] <strong>install_plugins</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <p><code>@param String name</code> This param refers to specific plugin's name that we require install, this param is default null, if this param is null the command does install all plugins from <code>settings.json</code>.</p>
                        
                        <h4>Examples</h4>
                        <pre>
$ fab environment:vagrant <strong>install_plugins</strong>
                        </pre>
                        <p>If we require install only <code>all-in-one-seo-pack</code> plugin, we type:</p>
                        <pre>
$ fab environment:vagrant <strong>install_plugins</strong>:<strong>"all-in-one-seo-pack"</strong>  // If <code>settings.json</code> does not have "all-in-one-seo-pack" this command show an error
                        </pre>
                   </div>

                    <div class="col-lg-12 anchor" id="change_domain" name="change_domain">
                        <h2>change_domain</h2>
                        <p>
                            Changes the project's domain according to the url configuration from
                            <code>environment.json</code>, this command must only be used with
                            <code>vagrant</code> environment.
                        </p>
                        <pre>
$ fab environment:vagrant <strong>change_domain</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <p>None</p>

                    </div>

                    <div class="col-lg-12 anchor" id="change_prefix" name="change_prefix">
                        <h2>change_prefix</h2>
                        <p>
                            Changes the database table prefix according to the dbprefix
                            configuration from <code>environment.json</code>.
                        </p>
                        <pre>
$ fab environment:vagrant <strong>change_prefix</strong>
                        </pre>

                        <h4>Arguments</h4>
                        <ol>
                            <li><strong><span class="args">old_prefix</span></strong> <i>(string)</i> current prefix.
                                <i>("wp_" by default)</i>.</li>
                        </ol>
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>change_prefix:wp_</strong>
                            </pre>

                    </div>

                    <div class="col-lg-12 anchor" id="import_data" name="import_data">
                            <h2>import_data</h2>
                            <p>
                                Imports the database from given file name that must be placed in <code>database/</code> path
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>import_data<span class="args">[:file_name]</span></strong>
                            </pre>

                            <h4>Arguments</h4>
                            <ol>
                                <li><strong><span class="args">file_name</span></strong> <i>(string)</i> dump file name to import. 
                                    <i>("data.sql" by default)</i>.</li>
                            </ol>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>import_data</strong>
$ fab environment:vagrant <strong>import_data:<span class="args">backup.sql</span></strong>
                            </pre>
                       </div>

                       <div class="col-lg-12 anchor" id="export_data" name="export_data">
                            <h2>export_data</h2>
                            <p>
                                Exports the database to given file name. Generated dump will be placed in <code>database/</code> path
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>export_data<span class="args">[:file_name]</span></strong>
                            </pre>

                            <h4>Arguments</h4>
                            <ol>
                                <li><strong><span class="args">file_name</span></strong> <i>(string)</i> dump file name to export. 
                                    <i>("data.sql" by default)</i>.</li>
                            </ol>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>export_data</strong>
$ fab environment:vagrant <strong>export_data:<span class="args">backup.sql</span></strong>
                            </pre>
                       </div>
                        
                        <div class="col-lg-12 anchor" id="resetdb" name="resetdb">
                            <h2>resetdb</h2>
                            <p>
                                Drops the database and recreate it.
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>resetdb</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <p>None</p>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>resetdb</strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="reset_all" name="reset_all">
                            <h2>reset_all</h2>
                            <p>
                                Deletes all the wordpress installation and starts over.
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>reset_all</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <p>None</p>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>reset_all</strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="sync_files" name="sync_files">
                            <h2>sync_files</h2>
                            <p>
                                Sync modified files and establish necessary permissions in selected environment.
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>sync_files</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <p>None</p>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>sync_files</strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="wordpress_upgrade" name="wordpress_upgrade">
                            <h2>wordpress_upgrade</h2>
                            <p>
                                Downloads the new wordpress version specified in <code>settings.json</code> and upgrades it.
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>wordpress_upgrade</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <p>None</p>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>wordpress_upgrade</strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="wordpress_downgrade" name="wordpress_downgrade">
                            <h2>wordpress_downgrade</h2>
                            <p>
                                Downloads the new specified wordpress version in <code>settings.json</code> and downgrades it
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>wordpress_downgrade</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <p>None</p>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>wordpress_downgrade</strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="set_webserver" name="set_webserver">
                            <h2>set_webserver</h2>
                            <p>
                                Changes project's web server, nginx or apache2 available, nginx by default.
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>set_webserver<span class="args">[:webserver]</span></strong>
                            </pre>

                            <h4>Arguments</h4>
                            <ol>
                                <li><strong><span class="args">webserver</span></strong> webserver name that will be used, you can switch between nginx and apache2
                                    <i>("nginx" by default)</i>.</li>
                            </ol>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>set_webserver</strong>
$ fab environment:vagrant <strong>set_webserver:<span class="args">nginx</span></strong>
$ fab environment:vagrant <strong>set_webserver:<span class="args">apache2</span></strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="upgrade_plugin" name="upgrade_plugin">
                            <h2>upgrade_plugin</h2>
                            <p>
                                Updates a plugin to specified version in <code>settings.json</code>.
                            </p>
                            <p>
                                <strong>Must be an official plugin in wordpress.org/plugins</strong>
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>upgrade_plugin<span class="args">:plugin_name</span></strong>
                            </pre>

                            <h4>Arguments</h4>
                            <ol>
                                <li><strong><span class="args">plugin_name</span></strong> <i>(string)</i> plugin name to update 
                                    <i>(<strong>Required</strong>)</i>.</li>
                            </ol>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>upgrade_plugin:<span class="args">wordpress-seo</span></strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="check_plugins" name="check_plugins">
                            <h2>check_plugins</h2>
                            <p>
                               Verifies installed versions of plugins.
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>check_plugins</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <p>None</p>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>check_plugins</strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="clean_plugins" name="clean_plugins">
                            <h2>clean_plugins</h2>
                            <p>
                               Checks for installed plugins and removes the unused.
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>clean_plugins</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <p>None</p>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>clean_plugins</strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="make_tarball" name="make_tarball">
                            <h2>make_tarball</h2>
                            <p>
                                Generates a tarball to upload to servers without ssh.
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>make_tarball:<span class="args">target_environment[,tar_name</span>]</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <ol>
                                <li><strong><span class="args">target_environment</span></strong> <i>(string)</i> Environment that will be used to generate tallbar
                                    <i>(<strong>Required</strong>)</i>.</li>

                                <li><strong><span class="args">tar_name</span></strong> <i>(string)</i> Name for generated tallbar
                                    <i>("wordpress-dist" by default)</i>.</li>
                            </ol>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>make_tarball:<span class="args">development</span></strong>
$ fab environment:vagrant <strong>make_tarball:<span class="args">production,production_tarball</span></strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="backup" name="backup">
                            <h2>backup</h2>
                            <p>
                                Generates a backup copy of database and uploads
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>backup<span class="args">[:tarball_name][,just_data]</span></strong>
                            </pre>

                            <h4>Arguments</h4>
                            <ol>
                            <li><strong><span class="args">tarball_name</span></strong> In which you can specify the custom name 
                                for the generated tarball. <i>("backup" by default)</i>.</li>

                            <li><strong><span class="args">just_data</span></strong> Specifies if CREATE TABLE statements should be 
                            excluded in the generated dump file. <i>(False by default)</i>.</li>
                        </ol>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>backup</strong>
$ fab environment:vagrant <strong>backup:<span class="args">database_backup,True</span></strong>
$ fab environment:vagrant <strong>backup:<span class="args">database_backup,False</span></strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="verify-checksums" name="verify-checksums">
                            <h2>verify checksums</h2>
                            <p>
                                Verify checksums from wordpress core and the repair if it fails
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>verify-checksums</strong>
                            </pre>

                            <h4>Arguments</h4>
                            <p>None</p>
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>verify-checksums</strong>
                            </pre>
                       </div>
                       <div class="col-lg-12 anchor" id="wordpress_workflow_upgrade" name="wordpress_workflow_upgrade">
                            <h2>wordpress_workflow_upgrade</h2>
                            <p>
                                Upgrades wordpress-workflow
                            </p>
                            <pre>
$ fab environment:env_name[,debug] <strong>wordpress_workflow_upgrade<span class="args">[:repository][,branch]</span></strong>
                            </pre>

                            <h4>Arguments</h4>
                            <ol>
                            <li><strong><span class="args">repository</span></strong> Repository name to use in wordpress-workflow upgrade. 
                                <i>("origin" by default)</i>.</li>

                            <li><strong><span class="args">branch</span></strong> Branch name to use in wordpress-workflow upgrade. 
                                <i>("master" by default)</i>.</li>
                        </ol>
                            
                            <h4>Examples</h4>
                            <pre>
$ fab environment:vagrant <strong>wordpress_workflow_upgrade</strong>
$ fab environment:vagrant <strong>wordpress_workflow_upgrade:<span class="args">origin,master</span></strong>
$ fab environment:vagrant <strong>wordpress_workflow_upgrade:<span class="args">upstream</span></strong>
$ fab environment:vagrant <strong>wordpress_workflow_upgrade:<span class="args">upstream,develop</span></strong>
$ fab environment:vagrant <strong>wordpress_workflow_upgrade:<span class="args">origin,develop</span></strong>
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
