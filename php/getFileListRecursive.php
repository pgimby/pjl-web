<?php
// ini_set('display_errors', 1);

$dir = $_POST['dirpath'];
$dir = "/var/www/html" . $dir;

$objects = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir));
foreach($objects as $file => $object){
	$filename = end(explode("/", $file));
	if ($filename != ".." and $filename != "." and strpos($filename, ".") != 0) {
		$files .= "," . str_replace("/var/www/html", "", $file);
	}
}

$files = trim($files, ",");
echo $files;




?>