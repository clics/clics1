<!-- SIDEBAR NONE -->
<div id="subnav2">
    <h2> <a href="browse.php">Browse</a></h2>
</div>
<div id="content_large_up">
<h3>Browse the Colexification Networks</h3>
<br>
<?php
include('query/query_community.php');
?>
<!--</div>-->
<?php
  if(isset($_POST['gloss']) or isset($_GET['gloss']) or isset($_POST['community']) or isset($_GET['community']))
  {
?>
<style>
<?php 
  include("css/visualize.css");
?>
</style>


<!--<div class="content_wrapper">-->
<?php
  include('query/communities.php');
?>
</div>
<div id="content_large_down">
<br>
<table id="control" class="query_table" style="background-color:lightgray">
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
<script type="text/javascript" src="js/d3/d3.v2.js"></script>
<div id="visualization">
      <div id="vis"></div>
      <div id="info" class="hidden"></div>
      <img id="WorldColorScale" class='hidden' src="pics/ColorScaleWorld.png" width="300">
<script src="js/visualize.js" type="text/javascript"></script>

<!--<div id="test" onclick="init(filename);">TEST</div>-->

</div></div>
<br>
<?php
  }
  else
  {
?>
</div>
<?php
  }
?>
