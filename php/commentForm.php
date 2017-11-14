
<?php
    $email = $_POST['email'];
    $msg = $_POST['message'];
    $from = 'From: PJL Webpage';
    $to = 'pgimby.ucalgary.ca';
    $subject = 'PJL: Contact Form Submission';
    $msg = wordwrap($msg, 256, "\n");
    $body = "E-Mail: $email\n Message:\n $msg";

    if ($_POST['submit']) {
         if (mail($to,$subject,$body)) {
            header('location:/');
            echo "message sending success";
         } else {
            echo "message sending failed";
         }
    }
?>
