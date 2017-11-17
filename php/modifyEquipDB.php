<?php
// ini_set('display_errors', 1);
$name = $_POST['eq-name'];
$make = $_POST['eq-make'];
$model = $_POST['eq-model'];
$total = $_POST['eq-total'];
$service = $_POST['eq-service'];
$repair = $_POST['eq-repair'];
$rooms = $_POST['eq-room'];
$stores = $_POST['eq-storage'];
$xml=simplexml_load_file("/var/www/html/data/equipmentDB.xml") or die("Error: Cannot create object");

foreach($xml->children() as $items) {
	if ($items['id'] == "3") {

	}
    echo $items->InventoryName . ", ";
    echo $items->Identification->Manufacturer . ", ";
    echo $items->Identification->Model . "<br>";
}


?>