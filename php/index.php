<?php

$inp = fopen("php://input");
$outp = fopen("../data/db-test.xml", "w");

while (!feof($inp)) {
    $buffer = fread($inp, 8192);
    fwrite($outp, $buffer);
}

fclose($inp);
fclose($outp);


?>
