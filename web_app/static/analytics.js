$('.spin').spin('hide');

$("#form").submit(function(event) {    

$('.spin').spin('show');
d3.select("#viz").selectAll("*").remove();

d3.json("/" + $("#analysis").val() + "/" + $("#category").val() + "/" + $("#limitResult").val(), function(error, json) {

	var diameter = 960;

	var color = d3.scale.category20c();

	var svg = d3.select("#viz")
		  .attr('width', diameter)
		  .attr('height', diameter);

	var bubble = d3.layout.pack()
			.size([diameter, diameter])
			.value(function(d) { return d.size; }).padding(3);

	var node = svg.selectAll(".node")
			      .data(bubble.nodes(json).filter(function(d) { return !d.children; }))
			      .enter().append("g")
			      .attr("class", "node")
			      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
		 node.append("circle")
		    .attr("r", function(d) { return d.r; })
		    .on("click", function(d) { alert(d.name); })
		    .style("fill", function(d) { return color(d.name); });
		node.append("text")
		    .attr("dy", ".3em")
		    .style("text-anchor", "middle")
		    .text(function(d) { return d.name.substring(0, d.r / 3) + ":" + d.size; });
		$('.spin').spin('hide');
});


   
    event.preventDefault();
      
});
