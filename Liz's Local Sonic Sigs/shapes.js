
var dataArray=[5,11,18];
var dataPuree=[5,-11,18];
var dataDays = ['Mon','Wed','Fri'];

var rainbow = d3.scaleSequential(d3.interpolateRainbow).domain([0,10]);

var x = d3.scaleBand()
              .domain(dataDays)
              .range([0,170])
              .paddingInner(0.1176);

var xAxis = d3.axisBottom(x);

var svg = d3.select("body").append("svg").attr("height","100%").attr("width","100%");

svg.selectAll("rect")
      .data(dataPuree)
      .enter().append("rect")
            .attr("height",function(d,i){return Math.abs(d*15);})
            .attr("width","50")
            .attr("fill",function(d,i){return rainbow(i);})
            .attr("x",function(d,i){return 60 * i;})
            .attr("y",function(d,i){if (d>0) {return 300-d*15;} else { return 300;}})

svg.append("g")
    .attr("class","x axis hidden")
    .attr("transform","translate(0,300)")
    .call(xAxis);

var newX = 300;
svg.selectAll("circle.first")
      .data(dataArray)
      .enter().append("circle")
            .attr("class","first")
            .attr("cx",function(d,i){ newX += (d*3)+(i*20);return newX;})
            .attr("cy","100")
            .attr("r",function(d){ return d*3; });

var newX = 600;
svg.selectAll("ellipse")
      .data(dataArray)
      .enter().append("ellipse")
            .attr("class","second")
            .attr("cx",function(d,i){ newX += (d*3)+(i*20);return newX;})
            .attr("cy","100")
            .attr("rx",function(d){ return d*3; })
            .attr("ry","30");

var newX = 900;
svg.selectAll("line")
      .data(dataArray)
      .enter().append("line")
            .attr("x1",newX)
            .style("stroke","green")
            //.attr("stroke","blue")
            .attr("stroke-width","2")
            .attr("y1",function(d,i){return 80 + (i*20);})
            .attr("x2",function(d){ return newX+(d*15); })
            .attr("y2",function(d,i){return 80 + (i*20);});

svg.append("text")
      .attr("x",newX)
      .attr("y","150")
      .attr("font-size","30")
      .attr("text-anchor","start")
      .attr("fill","none")
      .attr("stroke","blue")
      .attr("stroke-width","2")
      .text("start");
svg.append("text")
      .attr("x",newX)
      .attr("y","180")
      .attr("text-anchor","middle")
      .attr("font-size","30")
      .attr("fill","blue")
      .attr("stroke","none")
      .text("middle");
svg.append("text")
      .attr("x",newX)
      .attr("y","210")
      .attr("text-anchor","end")
      .attr("font-size","30")
      .attr("stroke","blue")
      .attr("fill","none")
      .text("end");