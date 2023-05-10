<?php

$dir = $_POST['dirpath'];



if (is_dir($dir)){
  	if ($dh = opendir($dir)){
    	while (($file = readdir($dh)) !== false){
    		if ($file != ".." and $file != "." and strpos($file, ".") != 0 and false == is_dir($file)) {
    			$files .= "," . $dir . $file;
    		}
    	}
    	closedir($dh);
  	}
}
$files = trim($files, ",");
echo $files;

?>
