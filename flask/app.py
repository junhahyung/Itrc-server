from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

client = MongoClient('localhost', 27017)
db = client["database"]
col = db["storage"]

@app.route('/', methods=['GET'])
def dropdown():
    colours = ['red', 'green', 'blue']
    dests = ['1','2', '3']
    return render_template('test.html', colours=colours, dests=dests)

@app.route("/json", methods=['POST'])
def add_num():
    color = request.form['colours']
    dest = request.form['dests']
    x = list(col.find({'dest': dest}))[0]
    return jsonify(x[color])
