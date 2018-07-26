// Dict mapping phonems to brightness/darkness values
var phonemes = {"IH":0,"IY":.25,"EY":1.05,"AY":1.09,"AE":1.1,"UW":1.25,"UH":1.4,"AA":1.65,"AO":1.7};

// Phonemes ordered from light to dark
var phonemeOrder = ["IH","IY","EY","AY","AE","UW","UH","AA","AO"];

// Dict mapping play code to full name
var playDict = {"AWW":"All's Well That Ends Well","Ant":"Antony and Cleopatra","AYL": "As You Like It",
    "Err":"The Comedy of Errors","Cor":"Coriolanus","Cym":"Cymbeline","Ham":"Hamlet","1H4":"Henry IV, Part 1"
    ,"2H4":"Henry IV, Part 2","H5":"Henry V","1H6":"Henry VI, Part 1","2H6":"Henry VI, Part 2","3H6":"Henry VI, Part 3","H8":"Henry VIII",
    "JC":"Julius Caesar", "Jn":"King John","Lr":"King Lear","LLL":"Love's Labor's Lost","Mac":"Macbeth",
    "MM":"Measure for Measure","MV":"The Merchant of Venice","Wiv":"The Merry Wives of Windsor","MND":"A Midsummer Night's Dream",
    "Ado":"Much Ado About Nothing","Oth":"Othello","Per":"Pericles","R2":"Richard II","R3":"Richard III","Rom":"Romeo and Juliet",
    "Shr":"The Taming of the Shrew","Tmp":"The Tempest","Tim":"Timon of Athens","Tit":"Titus Andronicus","Tro":"Troilus and Cressida",
    "TN":"Twelfth Night","TGV":"Two Gentlemen of Verona","TNK":"Two Noble Kinsmen","WT":"The Winter's Tale"};

// Color scale
var minimumColor = "#99D3DF";
var maximumColor = "MidnightBlue";
var color = d3.scaleLinear().domain([0,1.7]).range([minimumColor, maximumColor]);

// Margins
var margin = {top: 10, right: 10, bottom: 15, left: 10},
    smallWidth = 150 - margin.left - margin.right,
    smallHeight = 150 - margin.top - margin.bottom,
    bigWidth = 200,
    bigHeight = 200;

// z-score domain
var selectionZDomain;

var numberOfSVGsinDisplayDiv = 0;

var xOF = d3.scaleBand(),
    yOF = d3.scaleLinear();
// yOF = d3.scaleLinear().rangeRound([smallHeight, 0]);

//tooltip displaying character name
var tip = d3.select("body").append("div").attr("class", "toolTip");

var currentPlay = "";

// EA global vars
var playCharNest;   // Contains nest of all the plays' data
var playData;       // Contains data of selected play
var charsChecked;   // Maps character name to boolean of whether or not they are checked

//update sliderbar value (function not called by its name but by queryselector)
function outputUpdate(numlines) {
    document.querySelector('#numlines').value = numlines;
}

function initPlayControls() {
    // Set play label
    d3.select('#currPlayBrand').text(playDict[CURR_PLAY]);

    // Fill play dropdown
    d3.select('#playDropdown').selectAll('a')
        .data(playCharNest)
        .enter()
        .append('a')
        .attr('class', 'dropdown-item')
        .text(function(d) {
            return playDict[d.key];
        })
        .on('click', function(d) {
            var play_url = flask_util.url_for('bootTacos', {
                play: d.key
            });
            window.location.replace(play_url);
        });

    // Create character checkboxes
    playData = playCharNest.filter(function(d) { return d.key === CURR_PLAY; })[0].value;
    playData.character.sort(function (a, b) { return b.values[0].numlines - a.values[0].numlines; });
    charsChecked = {};
    playData.character.forEach(function(d) {
        charsChecked[d.key] = true;
    })

    var characterCheckboxLabels = d3.select('#characterCheckboxes').selectAll('label')
        .data(playData.character)
        .enter().append('label')
        .attr('id', function(d) { return 'checkbox_' + d.key.replace(/\./g, '_'); })
        .attr('class', 'btn btn-primary active')
        .html(function(d) {
            return '<input type="checkbox" checked>' +
                '<strong>' + d.key + '</strong> <span>' + d.values[0].numlines + ' lines </span>'
        })
        .on('click', function(d) {
            charsChecked[d.key] = !charsChecked[d.key];
            updateSmallMultiples();
        });

    // Initialize numLines slider
    d3.select('#rangeSlider')
        .attr('max', playData.maxNumlines)
        // Dynamically as the slider moves, change label highlighting
        .on('input', function() {
            // Update active class on the checkbox labels
            d3.selectAll('#characterCheckboxes label')
                .classed('active', function(d) {
                    return d.values[0].numlines >= parseInt(document.getElementById('rangeSlider').value);
                });
        })
        // Once slider is *released*, redraw the visualizations
        .on('change', function() {
            // Update charsChecked object
            playData.character.forEach(function(d) {
                if (d.values[0].numlines >= parseInt(document.getElementById('rangeSlider').value)) {
                    charsChecked[d.key] = true;
                } else {
                    charsChecked[d.key] = false;
                }
            });

            // Update the vis
            updateSmallMultiples();
        })
}

