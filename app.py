#!/usr/bin/env python3
from flask import Flask, render_template
from database import db_session
from models import Flow, Partner, Site, FlowTemplate
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

@app.route("/partners")
def list_partners():
    partners = Partner.query.filter(Partner.id < 50 )
    return render_template("partners_list.html",app_data=app_data, partners=partners)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, host="0.0.0.0")
