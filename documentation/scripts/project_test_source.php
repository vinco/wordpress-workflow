<?php 
  class ProjectTestSource extends SourcesActions implements SourceInterface
  {
    private static $instance;
    const TMPSESSIONNAME = "project_src_tmp_file";
    const TMPNAME = "project_src";

    private function __construct()
    {
      $this->tmpSessionName = "project_src_tmp_file";
      $this->tmpName = "project_src";
      $this->path = "/home/vagrant/public_www/wp-content/";
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