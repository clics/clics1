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
        <th>Language</th>
        <th>ISO</th>
        <th>Family</th>
        <th>Concepts</th>
        <th>URL</th>
    </tr>
</thead>
<tbody>

"""

# read tsv file
fh = open("../../../output/varieties.tsv").readlines()

data = [d.split('\t') for d in fh]

with open("varieties.html",'w') as oh:
    oh.write(header)

    for c,d in enumerate(sorted(data,key=lambda x: x[1])):

        #oh.write("<tr><td>" + "</td><td>".join([d[1],d[2],d[3],d[6],d[7]]) +
        #    "</td></tr>\n")
        oh.write("<tr>\n")
        oh.write("<td style='text-align: right;'>" + str(c+1) + "</td>")
        oh.write("<td>" + d[1] + "</td>")
        oh.write("<td style='min-width: 60px;'>" + d[2] + "</td>")
        oh.write("<td>" + d[3] + "</td>")
        oh.write("<td style='text-align: right;min-width: 100px;'>" + str(d[6]) + "</td>")
        oh.write("<td><a href='" + d[7] + "' target='_blank'>" + d[7] + "</a></td>")
        oh.write("</tr>\n")

    oh.write("</tbody></table></body></html>")



