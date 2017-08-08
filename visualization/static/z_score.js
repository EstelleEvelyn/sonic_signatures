var svgHeight = 3200;
var buffer = 10;

var svg = d3.select("body").append("svg")
            .attr('width', '100%')
            .attr('height', svgHeight)

var featScale = d3.scale.linear()
            .domain([-2, 2])
            .range([0, 50])

var phonScale = d3.scale.linear()
            .domain([-2, 2])
            .range([51, 100])

var featDiv = svg.append('g')
            .property('id', 'feats')


var features = ['fricative', 'affricate', 'glide', 'nasal', 'liquid',
        'stop', 'glottal', 'linguaalveolar', 'linguapalatal', 'labiodental',
        'bilabial', 'linguavelar','linguadental', 'voiced', 'voiceless',
        'sibilant', 'nonsibilant', 'sonorant', 'nonsonorant', 'coronal',
        'noncoronal', 'monophthong', 'diphthong', 'central', 'front', 'back',
        'tense', 'lax', 'rounded', 'unrounded']

var fSegment = (svgHeight - 2*buffer) / (features.length)


var fTopLine = d3.select('svg')
                    .select('#feats')
                    .selectAll('line')
                    .data(features)
                    .enter()
                    .append('line')
                    .attr('x1', '0%')
                    .attr('x2', '50%')
                    .attr('y1', function(d, i) { return h = buffer + (fSegment * i); })
                    .attr('y2', function(d, i) { return h = buffer + (fSegment * i); })
                    .style('stroke', 'black');

var fPivotLine = d3.select('svg')
                    .select('#feats')
                    .append('line')
                    .attr('x1', '25%')
                    .attr('x2', '25%')
                    .attr('y1', svgHeight - buffer)
                    .attr('y2', buffer)
                    .style('stroke', 'black')

var phonDiv = svg.append('g')
            .property('id', 'phons')

var phonemes = ['AA','AE','AH','AO','AW','AY','B','CH','D','DH','EH','ER','EY',
    'F','G','HH','IH','IY','JH','K','L','M','N','NG','OW','OY','P','R','S','SH','T','TH',
    'UH','UW','V','W','Y','Z','ZH']

var pSegment = (svgHeight - 2*buffer) / (phonemes.length)

var pTopLine = d3.select('svg')
                    .select('#phons')
                    .selectAll('line')
                    .data(phonemes)
                    .enter()
                    .append('line')
                    .attr('x1', '51%')
                    .attr('x2', '100%')
                    .attr('y1', function(d, i) { return h = buffer + (pSegment * i); })
                    .attr('y2', function(d, i) { return h = buffer + (pSegment * i); })
                    .style('stroke', 'black');


  var pPivotLine = d3.select('svg')
                    .select('#phons')
                    .append('line')
                    .attr('x1', '75.5%')
                    .attr('x2', '75.5%')
                    .attr('y1', svgHeight - buffer)
                    .attr('y2', buffer)
                    .style('stroke', 'black')

onLoad();

function onfSelect() {

    d3.select('#fCharacter')
      .selectAll('option')
      .remove();

    var fPlay = document.getElementById('fPlay').value
    var dataURL = '/options/' + fPlay
    d3.json(dataURL, function(error, data) {
      var data = data;
      if (data[0] != 'Character') {
        d3.select('#fCharacter')
          .selectAll('option')
          .data(data)
          .enter()
          .append('option')
          .text(function(d) { return d; })
          .property('value', function(d) {
            return fChar = fPlay + "_" + d;
          })
      }
      else {
        d3.select('#fCharacter')
          .append('option')
          .text('Character')
          .property('value', 'reset')
      }
    });
    loadData();
  }

function onpSelect() {
    d3.select('#pCharacter')
      .selectAll('option')
      .remove();

    var pPlay = document.getElementById('pPlay').value
    var dataURL = '/options/' + pPlay
    d3.json(dataURL, function(error, data) {
      var data = data;
      if (data[0] != 'Character') {
        d3.select('#pCharacter')
          .selectAll('option')
          .data(data)
          .enter()
          .append('option')
          .text(function(d) { return d; })
          .property('value', function(d) {
            return pChar = pPlay + "_" + d;
          })
      }
      else {
        d3.select('#pCharacter')
          .append('option')
          .text('Character')
          .property('value', 'reset')
    }
  });
  loadData();
}

