<?php
// Lab computer URL (eg. http://franklin.pjl.ucalgary.ca:4444 )
$lab_URL = 'http://franklin.pjl.ucalgary.ca:4444';

// If this page is accessed by POST,
// send the post request to the lab computer
if ($_SERVER["REQUEST_METHOD"] == "POST")
{
  if(isset($_POST['voltage']))
  {
    // Get the requested voltage
    $voltage=$_POST['voltage'];

     // Check for non-numeric characters
    $pattern =  '/^[0-9.]+$/';
    if (preg_match($pattern, $voltage) == 1){
      // Prepare POST request for lab computer
      $data = array('voltage' => $voltage);
      $options = array('http' => array(
                       'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                       'method'  => 'POST',
                       'content' => http_build_query($data)));
      // Send POST request to lab computer
      $context  = stream_context_create($options);
      $result = file_get_contents($lab_URL, false, $context);
      if ($result === FALSE) {
        echo "Data POST failed. Request was not forwarded to the lab computer.<br />\n";
        echo "Lab computer name: ";
        echo $lab_URL;
      } else {
        echo $result;
      }
    } else {
      echo "WARNING: non-numeric characters. Request not forwarded to lab computer.<br />\n";
    }
  } else if(isset($_POST['photo']))
  {
    // Prepare POST request for lab computer
    $data = array('photo' => 'y');
    $options = array('http' => array(
                     'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                     'method'  => 'POST',
                     'content' => http_build_query($data)));
    // Send POST request to lab computer
    $context  = stream_context_create($options);
    $result = file_get_contents($lab_URL, false, $context);
    if ($result === FALSE) {
      echo "Data POST failed. Request was not forwarded to the lab computer.<br />\n";
      echo "Lab computer name: ";
      echo $lab_URL;
    } else {
      echo $result;
    }
  }

}

// If this page is accessed by GET,
// send the request to the lab computer
if ($_SERVER["REQUEST_METHOD"] == "GET")
{

  // Prepare GET request for lab computer
  $options = array('http' => array(
                      'method'  => 'GET',
                      'max_redirects' => '0',
                      'ignore_errors' => '1'));

  // Send GET request to lab computer
  $context  = stream_context_create($options);
  $stream = fopen($lab_URL,'r',false,$context);
  //$result = file_get_contents($lab_URL, false, $context);
  //var_dump(stream_get_meta_data($stream));
  $result = stream_get_contents($stream);
  if ($result === FALSE) {
    echo "Data GET request failed. Lab computer is not responding.<br />\n";
    echo "Lab computer name: ";
    echo $lab_URL;
  } else {
    echo $result;
  }
  fclose($stream);
}

?>
