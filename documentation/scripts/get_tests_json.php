<?php

	session_start();
	header('Content-type: application/json');
	require_once "source_interface.php";
	require_once "source_actions.php";
	require_once "project_test_source.php";
	require_once "plugin_test_source.php";
	require_once "source.php";

	$report_type = htmlspecialchars($_GET['report_type']);
	$source = new Source();
	if($report_type == 'project_src_test'){
		$source->setSource(Source::PROJECT);
		$source->generateSource();
		echo $source->getSource();
		}
	else if($report_type == 'third_party_plugins_test'){
		$source->setSource(Source::PLUGIN);
		$source->generateSource();
		echo $source->getSource();
	}

?>