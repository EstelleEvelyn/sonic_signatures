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
    smallWidth = 120 - margin.left - margin.right,
    smallHeight = 100 - margin.top - margin.bottom,
    bigWidth = 200,
    bigHeight = 200;

var domains = {
    maindomain:[],
    detaildomain:[]

}

var numberOfSVGsinDisplayDiv = 0;

var xOF = d3.scaleBand(),
    yOF = d3.scaleLinear();
    // yOF = d3.scaleLinear().rangeRound([smallHeight, 0]);

//tooltip displaying character name
var tip = d3.select("body").append("div").attr("class", "toolTip");

var currentPlay = "";

//update sliderbar value (function not called by its name but by queryselector)
function outputUpdate(numlines) {
	document.querySelector('#numlines').value = numlines;
}

//open csv for processing
//d3.csv("../data/charPhoneZScoresNumlines.csv",
d3.csv(DATA_URL,
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
        

        //create the range slider
        var rangeSlider = d3.select("#rangeSlider")
            .on("change", onchange);
        
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
                //console.log(playDict[d.key]);
                return playDict[d.key];
            })
            .attr("value", function (d) {
                return d.key;
            });
        
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

        function close(){
           //this.parentElement.remove()
        }

        function doEricsThing(){

        }

        function zoom(d) {
            console.log(d)
            toggleHidden(true)

            d3.select("#detailView").append("div").attr("class",'emptyDetail')

            details = d3.selectAll(".emptyDetail").selectAll("svg")
                .data([d])
                .enter()
                .append("svg:svg")
                .attr("width", "100%")
                .attr("height","200px")
                .attr("class","detailCharGroups")
                .each(draw)
                .each(drawDetails)

            d3.selectAll(".emptyDetail").classed("emptyDetail",false);

            d3.selectAll(".detailCharGroups")
                .classed("closeable",true)
                .on("click",doEricsThing());



            // details.enter().append("svg:svg")
            //     .attr("width", "100%")
            //     .attr("height","200px")
            //     .attr("class","detailCharGroups")
            //     .each(draw)
            // details.exit().remove();
        };


        function toggleHidden(show){
            d3.select("#detailView").classed("hidden", !show).classed("visible", show)
            d3.select("#about").classed("hidden", show).classed("visible", show)
        }

        function drawDetails(d){
            d3.selectAll(".detailCharGroups").selectAll(".bar")
                .append("text")
                .attr("x",function(d,i){return this.parentElement.childNodes[0].getAttribute("x");})
                .attr("y",function(d,i){return this.parentElement.childNodes[0].getAttribute("y");})
                .text(function(d){return d.phoneme;})

            LeftAxis = d3.axisLeft(d3.scaleLinear().domain(domains.detaildomain).range([0,200]))
            d3.selectAll(".detailCharGroups").append("g")
                .attr("transform", "translate(20,0)")
                .call(LeftAxis)


        }

        function draw(d){
            // console.log(d)

            //set up x axis scaling using array of phonemes

            if(this.className.baseVal == "charGroups"){
                targetWidth = smallWidth;
                targetHeight = smallHeight;
                targetYDomain = domains.maindomain
            }else if(this.className.baseVal == "detailCharGroups"){
                targetWidth = document.getElementById('detailView').offsetWidth - 30;
                targetHeight = bigHeight;
                domains.detaildomain = d3.extent(d.values, function(element){return(element.zscore);});
                targetYDomain = domains.detaildomain;
            }

            if(this.className.baseVal == "detailCharGroups"){
               d3.select(this).append('svg:foreignObject')
                   .attr("x","300px")
                   .html('<i class="fas fa-times"></i>')
                   .on("click",close())
            }

            if(this.className.baseVal == "detailCharGroups"){
                xOF.domain(phonemeOrder).range([20,targetWidth]);
            }

            else{
                xOF.domain(phonemeOrder).range([0,targetWidth]);
            }



            // xOF.domain(phonemeOrder).range([0,targetWidth]);
            yOF.rangeRound([targetHeight, 0]).domain(targetYDomain);

            var initialbars = d3.select(this).selectAll(".bar")
                .data(d.values
                );

            initialbars.enter().append("g").attr("class","bar")
                .append("rect")
                .attr("class", "zBar")
                .attr("x", function (d) {
                    return xOF([d.phoneme]);
                })
                .attr("width",function(){return targetWidth/phonemeOrder.length})

                // .attr("width", function(){if(this.parentElement.parentElement.className.baseVal == "detailCharGroups") {
                //     console.log(this.className.baseVal)
                //     return 80 / phonemeOrder.length + "%";
                //
                // } else if(this.parentElement.parentElement.className.baseVal == "charGroups"){
                //    return targetWidth / phonemeOrder.length;
                // }})


                // .attr("height", function(d){
                //                    return Math.abs(yOF(d.zscore)-yOF(0));
                //                })
                .attr("fill", function (d) {
                    var phoneme = d.phoneme;
                    return color(phonemes[phoneme]);
                })
                .attr("title", function (d) {
                    return d.phoneme;
                })
                .on('mouseover', function (d) {

                    var charactertext = d.character
                    var xPosition = parseFloat(d3.select(this).attr("x"));
                    var yPosition = parseFloat(d3.select(this).attr("y"));

                    d3.selectAll(".toolTip")
                        .style("display", "inherit")
                        .style("left", xPosition + "px")
                        .style("top", yPosition + "px")
                        .text(charactertext);
                })
                .on('mouseout', function (d) {
                    tip.style("display", "none");
                });

            d3.select(this).selectAll('.zBar')
                .attr("height", function (d) {
                    return Math.abs(yOF(d.zscore) - yOF(0));
                })
                .attr("y", function (d) {
                    if (d.zscore > 0) {
                        return yOF(d.zscore);
                    }
                    else {
                        return yOF(0);
                    }
                });
            var labels = d3.select(this)
            // .enter()
                .append("text")
                .attr("x", 0)
                .attr("y", 10)
                .text(function (d) {
                    return d.key;
                })
                .attr("font-size", "8px");

            if(this.className.baseVal == "detailCharGroups"){
                var details = d3.select(this).selectAll('.zBar').append("text")
                    .attr("x",0)
                    .attr("y",10)
                    .text(function(d){
                        return d.phoneme;
                    })
                    .attr("font-size","12px")



            }




        }

        //graph
        var initialGraph;
        initialGraph = function (play, numlines, checked) {
            //if no checkboxes due to recent change of play
            if (typeof checked === 'undefined') {
                filteredData = data.filter(function (d) {
                    return (d.numlines >= numlines);
                })
            }
            else {
                filteredData = data.filter(function (d) {
                    if (checked.indexOf(d.character) != -1) {
                        return (d.numlines >= numlines);
                    }
                });
            }
            //create a nest
            playCharNest = calculateNest(filteredData);

            //filter by selected play
            var selectPlay = playCharNest.filter(function (d) {
                return (d.key == play);
            })

            //sort play characters by number of lines
            selectPlay[0].value.character.sort(function (a, b) {
                return b.values[0].numlines - a.values[0].numlines;
            });

            //set the maximum value of the slider bar to the max numlines for a char of that play
            var sliderBarMax = d3.select("#rangeSlider")
                .attr("max", selectPlay[0].value.maxNumlines);

            if (currentPlay != play) {
                var checkBoxes = characterChecklist(selectPlay[0].value.character)
                currentPlay = play;
            }

            //create an svg for each character
            var charGroups = d3.select(".main").selectAll("svg")
                .data(selectPlay[0].value.character,
                    function (d) {
                        return d.key;
                    }
                );

            domains.maindomain = selectPlay[0].value.zscoreExtent;

            var cgEnter = charGroups.enter()
                .append("svg:svg")
                .attr("width", smallWidth + margin.left + margin.right)
                .attr("height", smallHeight + margin.top + margin.bottom)
                .attr("class", "charGroups")
                .on('click', function (d) {
                    zoom(d)
                })
            ;

            d3.selectAll(".charGroups").each(draw)
            // var desiredYDomain = selectPlay[0].value.zscoreExtent;


            // yOF.domain(selectPlay[0].value.zscoreExtent);


            charGroups.exit().remove();

        };
           initialGraph("1H4", 0)                
    }
);     