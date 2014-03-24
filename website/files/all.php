<!-- SIDEBAR query -->
<h3>Search for all links of a given concept:</h3>
<br>
<?php
/* get the occurrences in json */
$occs = json_decode(file_get_contents('data/occurrences.json'),true);

/* connect the database */
$dsn = "sqlite:data/clips.sqlite3";
$conn = new PDO ($dsn);

if(isset($_POST['forms']))
{
  include('query/query_all.php');


  /* split forms */
  $forms = explode('//',$_POST['forms']);
  $count = 1;
  include('query/matches_2.php');
  
  /* iterate over forms array */
  foreach($forms as &$form)
  {      
	  /* get form and language ID */
    $tmp = explode(':',$form);
    $lid = $tmp[0];
    $form = substr($tmp[1],1,-1);

    // Now that we got form and language id, we take the data for all languages from clips.slqite3
    $query_string = 'select * from langs where id="'.$lid.'";';
    $query = $conn->query($query_string);
    $results = $query->fetch();
    $classification = explode(',',$results['classification']);
    $classification = array_shift($classification);
    $iso = explode('_',$results['iso']);
	  $iso = array_shift($iso);
	
	  /* include specific matches */
	  include('query/matches_3.php');
  }
  echo '</table></div>';
}
else if(isset($_POST['gloss']) or isset($_GET['gloss']) or isset($_GET['key']))
{
  include('query/query_all.php');
  
  if(isset($_GET['gloss']))
  {
    $_POST['gloss'] = $_GET['gloss'];
  }
  if(isset($_GET['key']))
  {
    $query_string = 'select * from links where numA == "'.$_GET['key'].'" order by families desc;';
  }
  else
  {
    /* make the query string */
    $query_string = 'select * from links where glossA == "'.$_POST['gloss'].'" order by families desc;';
  }
  $query = $conn->query($query_string);
  
  /* store the results in array $results*/
  $results = array();
  $next_result = $query->fetch();

  /* add the community to the result */
  $query_string2 = 'select community,label from communities where id = "'.$next_result['numB'].'";';
  $query2 = $conn->query($query_string2);
  $result2 = $query2->fetch();
  
  $next_result['community'] = $result2['community'];
  $next_result['community_label'] = $result2['label'];

  $check = $next_result;
  while($check['community'] != ''){
	  $results[] = $next_result;
    $next_result = $query->fetch();

    $query_string2 = 'select community,label from communities where id = "'.$next_result['numB'].'";';
    $query2 = $conn->query($query_string2);
    $result2 = $query2->fetch();
    
    $next_result['community'] = $result2['community'];
    $next_result['community_label'] = $result2['label'];
    
    $check = $next_result;
  }

  /* check whether there are enough results */
  if(count($results) > 1)
  {
	
	  /* include match 4*/
	  include('query/matches_4.php');

	  /* iterate over results array*/
    foreach($results as &$result)
    {
	    /* include match_3*/
	    include('query/matches_5.php');
	  }
	  echo '</table></div>';
  }
  else
  {
	  echo '<p align="left"><font color=red><b>No results found for your query.</b></font></p>';
  }
}
else
{
  include('query/query_all.php');
}
?>

