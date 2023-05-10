<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

$dir1 = $_POST['dirpath'];
$dir = "/var/www/html" . $dir1;
$files = "";

$iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir), RecursiveIteratorIterator::SELF_FIRST);
$objects = iterator_to_array($iterator);

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