from flask import Flask, render_template

app = Flask(__name__)

hello_target = "Hello world"


@app.route("/")
def hello():
    return render_template("index.html", target=hello_target)


if __name__ == "__main__":
    app.run(debug=True)