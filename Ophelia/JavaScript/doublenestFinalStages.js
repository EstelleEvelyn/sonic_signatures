// supplies brightness/darkness of phonemes
var phonemes = {"IH":0,"IY":.25,"EY":1.05,"AY":1.09,"AE":1.1,"UW":1.25,"UH":1.4,"AA":1.65,"AO":1.7};
// order from light to dark
var phonemeOrder = ["IH","IY","EY","AY","AE","UW","UH","AA","AO"];
// holds select menu values


var playDict = {"AWW":"All's Well That Ends Well","Ant":"Antony and Cleopatra","AYL": "As You Like It",
"Err":"The Comedy of Errors","Cor":"Coriolanus","Cym":"Cymbeline","Ham":"Hamlet","1H4":"Henry IV, Part 1"
,"2H4":"Henry IV, Part 2","H5":"Henry V","1H6":"Henry VI, Part 1","2H6":"Henry VI, Part 2","3H6":"Henry VI, Part 3","H8":"Henry VIII",
"JC":"Julius Caesar", "Jn":"King John","Lr":"King Lear","LLL":"Love's Labor's Lost","Mac":"Macbeth",
"MM":"Measure for Measure","MV":"The Merchant of Venice","Wiv":"The Merry Wives of Windsor","MND":"A Midsummer Night's Dream",
"Ado":"Much Ado About Nothing","Oth":"Othello","Per":"Pericles","R2":"Richard II","R3":"Richard III","Rom":"Romeo and Juliet",
"Shr":"The Taming of the Shrew","Tmp":"The Tempest","Tim":"Timon of Athens","Tit":"Titus Andronicus","Tro":"Troilus and Cressida",
"TN":"Twelfth Night","TGV":"Two Gentlemen of Verona","TNK":"Two Noble Kinsmen","WT":"The Winter's Tale"};

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

//update sliderbar value (function not called by its name but by queryselector)
function outputUpdate(numlines) {
	document.querySelector('#numlines').value = numlines;
}

//open csv for processing
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
                console.log(playDict[d.key]);
                return playDict[d.key];
            })
            .attr("value", function (d) {
                return d.key;
            })
        
        //create a checklist for the play options
        function characterChecklist(selectPlay) {
           //sort characters for checkboxes descending by number of lines
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

            // d3.selectAll(".playGroups").remove();
            //d3.selectAll(".charGroups").exit().remove();
            
            if (currentPlay != selectedPlay){
                d3.selectAll(".characterCheckBoxes").remove();
                checked = [];
                numlines = "0";
                initialGraph(selectedPlay,numlines);
            }
            else{   
                initialGraph(selectedPlay, numlines, checked);
            }
                
        };    
        
        //graph
        var initialGraph = function(play,numlines,checked) {
           //if no checkboxes due to recent change of play
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
           //create a nest
           playCharNest = calculateNest(filteredData);
           
           //filter by selected play
           var selectPlay = playCharNest.filter(function(d){
               return (d.key == play);
           })
           
           //sort play characters by number of lines
           selectPlay[0].value.character.sort(function(a, b){
               return b.values[0].numlines-a.values[0].numlines;
           });
           
           //set the maximum value of the slider bar to the max numlines for a char of that play
           var sliderBarMax = d3.select("#rangeSlider")
               .attr("max", selectPlay[0].value.maxNumlines);
           
           if (currentPlay != play){
               var checkBoxes = characterChecklist(selectPlay[0].value.character)
               currentPlay = play;
           }
           
           //d3.selectAll(".charGroups").exit().remove();
           //create an svg for each character    
           var charGroups = d3.select(".main").selectAll("svg")
               .data(selectPlay[0].value.character);
               
           var cgEnter = charGroups.enter()
               .append("svg:svg")
               .attr("width", width + margin.left + margin.right)
               .attr("height", height + margin.top + margin.bottom)
               .attr("class","charGroups")
               /*.each(function(d){
                   yOF.domain(selectPlay[0].value.zscoreExtent);
               });*/
            
           y.domain(selectPlay[0].value.zscoreExtent); 
           
           var initialbars = cgEnter.selectAll("bar")
               .data(function (d) {
                   return d.values;
               });
               
           initialbars.enter()
               .append("rect")
               .attr("class", "zBar")
               .attr("x", function(d){
                  return x([d.phoneme]); 
               })
               
               .attr("width", width/phonemeOrder.length)
               // .attr("smallHeight", function(d){
//                    return Math.abs(yOF(d.zscore)-yOF(0));
//                })
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
               
               d3.selectAll('.zBar')
                   .attr("height", function(d){
                       return Math.abs(y(d.zscore)-y(0)); 
                   })
                   .attr("y", function(d){ 
                      if (d.zscore > 0) {
                          return y(d.zscore);
                       } 
                       else {
                          return y(0);
                       } 
                   });
               var labels = d3.selectAll(".charGroups")
                   .append("text")
                   .attr("x",0)
                   .attr("y",10)
                   .text( function(d) {
                       return d.key;
                   })
                   .attr("font-size","8px");
               
               charGroups.exit().remove();
               
               

           }
           initialGraph("1H4", 0)                
    }
);     