// Function that will update the small multiple visualizations after changes are made to controls
function updateSmallMultiples() {
    // Filter character data by what has been selected
    var filteredCharData = playData.character.filter(function(d) {
        return charsChecked[d.key];
        //return d3.select('#checkbox_' + d.key.replace(/\./g, '_')).classed('active');
    })

    // Update the z-score domain to only include filtered characters
    var zExtents = playData.charZscoreExtents.filter(function(item) {
        return charsChecked[item.key];
    });
    var minZ = d3.min([0, d3.min(zExtents, function(item) { return item.value[0]; })]);
    var maxZ = d3.max([0, d3.max(zExtents, function(item) { return item.value[1]; })]);
    selectionZDomain = [minZ, maxZ];

    // Create SVGs for each character
    var charGroup = d3.select('#visCol').selectAll('svg')
        .data(filteredCharData, function(d) { return d.key; });

    // Enter: create the SVGs
    charGroup.enter()
        .append('svg')
        .attr('width', smallWidth + margin.left + margin.right)
        .attr('height', smallHeight + margin.top + margin.bottom)
        .attr('class', 'charGroup');
        //.on('click', zoom);

    // Update all visualizations (scales may have changed)
    //charGroup
    //    .each(drawSig);

    // Remove characters that are no longer selected
    charGroup.exit()
        .remove()

    // Had to put this down here to avoid some race condition where
    // enter() wasn't having drawSig called on it...
    d3.select('#visCol').selectAll('svg')
        .each(drawSig);
}

// Function called on small multiple SVGs
// Draws signature in the calling SVG, using data bound to it
function drawSig(d) {
    // Set up the dimensions of the visualization
    var targetWidth, targetHeight, targetYDomain;
    if (this.className.baseVal == 'charGroup') {    // If we're drawing a small one, set up accordingly
        targetWidth = smallWidth;
        targetHeight = smallHeight;
        targetYDomain = selectionZDomain;
    } else {                                        // If we're drawing a big one, use the available space
        targetWidth = 500;
        targetHeight = bigHeight;
        targetYDomain = d3.extent(d.values, function(item) { return item.zscore; });
    }
    xOF.domain(phonemeOrder).range([2,targetWidth-2]);
    yOF.domain(targetYDomain).rangeRound([targetHeight, 0]);

    // Create a bar for each z-value
    var zBar = d3.select(this).selectAll('.zBar')
        .data(d.values);

    // Create the new bars
    zBar.enter()
        .append('rect')
        .attr('class', function(d) {
            return "zBar zBar_" + d.phoneme;
        })
        .attr('x', function(d) { return xOF([d.phoneme]); })
        .attr('width', targetWidth / phonemeOrder.length)
        .attr('fill', function(d) { return color(phonemes[d.phoneme]); })
        // Highlight corresponding phoneme bars on mouseover
        .on('mouseover', function(d) {
            d3.selectAll('.zBar_' + d.phoneme)
                .raise() // Pulls selection to top--nifty!
                .style('stroke-width', 3)
                .style('stroke', 'black');
        })
        .on('mouseout', function(d) {
            d3.selectAll('.zBar_' + d.phoneme)
                .style('stroke', '');
        })
        // Add title tooltip, too
        .append('svg:title')
        .text(function(d) {
            return d.phoneme + "\nz: " + d.zscore.toFixed(3);
        });

    // Heights might have changed if scale changes (i.e., normalizing by different characters)
    d3.select(this).selectAll('.zBar')
        .attr('height', function(d) {
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

    // Shouldn't be anything exiting, but just in case?
    zBar.exit().remove();

    // If we haven't already labeled this SVG, let's do it now
    if (d3.select(this).selectAll('.sigLabel').size() == 0) {
        d3.select(this).append("text")
            .attr('class', 'sigLabel')
            .attr("x", 0)
            .attr("y", 10)
            .attr("font-size", "10px")
            .text(function (d) {
                return d.key;
            });
    }
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
            return d3.nest()
                .key(function (data) {
                    //organize by play
                    return data.play;
                })
                //do things to the data that is grouped by play
                .rollup(function(leaves){

                    //determine the highest and lowest zscore in each play
                    var zscoreExtent = d3.extent(leaves, function(d){
                        return d.zscore
                    });

                    // Determine the highest and lowest zscore for each character
                    var charZscoreExtents = d3.nest()
                        .key(function(d) {
                            return d.character;
                        })
                        .rollup(function(leaves) {
                            return d3.extent(leaves, function(d) { return d.zscore; });
                        })
                        .entries(leaves);

                    //determine the maximum number of lines by a character in each play
                    var maxNumlines = d3.max(leaves, function(d){
                        return d.numlines;
                    });

                    //nest by character
                    var character = d3.nest()
                        .key(function (data) {
                            return data.character;
                        })
                        .entries(leaves);

                    //return things from the rollup
                    return {
                        zscoreExtent:zscoreExtent,
                        charZscoreExtents:charZscoreExtents,
                        character:character,
                        maxNumlines:maxNumlines
                    };
                })
                .entries(data);
        }

        playCharNest = calculateNest(data);

        initPlayControls();

        updateSmallMultiples();
    }
);