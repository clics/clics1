header = """
<html>
<head>
<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
<script type="text/javascript" src="jquery.tablesorter.js"></script> 

<script>
        $(document).ready(function() 
            { 
                $("#myTable").tablesorter(); 
            } 
        ); 
</script>

<style>
/* tables */
table.tablesorter {
    font-family:arial;
    margin:10px 0pt 15px;
    font-size: 10pt;
    width: 100%;
    text-align: left;
}
table.tablesorter thead tr th, table.tablesorter tfoot tr th {
    background-color: #e6EEEE;
    border: 1px solid #FFF;
    font-size: 10pt;
    padding: 4px;
}
table.tablesorter thead tr .header {
    background-image: url(img/bg.gif);
    background-repeat: no-repeat;
    background-position: center right;
    cursor: pointer;
}
table.tablesorter tbody td {
    color: #4876a2;
    padding: 4px;
    vertical-align: top;
}
table.tablesorter tbody tr:nth-child(odd) {
    background-color: #ccc;
}
table.tablesorter thead tr .headerSortUp {
    background-image: url(img/asc.gif);
}
table.tablesorter thead tr .headerSortDown {
    background-image: url(img/desc.gif);
}
table.tablesorter thead tr .headerSortDown, table.tablesorter thead tr .headerSortUp {
background-color: #4876a2;
color: #fff;
}
</style>
</head>
<body>

<table id='myTable' class='tablesorter tablelisting'>
<thead>
    <tr>
        <th></th>
        <th>IDS key</th>
        <th>Label</th>
        <th>Occurrences</th>
    </tr>
</thead>
<tbody>

"""

# read tsv file
fh = open("../../../output/concepts.tsv").readlines()

data = [d.split('\t') for d in fh[1:]]

with open("concepts.html",'w') as oh:
    oh.write(header)

    for c,d in enumerate(sorted(data,key=lambda x: x[1])):


        oh.write("<tr>\n")
        oh.write("<td style='text-align: right;'>" + str(c+1) + "</td>")
        oh.write("<td>" + d[0] + "</td>")
        oh.write("<td>" + d[1] + "</td>")
        oh.write("<td style='text-align: right;'>" + str(d[2]) + "</td>")
        oh.write("</tr>\n")

    oh.write("</tbody></table></body></html>")



