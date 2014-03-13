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
  $qstring = 'select * from communities where gloss = "'.$_POST['gloss'].'";';
  $query = $conn->query($qstring);
  $result = $query->fetch();
  if($result['size'] == 1){$member = 'node';}
  else{$member = 'nodes';}
  echo '<script type="text/javascript">var filename = "'.$result['path'].'.json";</script>';
  echo '<br>Concept &quot;'.$_POST['gloss'].'&quot; is part of community '.$result['community'].' with the central concept &quot;'.$result['label'].'&quot; and a total of '.$result['size'].' '.$member.'.';
?>
Hover over the edges to check out the forms for each link. Click on the forms to check their sources.
<br>
<?php
}
else if(isset($_GET['community']) or isset($_POST['community']))
{
  if(isset($_POST['community']))
  {
    $_GET['community'] = $_POST['community'];
  }

  $qstring = 'select * from communities where path = "'.$_GET['community'].'";';
  $query = $conn->query($qstring);
  $result = $query->fetch();
  if($result['size'] == 1){$member = 'node';}
  else{$member = 'nodes';}
  echo '<script type="text/javascript">var filename = "'.$result['path'].'.json";</script>';
  echo '<br>Community '.$result['community'].' contains '.$result['size'].' '.$member.'. The central concept is &quot;'.$result['label'].'&quot;.';
?>
Hover over the edges to check out the forms for each link. Click on the forms to check their sources.
<br>
<?php
}
?>

