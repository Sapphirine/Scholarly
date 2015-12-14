$('.spin').spin('hide');

$("#form").submit(function(event) {    

$('.spin').spin('show');
d3.select("#viz").selectAll("*").remove();

d3.json("/" + $("#analysis").val() + "/" + $("#category").val() + "/" + $("#limitResult").val(), function(error, json) {
  if ($("#category").val() != "keyword") {
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
    } else {
	d3.layout.cloud().size([2000, 2000])
            .words(json)
	    .padding(3)
            .rotate(0)
	    .text(function(d) { return d.keyword; })
            .fontSize(function(d) { return d.appearances/30; })
            .on("end", draw)
            .start();
	}
	 
     $('.spin').spin('hide');
});



    event.preventDefault();
      
});

var color = d3.scale.linear()
            .domain([0,1,2,3,4,5,6,10,15,20,150])
            .range(["#ddd", "#ccc", "#bbb", "#aaa", "#999", "#888", "#777", "#666", "#555", "#444", "#333", "#222"]);


function draw(words) {
	var svg = d3.select("#viz")
   	  .attr('width', 2000)
 	  .attr('height', 2000)
	  .attr('class', 'wordcloud');

	svg.append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(1000,1000)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.appearances/30 + "px"; })
                .style("fill", function(d, i) { return color(i); })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.keyword; });
}
