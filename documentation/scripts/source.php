<?php 
  class Source
  {
    private $source;
    const PROJECT = 1;
    const PLUGIN = 2;

    public function setSource($type)
    {
      switch ($type)
      {
        case 1: $this->source = ProjectTestSource::getInstance(); break;
        case 2: $this->source = PluginTestSource::getInstance(); break;
      }
    }

    public function getSource()
    {
      return $this->source->getSrc();
    }

    public function generateSource()
    {
      $this->source->generateSrc();
    }
  }
?>