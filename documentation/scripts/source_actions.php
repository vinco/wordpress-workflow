<?php 
  
  abstract class SourcesActions
  {
    public $command;
    public $path;
    public $tmpFile;
    public $tmpSessionName;
    public $tmpName;

    public function getSrc()
    {
      $path_file = $_SESSION[$this->tmpSessionName];
      $content_file = file_get_contents( $path_file );
      return $content_file;
    }
    public function generateSrc()
    {
      $this->resetSrc();
      $retVal = array();
      exec($this->command, $retVal);
      $jsonRetVal = json_encode($retVal);
      $tmpFilePath = tempnam(sys_get_temp_dir(), $this->tmpName);
      $this->tmpFile = fopen($tmpFilePath, 'a');
      fwrite($this->tmpFile, $jsonRetVal);
      $_SESSION[$this->tmpSessionName] = $tmpFilePath;
    }

    public function resetSrc()
    {
      $pathFile = $_SESSION[$this->tmpSessionName];
      $file = fopen($pathFile, 'r');
      if(isset($_SESSION[$this->tmpSessionName])):
        fclose($file);
        unset($_SESSION[$this->tmpSessionName]);
      endif;
    }
  }
?>