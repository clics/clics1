<!-- SIDEBAR query -->
<h3>Search for all links of a given concept:</h3>
<br>
<?php
/* connect the database */
$dsn = "sqlite:data/clips.sqlite3";
$conn = new PDO ($dsn);

/* check for settings */
if(isset($_POST['source']) && isset($_POST['target'])){

    /* include the header */
    include('query/query_all.php');

    /* make the query */
    $query_string = 'select * from links where glossA="'.$_POST['source'].'" and glossB="'.$_POST['target'].'";';
    $query = $conn->query($query_string);
    $results = $query->fetch();
    
    /* check for results, if value greater one, display, else pass */
    if (count($results) > 1){

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
    else{
        echo "<p align=center><font color=red><b>No results found for your query.</b></font></p>";
    }
}
else if(isset($_POST['forms'])){
    include('query/query_all.php');
    include('query/matches_2.php');
    /* split forms */
    $forms = explode('//',$_POST['forms']);

    /* iterate over forms array */
    foreach($forms as &$form){
        
	/* get form and language ID */
        $tmp = explode(':',$form);
        $lid = $tmp[0];
        $form = $tmp[1];

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
else if(isset($_POST['concept'])){
    include('query/query_all.php');

    /* make the query string */
    $query_string = 'select * from links where glossA == "'.$_POST['concept'].'" order by families desc;';
    $query = $conn->query($query_string);
    
    /* store the results in array $results*/
    $results = array();
    $next_result = $query->fetch();
    $check = $next_result;
    while($check['glossA'] != ''){
	$results[] = $next_result;
	$next_result = $query->fetch();
	$check = $next_result;
    }

    /* check whether there are enough results */
    if(count($results) > 1){
	
	/* include match 4*/
	include('query/matches_4.php');

	/* iterate over results array*/
	foreach($results as &$result){

	    /* include match_3*/
	    include('query/matches_5.php');
	}
	echo '</table></div>';
    }
    else{
	echo "<p align=center><font color=red><b>No results found for your query.</b></font></p>";
    }
}
else{
    include('query/query_all.php');
}
?>

