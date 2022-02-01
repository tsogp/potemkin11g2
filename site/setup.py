from flask import *

app = Flask(__name__)

@app.route('/')
def setup():
    return redirect('/index')

@app.route('/index')
def render_index():
    return render_template("index.html")

@app.route('/catalogue')
def render_catalogue():
    return render_template("catalogue.html")

@app.route('/coffee')
def render_coffee():
    return render_template("coffee.html")

@app.route('/arabica')
def render_arabica():
    return render_template("arabica.html")

@app.route('/liberica')
def render_liberica():
    return render_template("liberica.html")

@app.route('/robusta')
def render_robusta():
    return render_template("robusta.html")

app.run(debug=True)