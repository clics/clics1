<?php if($result['families'] < 2){
?>
<tr>
  <td>
    <?php echo '<a href="all.php?gloss='.$result['glossB'].'">'.$result['glossB'].'</a>';?>
  </td>
  <td>
    <?php echo '<a href="all.php?key='.$result['numB'].'">'.$result['numB'].'</a>';?>
  </td>
  <td>
    <?php echo $occs[$result['numB']]; ?>
  </td>
  <td>
	  <?php echo $result['families'];?>
  </td>
  <td>
	  <?php echo $result['languages'];?>
  </td>
  <td class="submit_buttonx" style="text-align:left">
    <?php 
      echo '<span class="query_okk" onclick="window.location='."'".'browse.php?gloss='.$result['glossB']."'".';">&nbsp;COM&nbsp;</span> ';
      echo '<span class="query_okk" onclick="window.location='."'".'browse.php?gloss='.$result['glossB']."&view=part'".';">&nbsp;SUB&nbsp;</span>';
      //echo '<form action="browse.php?gloss='.$result['glossB'].'" method="post">';
      //echo '<input style="display:;color:red;" class="query_okkk" type="submit" value="COMM"/>'; //.$result['community'].'"/>';
      //echo '</form>';
      //echo '<form action="browse.php?gloss='.$result['glossB'].'&view=part" method="post">';
      //echo '<input style="display:table-cell;" class="query_okkk" type="submit" value="PART"/>'; //.$result['community'].'"/>';
      //echo '</form>';
    ?>   
  </td>
<?php 
}
else{
?>
<tr>
  <td style="background-color:lightgray">
    <?php echo '<a href="all.php?gloss='.$result['glossB'].'">'.$result['glossB'].'</a>';?>
  </td>
  <td style="background-color:lightgray">
    <?php echo '<a href="all.php?key='.$result['numB'].'">'.$result['numB'].'</a>';?>
  </td>
  <td style="background-color:lightgray">
    <?php echo $occs[$result['numB']]; ?>
  </td>
  <td style="background-color:lightgray">
	  <?php echo $result['families'];?>
  </td>
  <td style="background-color:lightgray">
	  <?php echo $result['languages'];?>
  </td>
  <td>
    <?php 
      echo '<span class="query_okk" onclick="window.location='."'".'browse.php?gloss='.$result['glossB']."'".';">&nbsp;COM&nbsp;</span> ';
      echo '<span class="query_okk" onclick="window.location='."'".'browse.php?gloss='.$result['glossB']."&view=part'".';">&nbsp;SUB&nbsp;</span>';

      //echo '<form action="browse.php?gloss='.$result['glossB'].'" method="post">';
      //echo '<input class="query_okk" type="submit" value="NETWORK_'.$result['community'].'"/>';
      //echo '</form>';
    ?>
  </td>
<?php 
}
?>
<form action="all.php" method="post">
<td class="submit_button">
	<input type="submit" class="query_ok" value="FORMS"/>
	<input type="hidden" name="forms" value=<?php echo $result['forms'];?> />
	<input type="hidden" name="glossA" value="<?php echo $result['glossA'];?>" />
	<input type="hidden" name="glossB" value="<?php echo $result['glossB'];?>" />
</td>
</form>
</tr>
