<br>
<div class="table_border">
<table class="query_table" align="left">
<tr> 
  <th colspan=6 align=center >
    <?php 
      if(count($forms) > 1){$colex = 'colexifications';}
      else{$colex = 'colexification';}
      echo 'Found '.count($forms).' '.$colex.' for &quot;';
      echo $_POST['glossA']; ?>&quot; and &quot;<?php echo $_POST['glossB']."&quot;."; 
    ?>
    <div class="popup"> <span class="info">?</span>
      <div class="hidden">
        Note that the number of attested colexifications may differ from the number of languages in which the colexifications were attested.
      </div>
    </div>
  </th>
<tr>
 <th>Nr.</th> 
 <th>Language</th>
 <th>ISO</th>
 <th>Family</th>
 <th>Source</th>
 <th>Form</th>
</tr>
