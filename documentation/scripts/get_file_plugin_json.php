<?php 
  header('Content-type: application/json');
  require_once "source_interface.php";
  require_once "source_actions.php";
  require_once "plugin_test_source.php";
  require_once "source.php";

  $source = new Source();
  session_start();
  $source->setSource(Source::PLUGIN);
  if(isset($_SESSION[PluginTestSource::TMPSESSIONNAME]))
  {
    echo $source->getSource();
  }
    
?>