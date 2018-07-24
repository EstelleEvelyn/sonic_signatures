from flask import Flask, render_template, jsonify, request
import sys

app = Flask(__name__)

@app.route('/')
def tacos():
    return render_template("tacos.html")

@app.route('/pronunciationData/')
def pronunciation_data():
    return render_template("aboutdata.html")

if __name__=='__main__':
    if len(sys.argv) not in [3,4]:
        app.run(debug=True)
    else:
        host = sys.argv[1]
        port = sys.argv[2]
        if len(sys.argv) == 4 and sys.argv[3] == 'debug':
            app.run(host=host, port=int(port), debug=True)
        else:
            app.run(host=host, port=port)