<?php
/* connect the database */
$dsn = "sqlite:data/clips.sqlite3";
$conn = new PDO ($dsn);

if(isset($_POST['gloss']) or isset($_GET['gloss']))
{
  if(isset($_GET['gloss']))
  {
    $_POST['gloss'] = $_GET['gloss'];
  }
  if(isset($_GET['view']))
  {
    $_POST['view'] = $_GET['view'];
  }
  else if(isset($_POST['view']) == false)
  {
    $_POST['view'] = 'community';
  }
  if($_POST['view'] == 'part')
  {
    $qstring = 'select * from cuts where gloss = "'.$_POST['gloss'].'";';
    $query = $conn->query($qstring);
    $result = $query->fetch();
    if($result['size'] == 1){$member = 'node';}
    else{$member = 'nodes';}
    if($result['size'] > 1)
    {
      echo '<script type="text/javascript">var filename = "cuts/'.$result['path'].'.json";</script>';
      //echo '<br>Concept &quot;'.$_POST['gloss'].'&quot; is part of a cluster with the central concept &quot;'.$result['label'].'&quot; with a total of '.$result['size'].' '.$member.'. ';
?>
<?php
    }
    else
    {
      echo 'The concept you selected is not available.';
    }
?>
<?php
  }
  else
  {
    $qstring = 'select * from communities where gloss = "'.$_POST['gloss'].'";';
    $query = $conn->query($qstring);
    $result = $query->fetch();
    if($result['size'] == 1){$member = 'node';}
    else{$member = 'nodes';}
    if($result['size'] > 1)
    {
      echo '<script type="text/javascript">var filename = "communities/'.$result['path'].'.json";</script>';
      //echo '<br>Concept &quot;'.$_POST['gloss'].'&quot; is part of community '.$result['community'].' with the central concept &quot;'.$result['label'].'&quot; and a total of '.$result['size'].' '.$member.'. ';
?>
<?php
    }
    else
    {
      echo "The concept you selected is not available.";
    }
  }
?>

<?php
}
else if(isset($_GET['community']) or isset($_POST['community']))
{
  if(isset($_POST['community']))
  {
    $_GET['community'] = $_POST['community'];
  }
  if(strpos($_GET['community'],"network") !== false)
  {
    $path = 'cuts/';
    $qstring = 'select * from cuts where path = "'.$_GET['community'].'";';
    $query = $conn->query($qstring);
    $result = $query->fetch();
    if($result['size'] == 1){$member = 'node';}
    else{$member = 'nodes';}
    echo '<script type="text/javascript">var filename = "'.$path.$result['path'].'.json";</script>';
    //echo '<br>This part of the network contains '.$result['size'].' '.$member.'. The central concept is &quot;'.$result['label'].'&quot;.';
  }
  else
  {
    $path = 'communities/';
    $qstring = 'select * from communities where path = "'.$_GET['community'].'";';
    $query = $conn->query($qstring);
    $result = $query->fetch();
    if($result['size'] == 1){$member = 'node';}
    else{$member = 'nodes';}
    echo '<script type="text/javascript">var filename = "'.$path.$result['path'].'.json";</script>';
    //echo '<br>Community '.$result['community'].' contains '.$result['size'].' '.$member.'. The central concept is &quot;'.$result['label'].'&quot;. ';
  }
?>
<?php
}
?>
