var margin = {top: -5, right: -5, bottom: -5, left: -5};
var width = 1000 - margin.left - margin.right,
height = 600 - margin.top - margin.bottom;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-200)
    .linkDistance(50)
    .size([width + margin.left + margin.right, height + margin.top + margin.bottom]);

var zoom = d3.behavior.zoom()
    .on("zoom", zoomed);

var drag = d3.behavior.drag()
    .origin(function(d) { return d; })
    .on("dragstart", dragstarted)
    .on("drag", dragged)
    .on("dragend", dragended);


 var svg = d3.select("#graph")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.right + ")")
    .call(zoom);

var rect = svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all");

var container = svg.append("g");


$("#form").submit(function(event) {

	d3.json("/" + $("#category").val() + "/" + $("#analysis").val() + "/" + $("#limitResult").val() , function(error, graph) {
		if (error) throw error;

		svg.selectAll("*").remove();

		svg = d3.select("#graph")
		    .attr("width", width + margin.left + margin.right)
		    .attr("height", height + margin.top + margin.bottom)
		    .append("g")
		    .attr("transform", "translate(" + margin.left + "," + margin.right + ")")
		    .call(zoom);

		rect = svg.append("rect")
		    .attr("width", width)
		    .attr("height", height)
		    .style("fill", "none")
		    .style("pointer-events", "all");

		container = svg.append("g");

        
                force
                    .nodes(graph.nodes)
                    .links(graph.links)
                    .start();
                
      
	    
		var link = container.append("g")
                        .attr("class", "links")
                        .selectAll(".link")
			.data(graph.links)
                        .enter().append("line")
			.attr("class", "link")
 
		var node = container.append("g")
                        .attr("class", "nodes")
                        .selectAll(".node")
			.data(graph.nodes)
			.enter().append("g")
			.attr("class", "node")
                        .attr("cx", function(d) { return d.x; })
                        .attr("cy", function(d) { return d.y; })
                        .call(drag);

		node.append("circle").attr("r", 15).
			style("fill", function(d) { return color(d.cluster); })
			.on("click", function(d) {
			if (d3.event.defaultPrevented) return;
				isSelected = d3.select(this).classed("selected");
				d3.select(this).classed("selected", !isSelected);
				$("#node-info tbody").empty();
				$("#node-info tbody").append("<tr><th>Paper Title</th><th>Cluster</th></tr>");
				$("#node-info tbody").append("<tr><td>"+ d.title +"</td><td><a href=\"" +
				"/" + $("#category").val() + "/" + $("#analysis").val() + "/" + $("#limitResult").val() 
				+ "/cluster/"  + d.cluster + "\">" + d.cluster + "</a></td></tr>");
		});
		  
                force.on("tick", function() {
                    link.attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y; })
                        .attr("x2", function(d) { return d.target.x; })
                        .attr("y2", function(d) { return d.target.y; });

                    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
                });
                
                var linkedByIndex = {};
                graph.links.forEach(function(d) {
                    linkedByIndex[d.source.index + "," + d.target.index] = 1;
                });

                function isConnected(a, b) {
                    return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index];
                }

		node.on("mouseover", function(d){
                        
                        node.classed("node-active", function(o) {
                            thisOpacity = isConnected(d, o) ? true : false;
                            this.setAttribute('fill-opacity', thisOpacity);
                            return thisOpacity;
                        });

                        link.classed("link-active", function(o) {
                            return o.source === d || o.target === d ? true : false;
                        });
                        
                        d3.select(this).classed("node-active", true);
                        d3.select(this).select("circle").transition()
                                .duration(750)
                })
		
		.on("mouseout", function(d){
                        
                        node.classed("node-active", false);
                        link.classed("link-active", false);
                    
                        d3.select(this).select("circle").transition()
                                .duration(750)
			d3.selectAll(".selected").classed("selected", false);
                });
});
	event.preventDefault();

});
        function dottype(d) {
          d.x = +d.x;
          d.y = +d.y;
          return d;
        }

        function zoomed() {
          container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }

        function dragstarted(d) {
          d3.event.sourceEvent.stopPropagation();
          
          d3.select(this).classed("dragging", true);
          force.start();
        }

        function dragged(d) {
          
          d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
          
        }

        function dragended(d) {
          
          d3.select(this).classed("dragging", false);
        }	

