$('.spin').spin('hide');

$("#form").submit(function(event) {    

	$('.spin').spin('show');
	d3.select("#viz").selectAll("*").remove();

//d3.json("/" + $("#analysis").val() + "/" + $("#category").val() + "/" + $("#limitResult").val(), function(error, json) {
	d3.json("/static/test.json", function(error, json) {
		switch($("#category").val()){
			case "reference":
			var diameter = 960;

			var max = d3.max(json.children, function(d) { return d.year;} );
			var min = d3.min(json.children, function(d) { return d.year;} );

			var color = d3.scale.linear()
							.domain([min,max])
							.range(['#fee8c8','#e34a33']);


			var svg = d3.select("#viz")
						.attr('width', diameter)
						.attr('height', diameter);

			var bubble = d3.layout.pack()
							.size([diameter, diameter])
							.value(function(d) { return d.size; })
							.padding(1.5);

			var node = svg.selectAll("circle")
						.data(bubble.nodes(json).filter(function(d) { return !d.children; }))
						.enter().append("circle")
						.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

				node.attr("r", 0)
					.style("fill", function(d) { return color(d.year); });
				node.transition().duration(2000).attr("r", function(d) { return d.r; });
				node.on("mousemove", function (d) {
					var nodeSelection = d3.select(this)
										  .attr("class","selected_circle");
					//Get this bar's x/y values, then augment for the tooltip
					var xPosition = d3.event.pageX - 160;
					var yPosition = d3.event.pageY - 60;

					
					var title = "Paper title:" + d.name;
					var text1 = "Reference num: " + d.size; 
					var text2 = "Published year: " + d.year;    

					d3.select("#tooltip")
						.style("left", xPosition + "px")
						.style("top", yPosition + "px")
						.select(".title")
						.text(title)

					d3.select("#tooltip")
						.select(".value")
						.text(text1)

					d3.select("#tooltip")
					  .select(".percent")
					  .text(text2)
					//Show the tooltip
					d3.select("#tooltip").classed("hidden", false);
				});
				node.on("mouseout", mouseout);
			d3.select(self.frameElement).style("height", diameter + "px");




			break;
			case "author":
			var diameter = 960;

			var color = d3.scale.category20c();

			var svg = d3.select("#viz")
				  .attr('width', diameter)
				  .attr('height', diameter);

			var bubble = d3.layout.pack()
							.size([diameter, diameter])
							.value(function(d) { return d.size; }).padding(3);

			var node = svg.selectAll("circle")
					      .data(bubble.nodes(json).filter(function(d) { return !d.children; }))
					      .enter().append("circle")
					      .attr("class", "node")
					      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
				node.attr("r", 0)
				    .style("fill", function(d) { return color(d.name); });
				node.transition().duration(2000).attr("r", function(d) { return d.r; });
				node.on("mousemove", function (d) {
					var nodeSelection = d3.select(this)
										  .attr("class","selected_circle");
					//Get this bar's x/y values, then augment for the tooltip
					var xPosition = d3.event.pageX - 160;
					var yPosition = d3.event.pageY - 60;

					var title = "Author:" + d.name;
					var text1 = "Published num: " + d.size;    

					d3.select("#tooltip")
						.style("left", xPosition + "px")
						.style("top", yPosition + "px")
						.select(".title")
						.text(title)

					d3.select("#tooltip")
						.select(".value")
						.text(text1)
					//Show the tooltip
					d3.select("#tooltip").classed("hidden", false);
				});
				node.on("mouseout", mouseout);




			break;
			case "institute":
			var diameter = 960;

			var color = d3.scale.category20c();

			var svg = d3.select("#viz")
				  .attr('width', diameter)
				  .attr('height', diameter);

			var bubble = d3.layout.pack()
							.size([diameter, diameter])
							.value(function(d) { return d.size; }).padding(3);

			var node = svg.selectAll("circle")
					      .data(bubble.nodes(json).filter(function(d) { return !d.children; }))
					      .enter().append("circle")
					      .attr("class", "node")
					      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
				node.attr("r", 0)
				    .style("fill", function(d) { return color(d.name); });
				node.transition().duration(2000).attr("r", function(d) { return d.r; });
				node.on("mousemove", function (d) {
					var nodeSelection = d3.select(this)
										  .attr("class","selected_circle");
					//Get this bar's x/y values, then augment for the tooltip
					var xPosition = d3.event.pageX - 160;
					var yPosition = d3.event.pageY - 60;

					var title = "Institute:" + d.name;
					var text1 = "Reference num: " + d.size;  

					d3.select("#tooltip")
					.style("left", xPosition + "px")
					.style("top", yPosition + "px")
					.select(".title")
					.text(title)

					d3.select("#tooltip")
					.select(".value")
					.text(text1)

					//Show the tooltip
					d3.select("#tooltip").classed("hidden", false);
				});
				node.on("mouseout", mouseout);
			break;
			case "keyword":
				d3.layout.cloud().size([2000, 2000])
		      	    .words(json)
					.padding(3)
					.rotate(0)
					.text(function(d) { return d.keyword; })
					.fontSize(function(d) { return d.appearances/30; })
					.on("end", draw)
					.start();
					break;
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
            };
function mouseout () {
    var nodeSelection = d3.select(this)
            			  .attr("class","default_circle")
            			  .attr("stroke-width", "0px");
    //Hide the tooltip
    d3.select("#tooltip").classed("hidden", true);
}
