<?php
	// $path = htmlspecialchars($_GET['path']);
	$report_type = htmlspecialchars($_GET['report_type']);

	if($report_type == 'project_src_test'){
		$path = '/home/vagrant/wordpress-workflow/';
	}
	else if($report_type == 'third_party_plugins_test'){
		$path = '/home/vagrant/public_www/wp-content/plugins';
	}
	$command = 'phpcs --standard=WordPress-Core '.
            '--report=json '.
            $path;

	system($command, $retval);
?>