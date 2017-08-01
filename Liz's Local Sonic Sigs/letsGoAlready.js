var data = ["option 1", "option 2", "option 3"]

var select = d3.select('body')
    .append('select')
    .attr('class','select');
    
var options = select
    .selectAll('option')
    .data(data)
    .enter().append('option')
    .text(function (d) { return d; });

var selectValue = d3.select('select')
                    .property('value');


d3.csv("masterData_split.csv", function(d) {return { character : d.character, AA : +d.AA, 
play: d.play,};}, function(data) {console.log(data[0]);});



var svg = d3.select("body").append("svg").attr("height","100%").attr("width","100%");

svg.selectAll("rect")
      .data(dataArray)
      .enter().append("rect")
            .attr("height",function(d,i){return d*15;})
            .attr("width","50")
            .attr("fill",function(d,i){return rainbow(i);})
            .attr("x",function(d,i){return 60 * i;})
            .attr("y",function(d,i){return 300-d*15;})
