#!/usr/bin/env python3
from flask import Flask, render_template

DEVELOPMENT_ENV = True
app = Flask(__name__)


app_data = {
    "name": "Manutan Waarp Flow request system",
    "description": "Basic site to manage waarp flows",
    "author": "Manutan BT",
    "html_title": "Template for a Flask Web App",
    "project_name": "Waarp Requests",
    "keywords": "flask, webapp, template, basic, waarp",
}

@app.route("/")
def hello_world():
        return render_template("index.html",app_data=app_data)
    

@app.route("/flows")
def list_flows():
    return render_template("flow_list.html",app_data=app_data)


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, host="0.0.0.0")
