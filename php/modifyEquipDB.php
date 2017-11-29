<?php
// ini_set('display_errors', 1);
// error_reporting(E_ALL);
header("Cache-Control: no-cache, no-store, must-revalidate"); // HTTP 1.1.
header("Pragma: no-cache"); // HTTP 1.0.
header("Expires: 0"); // Proxies.
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
		$item->Identification->Model = $model;
		$item->Quantity->Total = $total;
		$item->Quantity->InService = $service;
		$item->Quantity->UnderRepair = $repair;

		$locs = $item->Locations->xpath("Location");
		foreach($locs as $l) {
			unset($l[0]);
		}
		foreach($rooms as $index=>$room) {
			if (!empty($rooms) and !empty($stores[$index])) {
				$loc = $item->Locations->addChild("Location");
				$loc->addChild("Room", $room);
				$loc->addChild("Storage", $stores[$index]);
			}
		}
		break;
	}
}

file_put_contents("/var/www/html/data/equipmentDB.xml", $xml->asXML());

?>