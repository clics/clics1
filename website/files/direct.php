<!-- SIDEBAR query -->
<h3>Search for direct links between two concepts</h3>

<br>
<?php

/* connect the database */
$dsn = "sqlite:data/clips.sqlite3";
$conn = new PDO ($dsn);

if(isset($_POST['source']) && isset($_POST['target'])){
  
  /* include the header */
  include('query/query_direct.php');

  $query_string = 'select * from links where glossA="'.$_POST['source'].'" and glossB="'.$_POST['target'].'";';
  $query = $conn->query($query_string);
  $results = $query->fetch();
  
  /* check for results, if value greater one, display, else pass */
  if (count($results) > 1)
  {
	  /* glosses */
    $glossA = $results['glossA'];
	  $glossB = $results['glossB'];

	  /* forms */
    $forms = $results['forms'];

    /* families, languages in sqlite3-db */
	  $families = $results['families'];
	  $languages = $results['languages'];

	  /* the gloss ids */
          $numA = $results['numA'];
	  $numB = $results['numB'];

	  /* include next query */
	  include('query/matches_1.php');
  }
  else
  {
      echo "<p align=left><font color=red><b>No results found for your query.</b></font></p>";
  }
}

else if(isset($_POST['forms'])){
  include('query/query_direct.php');
  include('query/matches_2.php');
  
  /* split forms */
  $forms = explode('//',$_POST['forms']);

  /* iterate over forms array */
  foreach($forms as &$form){
        
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
else
{
  include('query/query_direct.php');
}
?>


