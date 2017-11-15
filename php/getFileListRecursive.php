<?php
// ini_set('display_errors', 1);

$dir = $_POST['dirpath'];
$dir = "/var/www/html" . $dir;
$files = "";

$objects = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir), RecursiveIteratorIterator::SELF_FIRST);
foreach($objects as $file => $object){
	$tmp = explode("/", $file);
	$filename = end($tmp);
	if ($filename != ".." and $filename != "." and strpos($filename, ".") != 0) {
		$files .= "," . str_replace("/var/www/html", "", $file);
	}
}

$files = trim($files, ",");
echo $files;




?>