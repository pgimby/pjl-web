<?php
/*
  Script to securely relay HTTP POST requests from outside users to the lab machines behind the firewall.
  POST request must include the key-value pair 'machine' to indicate which machine to relay to.
     -> Only machines included in the white list $valid_machines are allowed as relay targets.
  Other key-value pairs are forwarded to the specified target machine only if:
     1. The key is included in the white list $valid_keys
     2. The value uses only alphanumeric characters (a-z, A-Z, 0-9 and .)
     3. The string length of the value does not exceed $max_value_len

  EXAMPLE:
  POST request "machine=http://franklin.pjl.ucalgary.ca:4444&userID=myUser&voltage=1"
  relays a POST request "userID=myUser&voltage=1" to machine franklin.pjl.ucalgary.ca on port 4444.

  NOTE:
  Cross-Origin Resource Sharing (CORS) must be allowed if the HTML page accessing the data
  is on a different computer than this page.
  CORS is very useful for testing, but could be disabled for production code by setting
  $useCORS = False;

  FUTURE WORK: define valid_machines as a range of ip addresses from .20 to .160

  version 1.5, Modified Mar 5, 2021
*/

// SETTINGS:
$valid_machines = array(
    'http://asgard.pjl.ucalgary.ca:4444', //20
    'http://baldur.pjl.ucalgary.ca:4444', //21
    'http://bifrost.pjl.ucalgary.ca:4444', //22
    'http://branstock.pjl.ucalgary.ca:4444', //23
    'http://hugin.pjl.ucalgary.ca:4444', //28
    'http://nagifar.pjl.ucalgary.ca:4444', //30
    'http://tyr.pjl.ucalgary.ca:4444', //32
    'http://sigyn.pjl.ucalgary.ca:4444', //33
    'http://ymir.pjl.ucalgary.ca:4444', //34
    'http://embla.pjl.ucalgary.ca:4444', //35
    'http://thor.pjl.ucalgary.ca:4444', //39
    'http://loki.pjl.ucalgary.ca:4444', //40
    'http://midgard.pjl.ucalgary.ca:4444', //42
    'http://skuld.pjl.ucalgary.ca:4444', //48
    'http://creygan.pjl.ucalgary.ca:4444', //52
    'http://cromlaf.pjl.ucalgary.ca:4444', //53
    'http://gryfin.pjl.ucalgary.ca:4444', //54
    'http://nerthus.pjl.ucalgary.ca:4444', //55
    'http://njord.pjl.ucalgary.ca:4444', //56
    'http://alfheim.pjl.ucalgary.ca:4444', //57
    'http://frenja.pjl.ucalgary.ca:4444', //60
    'http://ingvar.pjl.ucalgary.ca:4444', //61
    'http://jolgeir.pjl.ucalgary.ca:4444', //62
    'http://bolturon.pjl.ucalgary.ca:4444', //63
    'http://carat.pjl.ucalgary.ca:4444', //67    
    'http://barrel.pjl.ucalgary.ca:4444', //68
    'http://newton.pjl.ucalgary.ca:4444', //69
    'http://franklin.pjl.ucalgary.ca:4444', //70
    'http://knot.pjl.ucalgary.ca:4444', //71
    'http://talent.pjl.ucalgary.ca:4444', //72
    'http://torr.pjl.ucalgary.ca:4444', //73
    'http://mole.pjl.ucalgary.ca:4444', //74
    'http://lumen.pjl.ucalgary.ca:4444',  //76
    'http://decisecond.pjl.ucalgary.ca:4444',  //79
    'http://centisecond.pjl.ucalgary.ca:4444',  //80
    'http://millisecond.pjl.ucalgary.ca:4444',  //81
    'http://microsecond.pjl.ucalgary.ca:4444',  //82
    'http://nanosecond.pjl.ucalgary.ca:4444',  //83
    'http://picosecond.pjl.ucalgary.ca:4444',  //84
    'http://femtosecond.pjl.ucalgary.ca:4444',  //85
    'http://attosecond.pjl.ucalgary.ca:4444',  //86
    'http://scruple.pjl.ucalgary.ca:4444' //155
);  // Only these machines/ports are allowed as targets
$valid_keys = array("userID","action","p1","p2",
                    "p3","p4","p5","p6");  // only these keys will be passed on to the lab computer
$max_value_len = 128;           // maximum # of characters allowed in a value
$pattern =  '/^[a-z0-9.]+$/i';  // Only values fitting this pattern (alphanumeric chars) are allowed
$useCORS = True;
/////////////////

// Cross-Origin Resource Sharing (CORS) header
if ($useCORS)
  header("Access-Control-Allow-Origin: *");

// Only respond to POST requests
if ($_SERVER["REQUEST_METHOD"] != "POST"){
  echo "Invalid machine specified.";
  return;
}

// Extract machine
if(isset($_POST['machine'])){
    $lab_URL = $_POST['machine'];
	// machine must be in the valid_machines white-list
    if (!in_array($lab_URL,$valid_machines)){
        echo "IBnvalid machine specified.";
        return;
    }
} else {
    echo "No machine specified.";
    return;
}

// Extract key-value pairs that match the keys allowed in the valid-keys whitelist
$data = array();
$keys_found = 0;
for($i = 0; $i < count($valid_keys); $i++) {
  if(isset($_POST[$valid_keys[$i]])) {
      $data[$valid_keys[$i]]=$_POST[$valid_keys[$i]];
      // Only allow alphanumeric characters in the value
      if (preg_match($pattern, $data[$valid_keys[$i]]) != 1){
          echo "Only alphanumeric characters allowed in values.";
          return;
      }
      // Value must be less than $max_value_len
      if (strlen($data[$valid_keys[$i]]) > $max_value_len){
          echo "Value is too long.";
          return;
      }
      $keys_found++;
  }
}
if ($keys_found == 0){
    echo "No valid keys.";
    return;
}

// Require a userID
//if(! isset($data['userID'])){
//    echo "No userID specified.";
//    return;
//}


// Prepare POST request for lab computer
$options = array('http' => array(
               'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
               'method'  => 'POST',
               'content' => http_build_query($data)));

// Send POST request to lab computer
$context  = stream_context_create($options);
$result = file_get_contents($lab_URL, false, $context);

// Return result
if ($result === FALSE) {
  echo "Data POST failed. Request was not forwarded to the lab computer.<br />\n";
  echo "Lab computer name: ";
  echo $lab_URL;
} else {
    echo $result;
}
?>
