// supplies brightness/darkness of phonemes
var phonemes = {"IH":0,"IY":.25,"EY":1.05,"AY":1.09,"AE":1.1,"UW":1.25,"UH":1.4,"AA":1.65,"AO":1.7};
// order from light to dark
var phonemeOrder = ["IH","IY","EY","AY","AE","UW","UH","AA","AO"];
// holds select menu values

//color scale
var minimumColor = "#99D3DF";
var maximumColor = "MidnightBlue";
var color = d3.scaleLinear().domain([0,1.7]).range([minimumColor, maximumColor]);

//margin
var margin = {top: 10, right: 10, bottom: 15, left: 10},
    width = 120 - margin.left - margin.right,
    height = 100 - margin.top - margin.bottom;

var x = d3.scaleBand(),         
    y = d3.scaleLinear().rangeRound([height, 0]);

//tooltip displaying character name
var tip = d3.select("body").append("div").attr("class", "toolTip");

var currentPlay = ""


//update sliderbar value
function outputUpdate(numlines) {
	document.querySelector('#numlines').value = numlines;
}

d3.csv("../data/charPhoneZScoresNumlines.csv",
    function(d) {
        //parse numbers as numbers not strings
        d.zscore = parseFloat(d.zscore);
        d.numlines = +d.numlines;
        
        //only include vowels
        if (phonemes.hasOwnProperty(d.phoneme)){
        return d;
        }
    },
    function(error, data) {
        if (error) throw error;
        
        //function to calculate the nest based on filtered data
        function calculateNest(data) {
            //create the nest
            var playCharNest = d3.nest()
                .key(function (data) {
                    //organize by play
                    return data.play;
                })
                //do things to the data that is grouped by play
                .rollup(function(leaves){
                    
                    //determine the highest and lowest zscore in each play
                    var zscoreExtent = d3.extent(leaves, function(d){
                        return d.zscore
                    })
                    //determine the maximum number of lines by a character in each play
                    var maxNumlines = d3.max(leaves, function(d){
                        return d.numlines;
                    })
                    //nest by character
                    var character = d3.nest().key(function (data) {
                        return data.character;
                    })
                    .entries(leaves);
                    //return things from the rollup
                    return {zscoreExtent:zscoreExtent, character:character, maxNumlines:maxNumlines};
               })
               .entries(data);
          
            return playCharNest;    
        }
        
        playCharNest = calculateNest(data);
        //console.log(playCharNest);
        
        //set up x axis scaling using array of phonemes
        x.domain(phonemeOrder).range([0,width]);
        
        //create the range slider
        var rangeSlider = d3.select("#rangeSlider")
            .on("change", onchange)
        
        //create the play dropdown
        var playMenu = d3.select("#navbar")
            .append("select")
            .on("change",onchange)
            .attr("id","playMenu");
        
        //options for the play dropdown    
        var playMenuOptions = playMenu.selectAll("option")
            .data(playCharNest)
            .enter()
            .append("option")
            .text(function (d) {
                return d.key;
            })
            .attr("value", function (d) {
                return d.key;
            })
        
        //create a checklist for the play options
        function characterChecklist(selectPlay) {
           
           selectPlay.sort(function(a, b){
               return b.values[0].numlines-a.values[0].numlines;
           });
           
           var checkboxdivs = d3.select("#characterChecklist").selectAll("div")
               .data(selectPlay)
               .enter().append("div")
               .attr("class","characterCheckBoxes")
               .append("label")
               .attr("class","characterCheckBoxes")
               .text(function(d){
                   return (d.key);
               })
               .append("input")
               .attr("type","checkbox")
               .attr("class", "characterCheckBoxes")
               .attr("value",function(d) {
                   return (d.key);
               })
               .attr("checked","true")
               .on("change", onchange);
        }
        
        d3.selection.prototype.checked = function(value) {
               return arguments.length < 1
                   ? this.property("checked")
                   : this.property("checked", !!value);
           };
        
        //determine which plays are checked   
        function findChecked() {
            checked = []
               
            checkedBoxes = d3.selectAll(".characterCheckBoxes:checked")._groups[0]
               
            for (i=0;i<checkedBoxes.length;i++){
                checked.push(checkedBoxes[i].value);
            }
               
            return checked;
        }
        
        //onchage
        function onchange() {
              
            var selectedPlay = d3.select("select")
                .property("value");
            var numlines = d3.select("#rangeSlider")
                .property("value");
            var checked = findChecked();    

            d3.selectAll(".playGroups").remove();
            d3.selectAll(".charGroups").remove();
            
            if (currentPlay != selectedPlay){
                //console.log("currentplay doesn't equal selectedplay")
                d3.selectAll(".characterCheckBoxes").remove();
                initialGraph(selectedPlay,numlines);
            }
            else{   
                initialGraph(selectedPlay, numlines, checked);
            }
                
        };    

        var initialGraph = function(play,numlines,checked) {
           
           if (typeof checked === 'undefined'){
               filteredData = data.filter(function (d){
                   return (d.numlines >= numlines);
               })
           }
           else{
              filteredData = data.filter(function (d){
                  if (checked.indexOf(d.character) != -1){
                      return (d.numlines >= numlines);
                  }
              });
           }
           
           playCharNest = calculateNest(filteredData);
           
           var selectPlay = playCharNest.filter(function(d){
               return (d.key == play);
           })
           
           var sliderBarMax = d3.select("#rangeSlider")
               .attr("max", selectPlay[0].value.maxNumlines);
           
           if (currentPlay != play){
               console.log(currentPlay);
               console.log("current play does not equal play")
               var checkBoxes = characterChecklist(selectPlay[0].value.character)
               currentPlay = play;
           }
                 
           var charGroups = d3.select(".main").selectAll("svg")
               .data(selectPlay[0].value.character)
               .enter().append("svg:svg")
               .attr("width", width + margin.left + margin.right)
               .attr("height", height + margin.top + margin.bottom)
               .attr("class","charGroups")
               .each(function(d){
                   y.domain(selectPlay[0].value.zscoreExtent);
               })
               .attr("onclick", function(d){console.log("hello")});

           
           var initialbars = charGroups.selectAll("bar")
               .data(function (d) {
                   //console.log(d.values);
                   return d.values;
               })
               .enter()
               .append("rect")
               .attr("class", "bar")
               .attr("x", function(d){
                  return x([d.phoneme]); 
               })
               .attr("y", function(d){ 
                   if (d.zscore > 0) {
                       return y(d.zscore);
                   } 
                   else {
                       return y(0);
                   } 
               })
               .attr("width", width/phonemeOrder.length)
               .attr("height", function(d){
                   return Math.abs(y(d.zscore)-y(0)); 
               })
               .attr("fill",function(d){
                   var phoneme = d.phoneme; 
                   return color(phonemes[phoneme]);
               })
               .attr("title", function(d) {
                   return d.phoneme;
               })
               .on('mouseover', function(d) {  
             
                   var charactertext = d.character
                   var xPosition = parseFloat(d3.select(this).attr("x"));
                   var yPosition = parseFloat(d3.select(this).attr("y"));
         
                   d3.selectAll(".toolTip")
                     .style("display","inherit")
                     .style("left", xPosition+"px")
                     .style("top", yPosition+"px")
                     .text(charactertext);
               })
               .on('mouseout', function(d){
                   tip.style("display","none");
               });

           }
           initialGraph("1H4", 0)                
    }
);


