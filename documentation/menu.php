

<div class="panel-group text-center" id="accordion" role="tablist" aria-multiselectable="true">
  
    <div class="panel panel-default">
        <div class="panel-heading logo text-center">
          <h4 class="panel-title">
            <a href="index.php">
               <img src="images/wwc.png" alt="wordpress-workflow logo" />
               <span>Wordpress-workflow</span>
            </a>
          </h4>
        </div>
    </div>
        

    <a href="index.php">
        <div class="panel panel-default">
            <div class="panel-heading">
              <h4 class="panel-title">
                  Summary 
              </h4>
            </div>
        </div>
    </a>

    <a href="install.php">
        <div class="panel panel-default">
            <div class="panel-heading">
              <h4 class="panel-title">
                  Installation
              </h4>
            </div>
        </div>
    </a>

    <a href="update.php">
        <div class="panel panel-default">
            <div class="panel-heading">
              <h4 class="panel-title">
                  Update
              </h4>
            </div>
        </div>
    </a>

    <a class="collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
      <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="headingTwo">
          <h4 class="panel-title">
              Use cases
          </h4>
        </div>
        <div id="collapseTwo" class="panel-collapse collapse <?php if($_SERVER['REQUEST_URI'] == '/use_cases.php'){ echo 'in'; } ?>" role="tabpanel" aria-labelledby="headingTwo">
            <ul class="list-group">
                <li class="list-group-item">
                    <a href="use_cases.php#change_theme">
                        Change theme
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="use_cases.php#add_plugin">
                        Add plugin
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="use_cases.php#add_custom_plugin">
                        Add custom plugin
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="use_cases.php#backup">
                        Backup information
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="use_cases.php#install_info">
                        Restore information
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="use_cases.php#upgrade_wordpress">
                        Update wordpress
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="use_cases.php#use_apache2_nginx">
                        Use apache2/nginx
                    </a>
                </li>
            </ul>
        </div>
      </div>
    </a>

    <a id="commands" class="collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
      <div class="panel panel-default">
        <div class="panel-heading" role="tab" id="headingThree">
          <h4 class="panel-title">
              Commands
          </h4>
        </div>
        <div id="collapseThree" class="panel-collapse collapse <?php if($_SERVER['REQUEST_URI'] == '/commands.php'){ echo 'in'; } ?>" role="tabpanel" aria-labelledby="headingThree">
          <ul class="list-group">
                <li class="list-group-item">
                    <a href="commands.php#environment">
                        environment
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#bootstrap">
                        bootstrap
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#create_config">
                        create_config
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#set_debug_mode">
                        set_debug_mode
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#wordpress_install">
                        wordpress_install
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#activate_theme">
                        activate_theme
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#install_plugins">
                        install_plugins
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#import_data">
                        import_data
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#export_data">
                        export_data
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#resetdb">
                        resetdb
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#reset_all">
                        reset_all
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#sync_files">
                        sync_files
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#wordpress_upgrade">
                        wordpress_upgrade
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#wordpress_downgrade">
                        wordpress_downgrade
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#set_webserver">
                        set_webserver
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#upgrade_plugin">
                        upgrade_plugin
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#check_plugins">
                        check_plugins
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#clean_plugins">
                        clean_plugins
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#search_plugin">
                        search_plugin
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#make_tarball">
                        make_tarball
                    </a>
                </li>
                <li class="list-group-item">
                    <a href="commands.php#backup">
                        backup
                    </a>
                </li>
            </ul>
        </div>
      </div>
    </a>
</div>
