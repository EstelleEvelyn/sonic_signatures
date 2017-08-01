

var width = 700,
    height = 500;

var y = d3.scaleLinear()
    .range([height,0]);

var chart = d3.select(".chart")
    .attr("width",width)
    .attr("height", height);


d3.csv("masterData_split.csv", function(csvdata){
    data = csvdata; 
     
    playMap = new Map();
    playKeys = []
    
    for (i = 0; i < data.length; i++){
        //console.log(data[i])
        row = data[i]
        play = row.play
        //console.log(play)
        if (playMap.has(play)){
           //console.log(play + "was in play map")
           entry = playMap.get(play)
           entry.push(row)
           playMap.set(play,entry);}
        else {
        //console.log('tacos')
        playKeys.push(play)
        playMap.set(play,[row])
        }
    }  

    var select = d3.select('body')
       .append('select')
       .attr('class','select')
       .on('change',onchange);
    
    var options = select
       .selectAll('option')
       .data(playKeys)
       .enter().append('option')
       .text(function (d) { return d; });
    
    function onchange() {
       selectValue = d3.select('select').property('value');
       console.log(selectValue);
       d3.selectAll("g").remove()
       updateGraph(playMap.get(selectValue)); }
})
//                     .property('value')
//                     .on("change", function () { console.log("tacos");})
//                     
//     play = playMap.get('1H4');
    
function updateGraph(play) {

    y.domain([0, d3.max(play, function(d) { return d.AA;})])
    
    //console.log(play[1]);
    
    var barWidth = width / play.length;
    
    var bar = chart.selectAll("g")
        .data(play)
      .enter().append("g")
        .attr("transform",function(d,i) { return "translate(" + i * barWidth + ",0)"; });
      
    bar.append("rect")
       .attr("y",function(d){ return y(d.AA) ; })
       .attr("height", function(d) { return height - y(d.AA); })
       .attr("width", barWidth - 1);
   
    bar.append("text")
       .attr("x", barWidth/2 )
       .attr("y", function(d) { return y(d.AA) + 3; })
       .attr("dy", ".75em")
       .attr("text-anchor","middle")
       .text(function(d) { return d.character ; });

    // update existing elements
    //d3.selectAll("rect").remove();

        //.attr("width",function (d) {return d.y; });

    // remove old elements
    //chart.exit().remove();



 };

function type(d) {
    d.AA = +d.AA; //coerce to number
    return d;
};    
     