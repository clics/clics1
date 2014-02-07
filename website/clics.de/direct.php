<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>CLiCs</title>

<meta http-equiv="content-type" content="text/html; charset=utf-8">
<meta name="description" content="Cross-Linguistic Colexification">
<meta name="keywords" content="linguistics, historical linguistics,polysemy">
<meta NAME="resource-type" CONTENT="linguistics,historical linguistics">
<meta name="distribution" CONTENT="global">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />

<link rel="icon" href="pics/favicon.png" type="image/png">  
<link rel="stylesheet" href="css/clips.css" type="text/css" media="screen" /> 
<link rel="stylesheet" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css" />
    
<script src="http://code.jquery.com/jquery-latest.js"></script>
<script src="http://code.jquery.com/ui/1.9.2/jquery-ui.js"></script>   
<script src="js/concepts.js"></script>

</head>
<body id="home">


<div id="wrapper">
  <div id="header">
  <a href="http://lingulist.de/clics/"><img id="logo" src="pics/favicon.png" width="60px" alt="logo" title="CLiCs" /></a>
  <div id="mainnav">
    <ul id="nav">
    <li>
      <!--<a href="main.php">Home</a>
      <ul id="home">
	<li><a href="main.php#news1">News1</a></li>
	<li><a href="main.php#news2">News2</a></li>
	<li><a href="main.php#news3">News3</a></li>
      </ul>
    </li>-->
    <li>
      <a href="about.php">About</a>
      <ul id="about">
	<li><a href="about.php">Introduction</a></li>
	<!--<li><a href="sources.php">Sources</a></li>-->
	<li><a href="faq.php">FAQ</a></li>
	<!--<li><a href="contact.php">Contact</a></li>-->
      </ul>
    </li>
    <li>
      <a href="query.php">Query</a>
      <ul id="query">
        <li><a href="direct.php">Direct Links</a></li>
        <li><a href="all.php">All Links</a></li>
      </ul>
    </li>
    <li>
	<a href="download.php">Download</a>
	<!--<ul>
	    <li><a href="courses.php#current">Current</a></li>
	    <li><a href="courses.php#old">Old</a></li>
	</ul>-->
    </li>
  </ul>
 </div><!--end mainnav-->
 </div><!-- end header -->  
 <div id="subnav">
    <h2> <a href="query.php">Query</a></h2>
   <ul>
    <li><a class="active" href="direct.php">Direct Links</a></li>
    <li><a class="inactive" href="all.php">All Links</a></li>
  </ul>

 </div>
 <div id="contentwrapper" class="clearfix">
     <div id="content">    
	 <!-- SIDEBAR query -->
<h3>Search for direct links between two concepts</h3>

<br>
<?php
/* connect the database */
$dsn = "sqlite:data/clips.sqlite3";
$conn = new PDO ($dsn);

/* check for settings */
if(isset($_POST['source']) && isset($_POST['target'])){

    /* include the header */
    include('query/query_direct.php');

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
    include('query/query_direct.php');

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
    include('query/query_direct.php');
}
?>



 </div>
 </div>
 <div id="footer">
 <p>Last updated on Feb. 07, 2014, 08:29 CET</p>
 <p>
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/deed.en_US">Creative Commons Attribution-NonCommercial 3.0 Unported License</a>.</p><br>
<p>
   <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/deed.en_US"><img
		alt="Creative Commons License" style="border-width:0;width:80px;"
		src="http://i.creativecommons.org/l/by-nc/3.0/88x31.png" /></a> </p>
 
 </div><!-- end footer -->

</div><!-- end wrapper-->
</body>
</html>