function onLoad() {

  svg.select('#feats').selectAll('g').remove()
  svg.select('#feats').selectAll('text').remove()

  svg.select('#phons').selectAll('g').remove()
  svg.select('#phons').selectAll('text').remove()

  var featureGroup = svg.select('#feats')
                      .selectAll('g')
                      .data(features)
                      .enter()
                      .append('g')
                      .property('id', function(d) {return d; })


  var fBoxLabel = svg.select('#feats')
                      .selectAll('text')
                      .data(features)
                      .enter()
                      .append('text')
                      .text(function(d) { return d; })
                      .attr('y', function(d, i) { return buffer + (fSegment * i) + 10; })
                      .attr('x', '1%');

  var phonemeGroup = svg.select('#phons')
                      .selectAll('g')
                      .data(phonemes)
                      .enter()
                      .append('g')
                      .property('id', function(d) {return d; })


  var pBoxLabel = svg.select('#phons')
                      .selectAll('text')
                      .data(phonemes)
                      .enter()
                      .append('text')
                      .text(function(d) { return d; })
                      .attr('y', function(d, i) { return buffer + (pSegment * i) + 10; })
                      .attr('x', '51%');

  loadData();
}

function loadData() {

  d3.selectAll('.fant').remove()
  d3.selectAll('.ffool').remove()
  d3.selectAll('.fprot').remove()
  d3.selectAll('.fprot_bar').remove()
  d3.selectAll('.fant_bar').remove()
  d3.selectAll('.ffool_bar').remove()

  var dataURL = '/data'
  d3.json(dataURL, function(error, data){
    var fdata = data['features']
    var pdata = data['phonemes']

    for (var i = 0; i < features.length; i++) {
      var feat_bars =   d3.select('#'+features[i])
                      .selectAll('rect')
                      .data(obj = fdata[features[i]])
                      .enter()
                      .append('rect')
                      .property('id', function(d, j) {
                        if (j == 0) {
                          return features[i] + '_prot';
                        } else if (j == 1) {
                          return features[i] + '_ant';
                        } else {
                          return features[i] + '_fool';
                        }
                      })
                      .attr('x', function (d) {
                          if (d > 0) {
                            return('25%')
                          } else {
                            // norm = 1+d;
                            // pos = 25 * (norm);
                            pos = featScale(d3.max([-2, d]))
                            return(pos.toString()+'%')

                          }
                        })
                      .attr('y', function(d, j) { return i * fSegment + j * fSegment / 3 + buffer * 1.25; })
                      .attr('width', function(d) {
                        // pos = Math.abs(d * 25)
                        // return pos.toString()+'%';
                        if (d > 0) {
                          pos = featScale(d3.min([2, d])) - 25
                          return(pos.toString()+'%')
                          // return pos = '25%';
                        } else {
                          pos = 25 - Math.abs(featScale(d3.max([-2, d])))
                          return (pos.toString()+'%')
                        }
                      })
                      .attr('height', fSegment / 3 - buffer / 2)
                      .attr('class', function (d, j) {
                        if (j == 0) {
                          return 'fprot';
                        } else if (j == 1) {
                          return 'fant';
                        } else {
                          return 'ffool';
                        }
                      })
                      // .style('fill', function(d, j) {
                      //   if (j == 0) {
                      //     // if (d < 0) {
                      //     //   return '#9216B2';
                      //     // } else {
                      //       return '#E68BFF';
                      //     // }
                      //   } else if (j == 1) {
                      //     // if (d < 0) {
                      //     //   return '#034F34';
                      //     // } else {
                      //       return '#3ECC97';
                      //     // }
                      //   } else {
                      //     // if (d < 0) {
                      //     //   return '7F6118';
                      //     // } else {
                      //       return '#FFDB83';
                      //     // }
                      //   }
                      // })
                      // .style('stroke', function(d) {
                      //   if (d < 0) {
                      //     return 'red';
                      //   } else {
                      //     return 'black'
                      //   }
                      // })
                      .on("mouseover", function(d){
                          d3.select(this).style("fill", d3.rgb(d3.select(this).style("fill")).darker());
                          tip.show(d);
                      })
                      .on("mouseout", function(d){
                          tip.hide(d);
                          d3.select(this).style("fill", function() {
                              return d3.rgb(d3.select(this).style("fill")).brighter();
                          });
                      });

    }
    vals = document.getElementById('fshow').elements

    show = []
    hide = []
    for(i = 0; i < 3; i++) {
      if (!vals[i].checked) {
        hide.push(vals[i])
      } else {
        show.push(vals[i])
      }
    }

    if (hide.length == 3) {
      d3.select('#feats').selectAll('rect').remove()
    } else if (hide.length == 2) {
      if (show[0].value == 'protag') {
        d3.selectAll('.fant').remove()
        d3.selectAll('.ffool').remove()
        d3.selectAll('.fprot').attr('height', fSegment - buffer/2)
      } else if (show[0].value == 'antag') {
        d3.selectAll('.fprot').remove()
        d3.selectAll('.ffool').remove()
        d3.selectAll('.fant')//.attr('transform', 'translate(0,' + ( - fSegment/3) + ')')
          .attr('height', fSegment - buffer/2)
          .attr('y', function() {
            blah = (d3.select(this).attr('y'))
            return (blah - fSegment/3)
          })
      } else {
        d3.selectAll('.fprot').remove()
        d3.selectAll('.fant').remove()
        d3.selectAll('.ffool')//.attr('transform', 'translate(0,' + ( - 2 * fSegment/3) + ')')
                  .attr('height', fSegment - buffer/2)
                  .attr('y', function() {
                    blah = (d3.select(this).attr('y'))
                    return (blah - 2*fSegment/3)
                  })
      }
    } else if (hide.length == 1) {
      if (hide[0].value == 'protag') {
        d3.selectAll('.fprot').remove()
        d3.selectAll('.fant')//.attr('transform', 'translate(0,' + ( - fSegment/3) + ')')
                  .attr('height', fSegment/2 - buffer/2)
                  .attr('y', function() {
                    blah = (d3.select(this).attr('y'))
                    return (blah - fSegment/3)
                  })
        d3.selectAll('.ffool')//.attr('transform', 'translate(0,'+(- fSegment/6)+')')
                  .attr('height', fSegment/2 - buffer/2)
                  .attr('y', function() {
                    blah = (d3.select(this).attr('y'))
                    return (blah - fSegment/6)
                  })
      } else if (hide[0].value == 'antag') {
        d3.selectAll('.fant').remove()
        d3.selectAll('.fprot').attr('height', fSegment/2 - buffer/2)
        d3.selectAll('.ffool')//.attr('transform', 'translate(0,'+(- fSegment/6)+')')
                  .attr('height', fSegment/2 - buffer/2)
                  .attr('y',function() {
                    blah = (d3.select(this).attr('y'))
                    return (blah - fSegment/6)
                  })
      } else {
        d3.selectAll('.ffool').remove()
        d3.selectAll('.fant')//.attr('transform', 'translate(0,' + ( + fSegment/6) + ')')
                  .attr('height', fSegment/2 - buffer/2)
                  .attr('y', function() {
                    blah = (d3.select(this).attr('y'))
                    return (parseFloat(blah) + fSegment/6)
                  })
        d3.selectAll('.fprot').attr('height', fSegment/2 - buffer/2)
      }
    }

    // if (!vals[0].checked){
    //   // d3.selectAll('.fprot').remove()
    //   d3.selectAll('.fprot').style('visibility','hidden')
    // } if (!vals[1].checked){
    //   // d3.selectAll('.fant').remove()
    //   d3.selectAll('.fant').style('visibility','hidden')
    // } if (!vals[2].checked){
    //   // d3.selectAll('.ffool').remove()
    //   d3.selectAll('.ffool').style('visibility','hidden')
    // }

    for (var i = 0; i < phonemes.length; i++) {
      var phon_bars =   d3.select('#'+phonemes[i])
                      .selectAll('rect')
                      .data(obj = pdata[phonemes[i]])
                      .enter()
                      .append('rect')
                      .property('id', function(d, j) {
                        if (j == 0) {
                          return phonemes[i] + '_prot';
                        } else if (j == 1) {
                          return phonemes[i] + '_ant';
                        } else {
                          return phonemes[i] + '_fool';
                        }
                      })
                      .attr('x', function (d) {
                          if (d > 0) {
                            return pos = '75.5%';
                          } else {
                            // norm = 1+d;
                            // pos = 25 * (norm) + 50;
                            pos = phonScale(d3.max([-2, d]))
                            return pos.toString()+'%'
                          }
                        })
                      .attr('y', function(d, j) { return i * pSegment + j * pSegment / 3 + buffer * 1.25; })
                      .attr('width', function(d) {
                        if (d > 0) {
                          pos = phonScale(d3.min([2, d])) - 75.5;
                        // pos = Math.abs(d * 25)
                        } else {
                          pos = 75.5 - Math.abs(phonScale(d3.max([-2, d])));
                        }
                        return (pos.toString()+'%');
                      })
                      .attr('height', pSegment / 3 - buffer / 2)
                      .attr('class', function (d, j) {
                        if (j == 0) {
                          return 'pprot';
                        } else if (j == 1) {
                          return 'pant';
                        } else {
                          return 'pfool';
                        }
                      })
                      // .style('fill', function(d, j) {
                      //   if (j == 0) {
                      //     // if (d < 0) {
                      //     //   return '#9216B2';
                      //     // } else {
                      //       return '#E68BFF';
                      //     // }
                      //   } else if (j == 1) {
                      //     // if (d < 0) {
                      //     //   return '#034F34';
                      //     // } else {
                      //       return '#3ECC97';
                      //     // }
                      //   } else {
                      //     // if (d < 0) {
                      //     //   return '7F6118';
                      //     // } else {
                      //       return '#FFDB83';
                          // }
                        // }
                      // })
                      // .style('stroke', function(d) {
                      //   if (d < 0) {
                      //     return 'red';
                      //   } else {
                      //     return 'black'
                      //   }
                      // })
                      .on("mouseover", function(d){
                          d3.select(this).style("fill", d3.rgb(d3.select(this).style("fill")).darker());
                          tip.show(d);
                      })
                      .on("mouseout", function(d){
                          tip.hide(d);
                          d3.select(this).style("fill", function() {
                              return d3.rgb(d3.select(this).style("fill")).brighter();
                          });
                      });
    }

    vals = document.getElementById('pshow').elements

    show = []
    hide = []
    for(i = 0; i < 3; i++) {
      if (!vals[i].checked) {
        hide.push(vals[i])
      } else {
        show.push(vals[i])
      }
    }

    if (hide.length == 3) {
      d3.select('#phons').selectAll('rect').remove()
    } else if (hide.length == 2) {
      if (show[0].value == 'protag') {
        d3.selectAll('.pant').remove()
        d3.selectAll('.pfool').remove()
        d3.selectAll('.pprot').attr('height', pSegment - buffer/2)
      } else if (show[0].value == 'antag') {
        d3.selectAll('.pprot').remove()
        d3.selectAll('.pfool').remove()
        d3.selectAll('.pant').attr('transform', 'translate(0,' + ( - pSegment/3) + ')').attr('height', pSegment - buffer/2)
      } else {
        d3.selectAll('.pprot').remove()
        d3.selectAll('.pant').remove()
        d3.selectAll('.pfool').attr('transform', 'translate(0,' + ( - 2 * pSegment/3) + ')').attr('height', pSegment - buffer/2)
      }
    } else if (hide.length == 1) {
      if (hide[0].value == 'protag') {
        d3.selectAll('.pprot').remove()
        d3.selectAll('.pant').attr('transform', 'translate(0,' + ( - pSegment/3) + ')').attr('height', pSegment/2 - buffer/2)
        d3.selectAll('.pfool').attr('transform', 'translate(0,'+(- pSegment/6)+')').attr('height', pSegment/2 - buffer/2)
      } else if (hide[0].value == 'antag') {
        d3.selectAll('.pant').remove()
        d3.selectAll('.pprot').attr('height', pSegment/2 - buffer/2)
        d3.selectAll('.pfool').attr('transform', 'translate(0,'+(- pSegment/6)+')').attr('height', pSegment/2 - buffer/2)
      } else {
        d3.selectAll('.pfool').remove()
        d3.selectAll('.pant').attr('transform', 'translate(0,' + ( + pSegment/6) + ')').attr('height', pSegment/2 - buffer/2)
        d3.selectAll('.pprot').attr('height', pSegment/2 - buffer/2)
      }
    }
    // pvals = document.getElementById('pshow').elements
    // if (!pvals[0].checked){
    //   d3.selectAll('.pprot').remove()
    // } if (!pvals[1].checked){
    //   d3.selectAll('.pant').remove()
    // } if (!pvals[2].checked){
    //   d3.selectAll('.pfool').remove()
    // }
    compare();
  })
}
function compare() {

  if (document.getElementById('fCharacter').value != 'default') {

    var dataURL = '/compare/'+document.getElementById('fCharacter').value
    d3.json(dataURL, function(error, data){

      if (data.length != 0) {
          var feat_data = data['features']
      }

      for (var i = 0; i < features.length; i++) {
        d3.select('#'+features[i]).selectAll('.fprot_bar').remove();
        d3.select('#'+features[i]).selectAll('.fant_bar').remove();
        d3.select('#'+features[i]).selectAll('.ffool_bar').remove();


        if (feat_data.length != 0){
          if(document.getElementById(features[i]+'_prot')) {
            var fprot_pos = document.getElementById(features[i]+'_prot').getAttribute('x')
            fprot_pos = parseFloat(fprot_pos)
          }
          if (document.getElementById(features[i]+'_ant')) {
            var fant_pos = document.getElementById(features[i]+'_ant').getAttribute('x')
            fant_pos = parseFloat(fant_pos)
          }
          if (document.getElementById(features[i]+'_fool')) {
            var ffool_pos = document.getElementById(features[i]+'_fool').getAttribute('x')
            ffool_pos = parseFloat(ffool_pos)
          }

          if (feat_data[features[i]] > 0) {
            pos = featScale(d3.min([2, feat_data[features[i]]]));
          } else {
            pos = featScale(d3.max([-2, feat_data[features[i]]]));
          }

          if(document.getElementById(features[i]+'_prot')) {
            var fprot_rect = d3.select('#'+features[i])
                          .append('rect')
                          .property('id', document.getElementById('fCharacter').value)
                          .attr('class', 'fprot_bar')
                          .attr('x', function() {
                            if (fprot_pos != 25) { //bar negative
                              if (pos - fprot_pos > 0) { //char >bar
                                start = fprot_pos; //bar
                              } else {
                                start = pos; //char
                              }
                            } else { //bar positive
                              width = parseFloat(document.getElementById(features[i]+'_prot').getAttribute('width'))
                              if (pos - (fprot_pos + width) > 0) { //char > bar
                                start = fprot_pos + width; //bar + width
                              } else { //char < bar
                                start = pos; //char
                              }
                            }
                            return start.toString()+'%';
                          })
                          .attr('y', function() {
                            return ugh = document.getElementById(features[i]+'_prot').getAttribute('y');
                          })
                          .attr('width',  function() {
                            fprotextra = parseFloat(document.getElementById(features[i]+'_prot').getAttribute('width'))
                            if (fprot_pos == 25) { //bar pos
                              if (pos > 25 + fprotextra) { //char > bar
                                fprot_width = pos - (25  + fprotextra) //char - (bar+width)
                              } else { //bar > char
                                fprot_width = 25 + fprotextra - pos
                              }
                            } else { //bar neg
                              fprot_width = Math.abs(pos-fprot_pos)
                            }
                            return foo = fprot_width.toString()+'%';
                          })
                          .attr('height', function() {
                          return bar = document.getElementById(features[i]+'_prot').getAttribute('height');
                          })
                          .style('stroke', 'black')
                          .style('opacity', '0.5')
                          .style('fill', 'blue')
                          // .style('fill', function() {
                          //   if (fprot_pos != 25) {
                          //     if (pos - fprot_pos > 0) {
                          //       return('blue');
                          //     } else {
                          //       return('red');
                          //     }
                          //   } else {
                          //     if (pos - fprot_pos > 0) {
                          //       return('blue');
                          //     } else {
                          //       return('red');
                          //     }
                          //   }
                          // });
                          // .style('stroke', function(){
                          //   if (feat_data[features[i]] < 0) {
                          //     return 'red';
                          //   } else {
                          //     return 'black';
                          //   }
                          // })
          }
          if(document.getElementById(features[i]+'_ant')) {
            var fant_rect = d3.select('#'+features[i])
                        .append('rect')
                        .property('id', document.getElementById('fCharacter').value)
                        .attr('class', 'fant_bar')
                        .attr('x', function() {
                          if (fant_pos != 25) { //bar negative
                            if (pos - fant_pos > 0) { //char >bar
                              start = fant_pos; //bar
                            } else {
                              start = pos; //char
                            }
                          } else { //bar positive
                            width = parseFloat(document.getElementById(features[i]+'_ant').getAttribute('width'))
                            if (pos - (fant_pos + width) > 0) { //char > bar
                              start = fant_pos + width; //bar + width
                            } else { //char < bar
                              start = pos; //char
                            }
                          }
                          return start.toString()+'%';
                        })
                        .attr('y', function() {
                          return baz = document.getElementById(features[i]+'_ant').getAttribute('y');
                        })
                        .attr('width',  function() {
                          fantextra = parseFloat(document.getElementById(features[i]+'_ant').getAttribute('width'))
                          if (fant_pos == 25) { //bar pos
                            if (pos > 25 + fantextra) { //char > bar
                              fant_width = pos - (25  + fantextra) //char - (bar+width)
                            } else { //bar > char
                              fant_width = 25 + fantextra - pos
                            }
                          } else { //bar neg
                            fant_width = Math.abs(pos-fant_pos)
                          }
                          return fant_width.toString()+'%';
                        })
                        .attr('height', function() {
                        return document.getElementById(features[i]+'_ant').getAttribute('height');
                        })
                        .style('stroke', 'black')
                        .style('opacity', '0.5')
                        .style('fill', 'blue')
          }
          if(document.getElementById(features[i]+'_fool')) {
            var ffool_rect = d3.select('#'+features[i])
                        .append('rect')
                        .property('id', document.getElementById('fCharacter').value)
                        .attr('class', 'ffool_bar')
                        .attr('x', function() {
                          if (ffool_pos != 25) { //bar negative
                            if (pos - ffool_pos > 0) { //char >bar
                              start = ffool_pos; //bar
                            } else {
                              start = pos; //char
                            }
                          } else { //bar positive
                            width = parseFloat(document.getElementById(features[i]+'_fool').getAttribute('width'))
                            if (pos - (ffool_pos + width) > 0) { //char > bar
                              start = ffool_pos + width; //bar + width
                            } else { //char < bar
                              start = pos; //char
                            }
                          }
                          return start.toString()+'%';
                        })
                        .attr('y', function() {
                          return document.getElementById(features[i]+'_fool').getAttribute('y');
                        })
                        .attr('width',  function() {
                          ffoolextra = parseFloat(document.getElementById(features[i]+'_fool').getAttribute('width'))
                          if (ffool_pos == 25) { //bar pos
                            if (pos > 25 + ffoolextra) { //char > bar
                              ffool_width = pos - (25  + ffoolextra) //char - (bar+width)
                            } else { //bar > char
                              ffool_width = 25 + ffoolextra - pos
                            }
                          } else { //bar neg
                            ffool_width = Math.abs(pos-ffool_pos)
                          }
                          return ffool_width.toString()+'%';
                        })
                        .attr('height', function() {
                        return document.getElementById(features[i]+'_fool').getAttribute('height');
                        })
                        .style('stroke', 'black')
                        .style('opacity', '0.5')
                        .style('fill', 'blue')
          }
        }
      }
    })
  }

  if (document.getElementById('pCharacter').value != 'default') {

    var dataURL = '/compare/'+document.getElementById('pCharacter').value
    d3.json(dataURL, function(error, data){

      if (data.length != 0) {
          var phon_data = data['phonemes']
      }

      for (var i = 0; i < phonemes.length; i++) {
        d3.select('#'+phonemes[i]).selectAll('line').remove();

        if (phon_data.length != 0){
          var phon_line = d3.select('#'+phonemes[i])
                        .append('line')
                        .property('id', document.getElementById('pCharacter'.value))
                        .attr('x1', function() {
                          if (phon_data[phonemes[i]] > 0) {
                            pos = phonScale(d3.min([2, phon_data[phonemes[i]]]))
                          } else {
                            pos = phonScale(d3.max([-2, phon_data[phonemes[i]]]))
                          }
                          return pos.toString()+'%'
                        })
                        .attr('x2', function() {
                          if (phon_data[phonemes[i]] > 0) {
                            pos = phonScale(d3.min([2, phon_data[phonemes[i]]]))
                          } else {
                            pos = phonScale(d3.max([-2, phon_data[phonemes[i]]]))
                          }
                          return pos.toString()+'%'
                        })
                        .attr('y1',  buffer + (pSegment * i))
                        .attr('y2', buffer + (pSegment * (i + 1)))
                        .style('stroke', 'black');
                        // .style('stroke', function(){
                        //   if (phon_data[phonemes[i]] < 0) {
                        //     return 'red';
                        //   } else {
                        //     return 'black';
                        //   }
                        // })
        }
      }
    })
  }
}

