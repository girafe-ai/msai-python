from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/json")
def json_example():
    return {
        'a': 1,
        'b': 2
    }


app.run(port=80)