//      var charSVG = playGroups.selectAll("svg")
//          .data(function(d){
//              return d.values;
//          })
//          .enter().append("svg:svg")
//          .attr("smallWidth", smallWidth + margin.left + margin.right)
//          .attr("smallHeight", smallHeight + margin.top + margin.bottom);
//   
//      charSVG.append('title')
//          .text(function(d) {
//              return d.key;
//          });    
//  
//      var g = charSVG.append("g")
//          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
//       
// 
//      x.domain(data.map(function(d){ 
//          return d.phoneme; 
//      }));
//
//      x.domain(phonemeOrder)
//          .range([0,smallWidth]);
//        
//      yOF.domain(d3.extent(playGroups, function(d) {
//          return d.values[0].zscore; 
//      }));
//     
//          
//      g.selectAll(".bar")
//          .data(function(d){
//              return d.values;
//          })
//          .enter().append("rect")
//          .attr("class", "bar")
//          .attr("x", function(d){
//             return x([d.phoneme]); 
//          })
//          .attr("yOF", function(d){
//              if (d.zscore > 0) {
//                  return yOF(d.zscore);
//          } 
//              else {
//                  return yOF(0);
//          } })
//          .attr("smallWidth", smallWidth/phonemeOrder.length)
//          .attr("smallHeight", function(d){
//              return Math.abs(yOF(d.zscore)-yOF(0));
//          })
//          .attr("fill",function(d){
//              var phoneme = d.phoneme; 
//              return color(phonemes[phoneme]);
//          })
//          .on('mouseover', function(d) {  
//              
//              var charactertext = d.character
//              var xPosition = parseFloat(d3.select(this).attr("x"));
//              var yPosition = parseFloat(d3.select(this).attr("yOF"));
//          
//              d3.selectAll(".toolTip")
//                .style("display","inherit")
//                .style("left", xPosition+"px")
//                .style("top", yPosition+"px")
//                .text(charactertext);
//          })
//          .on('mouseout', function(d){
//              tip.style("display","none");
//          });
//
//})                   
