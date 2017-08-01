// Part of a brief D3 tutorial
// Upon completion, will draw random circles of different colors to an SVG.
// CS 314, Spring 2017
// Eric Alexander

// Define some variables that will control the image being drawn.
var svgWidth = 400;
var svgHeight = 400;
var buffer = 10;
var numPoints = 20;
var minRadius = 5;
var maxRadius = 10;
var colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628'];

// Create a new SVG and populate it with points corresponding to given data.
var drawPoints = function(data) {

};

// This function will run once the rest of the page is finished loading.
window.onload = function() {

	// Create points of random location, radius, and color
    var data = [];
    var point;
    for (var i = 0; i < numPoints; i++) {
        point = {};
        point['x'] = Math.floor(Math.random() * (svgWidth - 2*buffer)) + buffer;
        point['y'] = Math.floor(Math.random() * (svgHeight - 2*buffer)) + buffer;
        point['r'] = minRadius + Math.floor(Math.random() * (maxRadius - minRadius));
        point['c'] = colors[Math.floor(Math.random() * colors.length)];
        data.push(point);
    }

    // Draw those points
    drawPoints(data);
};