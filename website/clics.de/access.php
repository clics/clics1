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
<body id="home2">


<div id="wrapper2">
<?php
//include('query/query_community.php');
?>
<!--</div>-->
<?php
  if(isset($_POST['gloss']) or isset($_GET['gloss']) or isset($_POST['community']) or isset($_GET['community']))
  {
?>
<style>
<?php 
  include("css/visu2.css");
?>
</style>


<!--<div class="content_wrapper">-->
<?php
  include('query/comms2.php');
?>

<form id="svgform" method="post" action="export.php">
 <input type="hidden" id="data" name="data" value="">
</form>
</div>
<?php 
  if($result['size'] > 1)
  {
?>
<div id="content_large_down2" style="float:left;margin-left:30px;">
<br>
<table id="control2" class="query_table" style="background-color:lightgray">
  <tr>
    <th>
      <label>Line opacity: </label>
    </th>
    <td>
      <input id="opacity" type='range' min="0" max="100" value="100">  
    </td>
    <th>
      <label>Line weights: </label>
    <th>
    </td>
	    <input id="weight" type='range' min="0" max="10" value="0">
    </td>
    <th>
      <label>Coloring: </label>
    </th>
    <td>
      <select class="submit_button" id="coloring">
        <option>Family</option>
        <option>Geolocation</option>
      </select>
    </td>
  </tr>
</table>
<!-- Pieces of Thomas' code -->
<script type="text/javascript" src="js/d3/d3.v3.js"></script>
<script type="text/javascript" src="js/d3/topojson.js"></script>
<script type="text/javascript" src="js/mousetrap.js"></script>
<div id="visualization">
      <div id="vis"></div>
      <div id="info" class="hidden"></div>
      <div id="map" style="border: thin solid #ccc;"></div>
      <!--<img id="WorldColorScale" class='hidden' src="pics/ColorScaleWorld.png" width="230">-->
<script src="js/visualize.js" type="text/javascript"></script>

<!--<div id="test" onclick="init(filename);">TEST</div>-->

</div></div>
<script type="text/javascript">
    Mousetrap.bind('ctrl+e', function()
    {
	// Get the d3js SVG element
	var tmp = document.getElementById("vis");
	var svg = tmp.getElementsByTagName("svg")[0];
	// Extract the data as SVG text string
	var svg_xml = (new XMLSerializer).serializeToString(svg);

	// Submit the <FORM> to the server.
	// The result will be an attachment file to download.
	var form = document.getElementById("svgform");
	form['data'].value = svg_xml ;
	form.submit();
}

    );
</script>
<br>
<?php
  }
  }
  else
  {
?>
</div>
<?php
  }
?>

 </div>
</div><!-- end wrapper-->
</body>
</html>
