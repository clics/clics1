<table class="query_table" align="left">
  <form action="browse.php" method="get">
  <tr>
	  <td>
	    <b>Concept:</b>&nbsp;
	  </td>
    <td>
      <input type="text" style="width:350px;" name="gloss" id="gloss" />
    </td>
    <td>
      <b>View:</b>&nbsp;
      <select class="submit_button" id="view" name="view" style="display:inline;">
        <option value="community">Community</option>
        <option value="part">Subgraph</option>
      </select>
      <div class="popup">
        <span class="info">?</span>
        <div class="hidden_info">
          Select between two different view modes:
          <br>
          <ul>
            <li>
              <b>Community:</b> Show the community into which the concept was clustered, using automatic approaches to community detection.
            </li>
            <li>
              <b>Subgraph:</b> Select a subgraph of the full CLiCs network containing the strongest links of the concept.
            </li>
          </ul>
        </div>
      </div>

    </td>
    <td width="10%" class="submit_button">
      <input type="submit" value="OK" class="query_ok"/>
    </td>
  </tr>
  </form>
</table>
<br><br>
