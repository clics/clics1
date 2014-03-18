//############### GLOBAL VARIABLES ##################
// store the community number
//var select = document.getElementById("selectNumber");  
var opacity = 100;
var coloring = "Family";


// load data about words for each edge
var linkByWords = {};
d3.json('data/words.json',function(words){
    words.forEach(function(a){
        linkByWords[a.key] = a.words;
    });
});

// load language data 
var langByInfo = {};
d3.json('data/langsGeo.json',function(langs){
    langs.forEach(function(a){
        langByInfo[a.key] = [a.name,a.variety,a.iso,a.url,a.family,a.lon,a.lat];
    });
});

//################ INIT function #####################
//function init(filename,coloring){
  
  /* debug */
  //document.getElementById("test").innerHTML = filename;

	// the default coloring is family
   	coloring = typeof coloring !== 'undefined' ? coloring : 'Family';

	// open community file
	d3.json('data/communities/' + filename,function(data){
	//d3.json('../../communities/cluster_10_edge.json',function(data){

	// dictionary to convert IDs (node names) to numbers
	nodesById = {};
	for(var i=0; i < data.nodes.length; i++){
		nodesById[data.nodes[i].id] = i;
	};
    
    // store all weights and nodes by links
    var weights = [];
    var nodeByLink = {};
    for(var i=0; i < data.adjacency.length; i++){
		for (var j=0; j < data.adjacency[i].length; j++){
			weights.push(data.adjacency[i][j].weight);
			if(nodeByLink[i]){
				nodeByLink[i].push(nodesById[data.adjacency[i][j].id]);
			}
			else{
				nodeByLink[i] = [nodesById[data.adjacency[i][j].id]];
			}
		}
    }
    
    // weight scale from 0...max(weights) to 0...1
    var scale = d3.scale.linear()
    .domain([0,d3.max(weights)])
    .range([0,1]);
    
    // longitudinal scale
    var longsScale = d3.scale.linear()
   	.domain([-180,180])
   	.range([0,1])
   	;
   	
   	// latitudinal scale
   	var latsScale = d3.scale.linear()
   	.domain([-90,90])
   	.range([0,1])
   	;
   	
   	// l*a*b* scale
   	var labScale = d3.scale.linear()
   		.domain([-1,1])
   		.range([-128,127]);
   	;
    
    // 
    var lscale = d3.scale.linear()
    .domain([0,d3.max(weights)])
    .range([1,100]);
    
    // color scale for all families (TODO: get better representation; there are too many families)
    var famscale = d3.scale.category20c();
    
    // store node and link information for the force directed graph
    var nodes = [];
    var labelAnchors = [];
    var labelAnchorLinks = [];
    var links = [];
    
    for(var i=0;i < data.nodes.length; i++){
        var node = {
            label : data.nodes[i].id,
            out_edge : data.nodes[i].out_edge
        };
        nodes.push(node);
        labelAnchors.push({
            node : node
        });
        labelAnchors.push({
            node : node
        });
    };
    
    // the actual nodes
    for(var i=0; i<data.adjacency.length; i++){
		for(var j=0; j<data.adjacency[i].length; j++){
			links.push({
				source : nodesById[data.adjacency[i][j].id],
				target : i,
				weight : scale(data.adjacency[i][j].weight),
        edge_width : data.adjacency[i][j].edge_width, // addon JML
			});
		}
    };
    
    // the label nodes with weight 1 connected to the actual nodes
    for(var i=0; i< nodes.length; i++){
        labelAnchorLinks.push({
            source : i * 2,
            target : i * 2 + 1,
            weight : 1
        });
    };
	
	// make force directed graph layout draggable
    var node_drag = d3.behavior.drag()
        .on("dragstart", dragstart)
        .on("drag", dragmove)
        .on("dragend", dragend);

    function dragstart(d, i) {
        force.stop() // stops the force auto positioning before you start dragging
    }

    function dragmove(d, i) {
        d.px += d3.event.dx;
        d.py += d3.event.dy;
        d.x += d3.event.dx;
        d.y += d3.event.dy; 
        tick(); // this is the key to make it work together with updating both px,py,x,y on d !
    }

    function dragend(d, i) {
        d.fixed = true; // of course set the node to fixed so the force doesn't include the 
        				// node in its auto positioning stuff
        tick();
        force.resume();
    }
    
    // enable panning and zooming
    function redraw() {
      vis.attr("transform",
          "translate(" + d3.event.translate + ")"
          + " scale(" + d3.event.scale + ")");
    }
    
	// plot the graph on an SVG
	var w = 600, h = 400, pad = 50;
	var labelDistance = 0;

	var vis = d3.select("#vis")
		.append("svg:svg")
		.attr("width", w)
		.attr("height", h)
		.on('click',function(){
			d3.select('#info').classed('hidden',true);
			d3.selectAll('.link').style('stroke','#CCC');
		})
		.append('svg:g')
		  .call(d3.behavior.zoom().on("zoom", redraw))
		.append('svg:g');
		;
           
	// force layout for actual nodes
	var force = d3.layout.force()
		.size([w-pad, h-pad])
		.nodes(nodes)
		.links(links)
		.gravity(1)
		.linkDistance(50)
		.charge(-3000)
		.linkStrength(function(x) {
			return x.weight * 10
		})
		;

	force.start();
	
	// force layout for node labels
	var force2 = d3.layout.force()
		.nodes(labelAnchors)
		.links(labelAnchorLinks)
		.gravity(0)
		.linkDistance(0)
		.linkStrength(8)
		.charge(-100)
		.size([w-pad, h-pad])
		;
		
	force2.start();
		
	// link behavior
	var link = vis.selectAll("line.link")
		.data(links).enter()
		.append("svg:line")
		.attr("class", function(d,i){
			var weight = parseInt(d.weight * 10);
			var weightOutput = [];
			for(var i=0;i<=weight;i++){
				weightOutput.push('weight_' + i);
			}
			
			return "link link_" + d.source.index 
			+ "-" + d.target.index + ' link_' 
			+ d.target.index + "-" + d.source.index
			+ " " + weightOutput.join(" ") + " " + weight;
			
		})
		.style("stroke", "#CCC")
		.style('stroke-width',function(d){
      return d.edge_width
		})
		.style('cursor','pointer')
		.on('mouseover',function(d,i){
			//console.log(d);
			d3.selectAll('.link').style('stroke','#CCC').style('stroke-opacity',opacity/100);
			d3.select(this).style('stroke','OliveDrab').style('stroke-opacity',1);
			d3.select("#info")
			.html(function(){
				var wordlist = [];
				if(linkByWords[d.source.label + "___" + d.target.label]){
					wordlist = linkByWords[d.source.label + "___" + d.target.label];
				}
				else{
					wordlist = linkByWords[d.target.label + "___" + d.source.label]
				}
				
				var infolist = [];
				wordlist.forEach(function(b){
				   var parts = b.split(":")
				   //console.log(parts[0]);
				   var lg = langByInfo[parts[0]];
				   var fam = lg[4].split(',')[0];
				   infolist.push([fam,parts[1],lg[2],lg[3],lg[0],lg[5],lg[6]]);
				});
				
				infolist.sort(function(a,b){
					if (a[0] > b[0]){
						return 1;
					}
					if (a[0] < b[0]){
						return -1;
					}
					else{
						if(a[4] > b[4]){
							return 1;
						}
						else{
							return -1;
						}
					}
				});
				
				var infolistoutput = [];
				infolist.forEach(function(c){
					var backColor = famscale(c[0]);
					if(coloring == "Geolocation"){
						lab = cl2pix(longsScale(c[5]),latsScale(c[6]));
						//console.log(lab);
						//console.log(c[5],c[6]);
						var col = d3.lab(lab[0]*100,labScale(lab[1]),labScale(lab[2]));
						//console.log(col);
						backColor = col;
					}
					// taken from http://www.jasondavies.com/coffee-wheel/
					var fontcolor = brightness(d3.rgb(backColor)) < 125 ? "#eee" : "#000";
					
					infolistoutput.push("<td valign=\"top\">" // style=\"background-color:" 
					+ c[4] +  "</td><td style=\"background-color:"+backColor+"; color:" + fontcolor + ";\">" + c[0] + "</td>"
           + "<td class=\"infotable\" valign=\"top\"><a target=\"_blank\" href=\"" + c[3] 
           + "\">" + c[1] + "</a>") + "</td>";
				});
        if(wordlist.length == 1)
        {
          var link_label = 'link';
        }
        else
        {
          var link_label = 'links';
        }
				
				return "<b>" + wordlist.length + " "+ link_label + " for &quot;"+ 
					d.source.label + "&quot; and &quot;" 
					+ d.target.label + 
					"&quot;.</b><br><table class=\"infotable\"><tr><th>Language</th><th>Family</th>" + 
					"<th>Form</th></tr><tr>" + 
					infolistoutput.join('</tr><tr>') + "</tr></table>";
			});
			d3.select('#info').classed('hidden',false)
		})
		.on('mouseout',function(d,i){
			//d3.select(this).style('stroke','#CCC');
		})
		;

		
	// node behavior
	var node = vis.selectAll("g.node")
		.data(force.nodes())
		.enter()
		.append("svg:g")
		.attr("class", "node")
		;
	
	node.append("svg:circle")
		.attr("r", 5)
		.style("fill", "#555")
		.style("stroke", "#FFF")
		.style("stroke-width", 3)
		.style('cursor','move')
		.on('dragend',function(d){
			d.fixed = true;
		})
		;
	node.call(node_drag);

	var anchorLink = vis.selectAll("line.anchorLink")
		.data(labelAnchorLinks)
		//.enter().append("svg:line").attr("class", "anchorLink").style("stroke", "#999")
		;

	var anchorNode = vis.selectAll("g.anchorNode")
		.data(force2.nodes())
		.enter()
		.append("svg:g")
		.attr("class", function(d,i){
			return "anchorNode_" + d.node.index;
		})
		;
		
	anchorNode.append("svg:circle")
		.attr("r", 0)
		.style("fill", "#FFF")
		;
		
	anchorNode.append("svg:text")
		.attr('class',function(d,i){
			return "aNode aNode_" + d.node.index;
		})
		.text(function(d, i) {
			return i % 2 == 0 ? "" : d.node.label;
		})
		.style("fill", "#555")
		.style("font-weight",function(d,i){
			//console.log(d);
			// make concepts with outer edges bold
			if(d.node.out_edge.length > 0){
				return "bold";
			}
			else{
				return "normal";
			}
			
			//return "underline";
		})
		.style("font-family", "Arial")
		.style("font-size", 12)
		.style('cursor',function(d,i){
			d.node.out_edge.length > 0 ? cursorvalue = "pointer" : cursorvalue = "arrow";
			return cursorvalue;
		})
		.on('mouseover',function(d,i){
			//console.log(d);

			d3.selectAll('.link').style('stroke','#CCC').style('stroke-opacity',opacity/100);
			d3.select(this).style('fill','DarkBlue').style('stroke-opacity',1);
			nodeByLink[d.node.index].forEach(function(a){
				//console.log("effects ",a);
				d3.selectAll('.aNode_' + a)
					.style('fill','FireBrick').style('stroke-opacity',1);
				d3.selectAll('.link_' + a + "-" + d.node.index)
					.style('stroke','OliveDrab').style('stroke-opacity',1);
			});
			
			if(d.node.out_edge.length > 0){
			
				d3.select("#info")
					.html(function(){
						console.log(d);
						var outstring = '<b>Links to other communities from \'' +  d.node.label + '\'</b>:<br>';
						for(var j=0;j<d.node.out_edge.length;j++){
							outstring += "&bull; <a href='?community=" + d.node.out_edge[j][0] + "'>" 
							+ d.node.out_edge[j][0] + '</a> (' + d.node.out_edge[j][1] + ')<br>';
						};
						return outstring;
					});
				d3.select('#info').classed('hidden',false);
			}
		})
		.on('mouseout',function(d,i){
			d3.selectAll('.aNode')
				.style('fill','#555')
				.style('stroke-opacity',opacity/100)
			;
			d3.selectAll('.link')
				.style('stroke','#CCC')
			.style('stroke-opacity',opacity/100)
			;
		})
		.append('title')
		.text(function(d,i){
			var outstring = '';
			for(var j=0;j<d.node.out_edge.length;j++){
				outstring += d.node.out_edge[j][0] + '\n';
			};
			return outstring;
		})
		;

	var updateLink = function() {
		this.attr("x1", function(d) {
			return d.source.x;
		}).attr("y1", function(d) {
			return d.source.y;
		}).attr("x2", function(d) {
			return d.target.x;
		}).attr("y2", function(d) {
			return d.target.y;
		});
	};

	var updateNode = function() {
		this.attr("transform", function(d) {
			return "translate(" + d.x + "," + d.y + ")";
		})
		;
	}

	function tick() {
	
		force2.start();
		node.call(updateNode);

		anchorNode.each(function(d, i) {
			if(i % 2 == 0) {
				d.x = d.node.x;
				d.y = d.node.y;
			} else {
				//var b = this.childNodes[1].getBBox();
				// changed from above due to Firefox bug 
				// (https://bugzilla.mozilla.org/show_bug.cgi?id=612118)
				var b = this.childNodes[1].getBoundingClientRect();	
				var diffX = d.x - d.node.x;
				var diffY = d.y - d.node.y;
		
				var dist = Math.sqrt(diffX * diffX + diffY * diffY);
		
				var shiftX = b.width * (diffX - dist) / (dist * 2);
				shiftX = Math.max(-b.width, Math.min(0, shiftX));
				var shiftY = 5;
				this.childNodes[1].setAttribute("transform", 
					"translate(" + shiftX + "," + shiftY + ")")
				;
			}
		});
		anchorNode.call(updateNode);
		link.call(updateLink);
		anchorLink.call(updateLink);
	};
				
	// taken from http://davidad.net/colorviz/
	// convert into lab color
	function cl2pix(c,l){
		var TAU = 6.283185307179586476925287 // also known as "two pi"
		var L = l*0.61 + 0.09; // L of L*a*b*
		var angle = TAU/6.0 - c*TAU;   	
		var r = l*0.311 + 0.125 //~chroma
		var a = Math.sin(angle)*r;
		var b = Math.cos(angle)*r;
		return [L,a,b];
	};
	
	// taken from http://www.jasondavies.com/coffee-wheel/
	function brightness(rgb) {
  	return rgb.r * .299 + rgb.g * .587 + rgb.b * .114;
	}
	
	force.on('tick',tick);
	});
	      
//};
      
//############### listener to community selection ###############
//d3.select('#selectNumber').on('change',function(){
//	filename = this.value;
//	d3.select('svg').remove();
//	d3.select('#info').classed('hidden',true);
//	init(filename,coloring);
//})

//############### listener to coloring selection ###############
d3.select('#coloring').on('change',function(){
	coloring = this.value;
	d3.select('#info').classed('hidden',true);
	var colorBool = coloring == 'Family';
	d3.select('#WorldColorScale').classed('hidden',colorBool);
	
})

//############### OPACITY slider ############### 
d3.select("#opacity").on("change", function() {
	opacity = this.value; 
	d3.selectAll('.link') 
	.style('stroke-opacity',function(){ 
		return opacity/100;
	}); 
});

//############### OPACITY slider ############### 
d3.select("#weight").on("change", function() {
	lineweight = parseInt(this.value); 
	d3.selectAll(".link").classed('hidden',true);

	d3.selectAll('.weight_' + lineweight)
	.classed('hidden',false);
});


