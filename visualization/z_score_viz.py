import flask
import json
import urllib
import csv

app = flask.Flask(__name__)

@app.route("/")
def default():
    return flask.render_template("z_score.html")

@app.route("/load")
def get_zzz():
    ret_list = {}
    with open("../classifier/phoneme_z_scores.csv") as source:
        read = csv.DictReader(source)
        for row in read:
            ret_list[row.get('phoneme')] = float(row.get('protag'))
    return flask.jsonify(ret_list)


if __name__ == "__main__":
    app.run(debug=True)
