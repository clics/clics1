<?php if($result['families'] < 2){
?>
<tr>
  <td>
    <?php echo '<a href="all.php?concept='.$result['glossB'].'">'.$result['glossB'].'</a>';?>
  </td>
  <td>
    <?php echo '<a href="all.php?key='.$result['numB'].'">'.$result['numB'].'</a>';?>
  </td>
  <td>
	  <?php echo $result['families'];?>
  </td>
  <td>
	  <?php echo $result['languages'];?>
  </td>
  <td>
    <?php echo $result['community'];?>
  </td>
  <td>
    <?php echo '<a href="browse.php?key=cluster_'.$result['community'].'_'.$result['community_label'].'"><em>'.$result['community_label'].'</em></a>';?>
   
  </td>
<?php 
}
else{
?>
<tr>
  <td style="background-color:lightgray">
    <?php echo '<a href="all.php?concept='.$result['glossB'].'">'.$result['glossB'].'</a>';?>
  </td>
  <td style="background-color:lightgray">
    <?php echo '<a href="all.php?key='.$result['numB'].'">'.$result['numB'].'</a>';?>
  </td>
  <td style="background-color:lightgray">
	  <?php echo $result['families'];?>
  </td>
  <td style="background-color:lightgray">
	  <?php echo $result['languages'];?>
  </td>
  <td style="background-color:lightgray">
    <?php echo $result['community'];?>
  </td>
  <td style="background-color:lightgray">
    <?php echo '<a href="browse.php?key=cluster_'.$result['community'].'_'.$result['community_label'].'"><em>'.$result['community_label'].'</em></a>';?>
  </td>
<?php 
}
?>
    <form action="all.php" method="post">
    <td class="submit_button">
	<input type="submit" class="query_ok" value="FORMS"/>
	<input type="hidden" name="forms" value=<?php echo $result['forms'];?> />
	<input type="hidden" name="glossA" value=<?php echo $result['glossA'];?> />
	<input type="hidden" name="glossB" value=<?php echo $result['glossB'];?> />
    </td>
    </form>
</tr>
