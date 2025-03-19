from flask import Flask, render_template
from model.demo import format_date, generate_greeting
import datetime
app = Flask(__name__)



@app.route("/")
def hello_world():
    today = datetime.datetime.now()
    return f"Hôm nay là {format_date(today)}. {generate_greeting('Tuyet')}"

@app.route("/person/<name>")
def hello(name=None):
    return render_template('hello.html', person=name)

if __name__ == '__main__':
    app.run(debug=True)
