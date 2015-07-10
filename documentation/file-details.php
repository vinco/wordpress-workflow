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
	    <link href="css/highlight.min.css" rel="stylesheet">
	    <link href="css/dashboard.css" rel="stylesheet">

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
		      	<span>Wordpress-<strong>workflow</strong></span>
		      </a>
		    </div>
		  </div><!-- /.container-fluid -->
		</nav>
	    <div id="wrapper">
	        <!-- Sidebar -->
	        <div id="sidebar-wrapper">
	        <?php include("menu.php") ?>
	        </div>

	                <!-- Page Content -->
        <div>
        <div id="page-content-wrapper">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-12">
                        <h1 name="wordpress-workflow">File details</h1>
                        <h4 id="file-name-title"></h4>
                        <hr>

                        <section id="file-details-content">
                        	<article id="file-details-list" >
                        		<div class="table-responsive">
                              
                            </div>
                        	</article>
                        </section>
                        
                    </div>
                </div>
            </div>
        <!-- /#page-content-wrapper -->
        </div>
    <!-- /#wrapper -->
    
    <!-- jQuery -->
    <script src="js/jquery.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.js"></script>
    <script src="js/Chart.min.js"></script>
    <script src="js/lodash.min.js"></script>
    <script src="js/highlight.min.js"></script>

    <script>
		var file_path = '<?php echo $_GET["file_path"]; ?>';
		var report_type = '<?php echo $_GET["report_type"]; ?>';
    </script>

    <script src="js/dashboard.js"></script>
</body>

</html>
