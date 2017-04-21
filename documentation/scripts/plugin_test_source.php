<?php 
  class PluginTestSource extends SourcesActions implements SourceInterface
  {
    private static $instance;
    const TMPSESSIONNAME = "plugin_src_tmp_file";
    const TMPNAME = "plugin_src";
    private function __construct()
    {
      $this->tmpSessionName = "plugin_src_tmp_file";
      $this->tmpName = "plugin_src";
      $this->path = "/home/ubuntu/public_www/wp-content/plugins";
      $this->command = 'phpcs --standard=WordPress-Core '.
            '--report=json '.
            $this->path;
    }
    public static function getInstance()
    {
      if(null == static::$instance)
      {
        static::$instance = new static;
      }
      return static::$instance;
    }

    public static function destroyInstance()
    {
      if(null != static::$instance)
      {
        static::$instance = null;
      }
    }
  }
?>