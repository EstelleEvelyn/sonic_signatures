from flask import Flask, render_template, jsonify, request
import random
import sys
app = Flask(__name__)

@app.route('/')
def tacos():
    return render_template("tacos.html")

@app.route('/pronunciationData/')
def pronunciation_data():
    if request.method == 'POST':
        return redirect(url_for('pronunciation_data'))

    return render_template("aboutdata.html")

@app.route('/testHTML/')
def test_html():
    htmlStr = '<html lang="en">' + \
        '<head>' + \
        '  <title>My Page</title>' + \
        '</head>' + \
        '<body>' + \
        '  <h1>Welcome to CS 314</h1>' + \
        '  <p>We make pretty pictures!</p>' + \
        '</body>' + \
        '</html>'
    return htmlStr

if __name__=='__main__':
    if len(sys.argv) != 3:
        app.run(debug=True)
    else:
        host = sys.argv[1]
        port = sys.argv[2]
        app.run(host=host, port=port)
