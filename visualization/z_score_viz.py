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

@app.route('/data')
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

    phonemes = {'AA':[], 'AE':[], 'AH':[], 'AO':[], 'AW':[], 'AY':[], 'B':[], 'CH':[],
    'D':[], 'DH':[], 'EH':[], 'ER':[], 'EY':[], 'F':[], 'G':[], 'HH':[], 'IH':[],
    'IY':[], 'JH':[], 'K':[], 'L':[], 'M':[], 'N':[], 'NG':[], 'OW':[], 'OY':[],
    'P':[], 'R':[], 'S':[], 'SH':[], 'T':[], 'TH':[], 'UH':[], 'UW':[], 'V':[],
    'W':[], 'Y':[], 'Z':[], 'ZH':[]}

    with open('../classifier/phoneme_z_scores.csv', 'r') as phonfile:
        reader = csv.reader(phonfile)
        for row in reader:
            if row[0] != 'phoneme':
                for i in range(1, 4):
                    phonemes[row[0]].append(float(row[i]))

    ret = {'features':features, 'phonemes':phonemes}
    return flask.jsonify(ret)

@app.route('/compare/<char>')
def comparison_value(char):

    if char == 'reset':
        return flask.jsonify({'features':[], 'phonemes':[]})

    feat_dict = {}
    phon_dict = {}
    with open('../tagging/features/percentData.csv', 'r') as feat_file:
        freader = csv.DictReader(feat_file)
        for frow in freader:
            if frow['filename'] == char:
                for feature in frow:
                    if feature != 'filename':
                        char_feat_value = float(frow[feature])
                        with open('../stats/feature_statistics.csv', 'r') as fstats:
                            fsreader = csv.reader(fstats)
                            for statrow in fsreader:
                                if statrow[0] == feature:
                                    z_val = (char_feat_value - float(statrow[1]))/float(statrow[2])
                                    feat_dict[feature] = z_val
                                    break

    with open('../tagging/phonemefreq/masterData.csv', 'r') as phon_file:
        preader = csv.DictReader(phon_file)
        for prow in preader:
            if prow['filename'] == char:
                for phoneme in prow:
                    if phoneme != 'filename':
                        char_phon_value = float(prow[phoneme])
                        with open('../stats/phoneme_statistics.csv', 'r') as pstats:
                            psreader = csv.reader(pstats)
                            for statrow in psreader:
                                if statrow[0] == phoneme:
                                    z_val = (char_phon_value - float(statrow[1]))/float(statrow[2])
                                    phon_dict[phoneme] = z_val
                                    break

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

#testing port is 5100
if __name__ == "__main__":
    app.run(debug=True)
