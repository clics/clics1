<?php
if(isset($_POST['data']))
{
  header('Content-Disposition: attachment; filename="clics.svg');
  echo $_POST['data'];
}

