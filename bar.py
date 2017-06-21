import sys
import flask
import json
import api_config
import psycopg2
import urllib

app = flask.Flask(__name__)
@app.route('/')
def default():
    return render_template('bar_chart_depiction.html')

@app.route('/data/<char1>+<char2>+<char3>')
def create_data(char1, char2, char3):

    manner_data = [{},{},{}]
    placement_data = [{},{},{}]
    voice_data = [{},{},{}]


    files = [[],[],[]]

    files[0][0] = "features/{}_manner.csv".format(char1)
    files[0][1] = "features/{}_manner.csv".format(char2)
    files[0][2] = "features/{}_manner.csv".format(char3)

    files[1][0] = "features/{}_placement.csv".format(char1)
    files[1][1] = "features/{}_placement.csv".format(char2)
    files[1][2] = "features/{}_placement.csv".format(char3)

    files[2][0] = "features/{}_voice.csv".format(char1)
    files[2][1] = "features/{}_voice.csv".format(char2)
    files[2][2] = "features/{}_voice.csv".format(char3)

    manner_data[0]['character'] = char1
    manner_data[1]['character'] = char2
    manner_data[2]['character'] = char3

    placement_data[0]['character'] = char1
    placement_data[1]['character'] = char2
    placement_data[2]['character'] = char3

    voice_data[0]['character'] = char1
    voice_data[1]['character'] = char2
    voice_data[2]['character'] = char3

    for i in range(2):
        manner_data[i]['total'] = 100
        placement_data[i]['total'] = 100
        voice_data[i]['total'] = 100

    for j in range(2):
        with open(files[0][j]) as manner_file:
            manner_reader = csv.DictReader(manner_file)
            for m_row in manner_reader:
                manner_data[m_row.get('feature')] = m_row.get('percent')

        with open(files[1][j]) as placement_file:
            placement_reader = csv.DictReader(placement_file)
            for p_row in placement_reader:
                placement_data[p_row.get('feature')] = p_row.get('percent')

        with open(files[2][j]) as voice_file:
            voice_reader = csv.DictReader(voice_file)
            for v_row in voice_reader:
                voice_data[v_row.get('feature')] = v_row.get('percent')

    return jsonify({'manner':manner_data, 'placement':placement_data, 'voice':voice_data})

if __name__=='__main__':
    app.run(debug=True)
