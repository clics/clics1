<?php
if(isset($_POST['data']))
{
  header('Content-Disposition: attachment; filename="clics.svg');
  $data = preg_replace("/\\\/","", $_POST['data']);
  echo $data;
}

