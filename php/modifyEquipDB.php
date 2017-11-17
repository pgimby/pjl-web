<?php
// ini_set('display_errors', 1);
// error_reporting(E_ALL);
$id = $_POST['eq-id'];
$name = $_POST['eq-name'];
$make = $_POST['eq-make'];
$model = $_POST['eq-model'];
$total = $_POST['eq-total'];
$service = $_POST['eq-service'];
$repair = $_POST['eq-repair'];
$rooms = $_POST['eq-room'];
$stores = $_POST['eq-storage'];
$xml=simplexml_load_file("/var/www/html/data/equipmentDB.xml") or die("Error: Cannot create object");


foreach($xml->children() as $item) {
	if ($item['id'] == $id) {
		$item->InventoryName = $name;
		$item->Identification->Manufacturer = $make;
		$items->Identification->Model = $model;

		list($loc) = $item->Locations->xpath("Location");
		unset($loc[0]);
		foreach($rooms as $index=>$room) {
			$loc = $item->Locations->addChild("Location");
			$loc->addChild("Room", $room);
			$loc->addChild("Storage", $stores[$index]);
		}
		break;
	}
}

echo "success";
file_put_contents("/var/www/html/data/equipmentDB.xml", $xml->asXML());

?>