<!-- SIDEBAR browse -->
<h3>Browse the Colexification Networks</h3>
<br>
<br>
<font color="red">SIDE UNDER RECONSTRUCTION</font> 
<style>
#visualization {
  width: 800px;
  position: relative;
  height: 800px;
  background-color: white;
  border: 3px dotted gray;
  }

#info {
  background-color: white;
	position: absolute;
	font-family: Arial,Verdana,Helvetica,sans-serif;
	font-size: 9pt;
	left: 0px;
	top: 10px;
  width: 300px;
  display: table-cell;
  //vertical-align: top;
}
#info.hidden {
	display: none;
}
#vis {
	position: absolute;
	left: 10px;
  top: 0px;
  //display: table-cell;
  //vertical-align: top;
}
label {
	font-size: 10pt;
	margin-left: 12px;
}
tr:nth-child(even) {background: #DDD}
tr:nth-child(odd) {background: #FFF}
table { counter-reset: line-number; }
td:first-child:before {
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

<!-- Pieces of Thomas' code -->
<script type="text/javascript" src="js/d3/d3.v2.js"></script>
<div id="control">
  
  <label>Line opacity: </label>
	<input id="opacity" type='range' min="0" max="100" value="100">
  
  <br>
  
  <label>Line weights: </label>
	<input id="weight" type='range' min="0" max="10" value="0">
  
  <label>Coloring: </label>
  <select id="coloring">
    <option>Family</option>
    <option>Geolocation</option>
  </select>
  
  <img id="WorldColorScale" class='hidden' src="img/ColorScaleWorld.png" width="300">
</div>
<br><br>
<div id="visualization">
      <div id="vis"></div>
      <div id="info" class="hidden"></div>

<?php
if(isset($_GET['key']))
{
  echo '<script type="text/javascript">var filename = "'.$_GET['key'].'.json";</script>';
  echo '<font color="red">OK so far</font>';
}
?>
<script src="js/visualize.js" type="text/javascript"></script>

<div id="test" onclick="init(filename);">TEST</div>

</div>
