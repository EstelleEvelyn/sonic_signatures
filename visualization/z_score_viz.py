import flask
import json
import urllib
import csv
import os
import re

app = flask.Flask(__name__)

@app.route("/")
def default():
    return flask.render_template("z_score.html")

@app.route('/feature_data')
def data_load():
    features = {'fricative':[], 'affricate':[], 'glide':[], 'nasal':[], 'liquid':[],
        'stop':[], 'glottal':[], 'linguaalveolar':[], 'linguapalatal':[], 'labiodental':[],
        'bilabial':[], 'linguavelar':[], 'linguadental':[], 'voiced':[], 'voiceless':[],
        'sibilant':[], 'nonsibilant':[], 'sonorant':[], 'nonsonorant':[], 'coronal':[],
        'noncoronal':[], 'monophthong':[], 'diphthong':[], 'central':[], 'front':[], 'back':[],
        'tense':[], 'lax':[], 'rounded':[], 'unrounded':[]}
    with open('../classifier/feature_z_scores.csv', 'r') as featfile:
        reader = csv.reader(featfile)
        for row in reader:
            if row[0] != 'feature':
                for i in range(1, 4):
                    features[row[0]].append(float(row[i]))
    return flask.jsonify(features)

@app.route('/compare/<char>')
def comparison_value(char):
    if char == 'default':
        return flask.jsonify([])
    feat_dict = {}
    phon_dict = {}
    with open('../tagging/features/percentData.csv', 'r') as feat_file:
        freader = csv.DictReader(feat_file)
        for frow in freader:
            if frow['filename'] == char:
                for feature in frow:
                    if feature != 'filename':
                        feat_dict[feature] = float(frow[feature])
    with open('../tagging/phonemefreq/masterData.csv', 'r') as phon_file:
        preader = csv.DictReader(phon_file)
        for prow in preader:
            if prow['filename'] == char:
                for phoneme in prow:
                    if phoneme != 'filename':
                        phon_dict[phoneme] = float(prow[phoneme])
    ret_dict = {'features':feat_dict, 'phonemes':phon_dict}
    return flask.jsonify(ret_dict)

@app.route('/options/<play>')
def list_options(play):
    '''
    Returns the list of characters in a given play
    '''
    character_list = []
    if play == 'default':
        return flask.jsonify(['Character'])
    for fn in os.listdir("../tagging/dest"):
        if re.match(play+"_", fn) is not None:
            lstrip_length = len(play)+1
            character = fn[lstrip_length:-4]
            character_list.append(character)
    character_list.sort()
    return flask.jsonify(character_list)

if __name__ == "__main__":
    app.run(debug=True)
