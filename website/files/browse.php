<!-- SIDEBAR browse -->
<h3>Browse the Colexification Networks</h3>
<br>
<br>
<?php 
  if(isset($_POST['gloss']) or isset($_GET['key']))
  {
?>
<style>
#visualization {
  width: 100%; //800px;
  position: relative;
  height: 550px;
  background-color: white;
  //border: 3px dotted gray;
  overflow-right: hidden;
  }

#info {
  background-color: white;
	position: absolute;
	//font-family: Arial,Verdana,Helvetica,sans-serif;
	font-size: 10pt;
	left: 0px;
	top: 10px;
  width: 325px;
  height: 540px;
  overflow: auto;
  display: table-cell;
  //vertical-align: top;
}
#info.hidden {
	display: none;
}
#vis {
	position: absolute;
	left: 200px;
  top: 0px;
  //display: table-cell;
  //vertical-align: top;
}
label {
	//font-size: 10pt;
  //margin-left: 12px;
  //border: 1px dotted gray;
}


tr:nth-child(even) {background: #DDD}
tr:nth-child(odd) {background: #FFF}
table.infotable { counter-reset: line-number; border: 1px dotted gray;}
table.infotable td:first-child:before {
content: counter(line-number) ".";
counter-increment: line-number;
padding-right: 0.3em; }
.infotable td {
	padding-right: 5px;
}
.hidden {
	display: none;
}
#WorldColorScale {
	position: absolute;
	top: 10px;
	right: 10px;
}
</style>
<?php
  }
?>
<?php
  include('query/query_community.php');
  include('query/communities.php');
?>
<!-- Pieces of Thomas' code -->
<?php
  if(isset($_POST['gloss']) or isset($_GET['key']))
  {
?>
<script type="text/javascript" src="js/d3/d3.v2.js"></script>
<br>
<div style="border: 2px solid #2f95e3;">
<table id="control" class="query_table">
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
<img id="WorldColorScale" class='hidden' src="pics/ColorScaleWorld.png" width="300">

<br>
<div id="visualization">
      <div id="vis"></div>
      <div id="info" class="hidden"></div>

<script src="js/visualize.js" type="text/javascript"></script>

<!--<div id="test" onclick="init(filename);">TEST</div>-->

</div>
</div>
<br>

<?php
  }
?>

