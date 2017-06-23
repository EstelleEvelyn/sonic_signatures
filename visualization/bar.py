import sys
import flask
import json
import urllib
import csv
import os
import re


app = flask.Flask(__name__)
@app.route('/')
def default():
    return flask.render_template('bar_chart_depiction.html')

@app.route('/data/<char1>+<char2>+<char3>')
def create_data(char1, char2, char3):

    manner_data = [{},{},{}]
    placement_data = [{},{},{}]
    voice_data = [{},{},{}]

    manner_keys = ['stop', 'affricate', 'fricative', 'liquid', 'glide', 'nasal']
    placement_keys = ['bilabial', 'linguaalveolar', 'linguadental', 'labiodental', 'linguavelar', 'glottal', 'linguapalatal']
    voice_keys = ['voiced', 'voiceless']

    manner_data[0]['character'] = char1
    manner_data[1]['character'] = char2
    manner_data[2]['character'] = char3

    placement_data[0]['character'] = char1
    placement_data[1]['character'] = char2
    placement_data[2]['character'] = char3
    
    voice_data[0]['character'] = char1
    voice_data[1]['character'] = char2
    voice_data[2]['character'] = char3

    for i in range(3):
        manner_data[i]['total'] = 100
        placement_data[i]['total'] = 100
        voice_data[i]['total'] = 100

    with open('../tagging/features/percentData.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row.get('filename') == char1:
                for m_key in manner_keys:
                    manner_data[0][m_key] = row.get(m_key)
                for p_key in placement_keys:
                    placement_data[0][p_key] = row.get(p_key)
                for v_key in voice_keys:
                    voice_data[0][v_key] = row.get(v_key)

            if row.get('filename') == char2:
                for m_key in manner_keys:
                    manner_data[1][m_key] = row.get(m_key)
                for p_key in placement_keys:
                    placement_data[1][p_key] = row.get(p_key)
                for v_key in voice_keys:
                    voice_data[1][v_key] = row.get(v_key)

            if row.get('filename') == char3:
                for m_key in manner_keys:
                    manner_data[2][m_key] = row.get(m_key)
                for p_key in placement_keys:
                    placement_data[2][p_key] = row.get(p_key)
                for v_key in voice_keys:
                    voice_data[2][v_key] = row.get(v_key)

    return flask.jsonify({'manner':manner_data, 'placement':placement_data, 'voice':voice_data})

@app.route('/options/<play>')
def list_options(play):
    character_list = []
    for fn in os.listdir("../tagging/dest"):
        if re.match(play+"_", fn) is not None:
            lstrip_length = len(play)+1
            character = fn[lstrip_length:-4]
            character_list.append(character)
    character_list.sort()
    return flask.jsonify(character_list)

if __name__=='__main__':
    app.run(debug=True)
