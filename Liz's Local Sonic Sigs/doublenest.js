// supplies brightness/darkness of phonemes
var phonemes = {"IH":0,"IY":.25,"EY":1.05,"AY":1.09,"AE":1.1,"UW":1.25,"UH":1.4,"AA":1.65,"AO":1.7};
// order from light to dark
var phonemeOrder = ["IH","IY","EY","AY","AE","UW","UH","AA","AO"];
// holds select menu values
var plays = [];

//color scale
var minimumColor = "Pink";
var maximumColor = "MidnightBlue";
var color = d3.scaleLinear().domain([0,1.7]).range([minimumColor, maximumColor]);

//margin
var margin = {top: 10, right: 10, bottom: 15, left: 10},
    width = 120 - margin.left - margin.right,
    height = 100 - margin.top - margin.bottom;

var x = d3.scaleBand(),         
    y = d3.scaleLinear().rangeRound([height, 0]);

var tip = d3.select("body").append("div").attr("class", "toolTip");

// added just to have another svg         
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g") // TODO: is this still needed?
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
              
d3.csv("charPhoneZScoresNumlines.csv",
    function(d) {
        d.zscore = parseFloat(d.zscore);
        d.numlines = +d.numlines;
        //console.log(d.numlines);
        if (!(plays.indexOf(d.play) > -1)) {
            plays.push(d.play);
        }
        return d;
        //if (d.play == "1H4" && phonemes.hasOwnProperty(d.phoneme) && d.numlines > 1000) {
        //  return d;
        //}
    },
    function(error, data) {
        if (error) throw error;
        var playCharNest = d3.nest()
            .key(function (data) {
                return data.play;
            })
            .key(function (data) {
                return data.character;
            })
            .entries(data);

        var playGroups = svg.selectAll(".playGroups")
            //.data(playCharNest)
            .data(playCharNest[0].values)
            .enter()
            .append("g");

        var playMenu = d3.select('body')
            .append("select")
            .selectAll("option")
            .data(playCharNest)
            .enter()
            .append("option")
            .attr("value", function (d) {
                return d.key;
            })
            .text(function (d) {
                return d.key;
            });

        // var initialGraph = function(play) {
        //       var selectPlay = playCharNest.filter(function(d){
        //          return d.key == play;
        //       })

        //  var selectPlayGroups = svg.selectAll(".playGroups")
        //           .data(selectPlay, function(d){
        //               return d ? d.key : this.key;
        //           })
        //           .enter()
        //           .append("g")
        //           .attr("class","playGroups")

        var circles = playGroups.selectAll("circle")
            .data(function (d) {
                return d.values;
            })
            .enter()
            .append("circle")
            .attr("cy", 60)
            .attr("cx", function (d, i) {
                return i * 100 + 30;
            })
            .attr("r", function (d) {
                if (phonemeOrder.indexOf(d.phoneme) != -1) {
                    return phonemes[d.phoneme] + 30;
                } else {
                    return 0;
                }
            });
        // }
        // initialGraph("1H4")
    }
);


 // var charSVG = playGroups.selectAll("svg")
//       .data(function(d){
//           return d.values;
//        })
//       .enter().append("svg:svg")
//       .attr("width", width + margin.left + margin.right)
//       .attr("height", height + margin.top + margin.bottom);
//   
//    charSVG.append('title')
//           .text(function(d) {return d.key;});    
//  
//    var g = charSVG.append("g")
//       .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
//       
// 
//      x.domain(data.map(function(d) { return d.phoneme; }));
//      x.domain(phonemeOrder)
//        .range([0,width]);
//        
//      y.domain(d3.extent(playGroups, function(d) { return d.values[0].zscore; }));
//     
//          
//      g.selectAll(".bar")
//        .data(function(d){return d.values;})
// 
//        .enter().append("rect")
//          .attr("class", "bar")
//          .attr("x", function(d) { return x([d.phoneme]); })
//          .attr("y", function(d) { if (d.zscore > 0) {return y(d.zscore);} else {return y(0);} })
//          .attr("width", width/phonemeOrder.length)
//          .attr("height", function(d) { return Math.abs(y(d.zscore)-y(0)); })
//          .attr("fill",function(d){ var phoneme = d.phoneme; return color(phonemes[phoneme]) ;})
//          .on('mouseover', function(d) {  
//              
//              var charactertext = d.character
//              var xPosition = parseFloat(d3.select(this).attr("x"));
//              var yPosition = parseFloat(d3.select(this).attr("y"));
//          
//              d3.selectAll(".toolTip")
//                .style("display","inherit")
//                .style("left", xPosition+"px")
//                .style("top", yPosition+"px")
//                .text(charactertext);
//          })
//          .on('mouseout', function(d){ tip.style("display","none");});

//})                   
