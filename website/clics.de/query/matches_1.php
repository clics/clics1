<br>
<div class="main_table_small">
<table class="match_table" align="left">
    <tr>
	<td colspan=2 align=center>
	    <b>Matches for <?php echo $glossA.'('.$numA.')';?> and <?php echo $glossB.'('.$numB.')';?>:</b>
	</td>
    </tr> 
    <tr><td><b>Number of Languages:</b></td><td><?php echo $languages;?></td></tr>
    <tr><td><b>Number of Language Families:</b></td><td><?php echo $families;?></td></tr>
    <form action="direct.php" method="post">
    <tr>
	<td colspan="2" class="submit_button"> 
	    <input type="submit" value="Forms" class="query_ok"/>
	    <input type="hidden" name="forms" value="<?php echo $forms; ?>" />
	    <input type="hidden" name="glossA" value="<?php echo $glossA; ?>" />
	    <input type="hidden" name="glossB" value="<?php echo $glossB; ?>" />
	</td>
    </tr>
</table></div>
