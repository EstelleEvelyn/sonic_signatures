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

@app.route('/options/<play>')
def list_options(play):
    '''
    Returns the list of characters in a given play
    '''
    character_list = []
    for fn in os.listdir("../tagging/dest"):
        if re.match(play+"_", fn) is not None:
            lstrip_length = len(play)+1
            character = fn[lstrip_length:-4]
            character_list.append(character)
    character_list.sort()
    return flask.jsonify(character_list)

if __name__ == "__main__":
    app.run(debug=True)
