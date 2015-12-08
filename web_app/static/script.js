jQuery(function($) {
    var width = 1000,
    bar_height = 20,
    left_width = 200;
    d3.json("/top_authors_within_top_institutes", function(error, data) {
    if (error) return;
    var height = data.length*bar_height;
    var arrauthorname = $.map( data, function( d, i ) { return d.AuthorName; } );
    var arrpubnum = $.map(data, function(d,i) { return d.PublishNum });
    var x, y;

    x = d3.scale.linear()
    .domain([0, d3.max(arrpubnum)])
    .range([0, width]);
    var gap = 2, yRangeBand;
    yRangeBand = bar_height + 2 * gap;
    y = function(i) { return yRangeBand * i; };
    
    chart = d3.select($("#topauthor")[0])
    .append('svg')
    .attr('class', 'chart')
    .attr('width', left_width + width + 40)
    .attr('height', (bar_height + gap * 2) * arrpubnum.length + 30)
    .append("g")
    .attr("transform", "translate(10, 20)");
    
    chart.selectAll("line")
    .data(x.ticks(d3.max(arrpubnum)/10))
    .enter().append("line")
    .attr("x1", function(d) { return x(d) + left_width; })
    .attr("x2", function(d) { return x(d) + left_width; })
    .attr("y1", 0)
    .attr("y2", (bar_height + gap * 2) * arrpubnum.length);
    
    chart.selectAll(".rule")
    .data(x.ticks(d3.max(arrpubnum)/10))
    .enter().append("text")
    .attr("class", "rule")
    .attr("x", function(d) { return x(d) + left_width; })
    .attr("y", 0)
    .attr("dy", -6)
    .attr("text-anchor", "middle")
    .attr("font-size", 10)
    .text(String);
    
    chart.selectAll("rect")
    .data(arrpubnum)
    .enter().append("rect")
    .attr("x", left_width)
    .attr("y", function(d, i) { return y(i) + gap; })
    .attr("width", x)
    .attr("height", bar_height);
    
    chart.selectAll("text.score")
    .data(arrpubnum)
    .enter().append("text")
    .attr("x", function(d) { return x(d) + left_width; })
    .attr("y", function(d, i) { return y(i) + yRangeBand/2;})
    .attr("dx", -5)
    .attr("dy", ".36em")
    .attr("text-anchor", "end")
    .attr('class', 'score')
    .text(String);
    
    chart.selectAll("text.name")
    .data(arrauthorname)
    .enter().append("text")
    .attr("x", left_width / 2)
    .attr("y", function(d, i){ return y(i) + yRangeBand/2; } )
    .attr("dy", ".36em")
    .attr("text-anchor", "middle")
    .attr('class', 'name')
    .text(String);
    });
    }(jQuery));