function sortOrder() {
  var dataURL = '/data'

  d3.json(dataURL, function(error, data){
    var unordered_fdata = data['features']
    var unordered_pdata = data['phonemes']
    var new_fdat = []
    var new_pdat = []
    for (var i = 0; i < features.length; i++) {
      var currFeat = features[i]
      var z_vals = unordered_fdata[currFeat]
      var new_ftuple


      if (document.getElementById('f_psort').checked) {
          new_ftuple = [Math.abs(z_vals[0]),  currFeat]

      } else if (document.getElementById('f_asort').checked) {
          new_ftuple = [Math.abs(z_vals[1]), currFeat]

      } else {
          new_ftuple = [Math.abs(z_vals[2]), currFeat]
      }
      new_fdat.push(new_ftuple)
    }
    for (var i = 0; i < phonemes.length; i++) {
      var currPhon = phonemes[i]
      var z_vals = unordered_pdata[currPhon]
      var new_ptuple


      if (document.getElementById('p_psort').checked) {
          new_ptuple = [Math.abs(z_vals[0]),  currPhon]

      } else if (document.getElementById('p_asort').checked) {
          new_ptuple = [Math.abs(z_vals[1]), currPhon]

      } else {
          new_ptuple = [Math.abs(z_vals[2]), currPhon]
      }
      new_pdat.push(new_ptuple)
    }

    new_fdat.sort(sortFunction);
    new_pdat.sort(sortFunction);

    function sortFunction(a, b) {
        if (a[0] === b[0]) {
            return 0;
        }
        else {
            return (a[0] < b[0]) ? -1 : 1;
        }
    }
    var new_features = []
    var new_phonemes = []
    for (var j = new_fdat.length - 1; j >= 0; j--) {
      new_features.push(new_fdat[j][1])
    }
    for (var j = new_pdat.length - 1; j >= 0; j--) {
      new_phonemes.push(new_pdat[j][1])
    }
    features = new_features
    phonemes = new_phonemes
    onLoad();
  })
}


// var tip = d3.tip()
//   .attr('class', 'd3-tip')
//   .offset([-10, 0])
//   .html(function(d) {
//     return "<strong>"+d+"</strong>";
//   })
//
//   svg.call(tip);
