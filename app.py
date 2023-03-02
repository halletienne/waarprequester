#!/usr/bin/env python3
from flask import Flask, render_template
from database import db_session
from markupsafe import escape
from models import Flow, Partner, Site, FlowTemplate, PartnerRequest, FlowRequest
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
    flows = Flow.query.filter(Flow.waarp_id < 50 )
    partners = Partner.query.all()
    partner_linked = [
        {
            "waarp_id": partner.waarp_id,
            "hostid": partner.hostid
        } for partner in partners ]

    flow_results = [
              {
                  "waarp_id": flow.waarp_id,
                  "name": flow.name,
                  "description": flow.description,
                  "active": flow.active,
                  "origin": flow.origin
                  } for flow in flows]
    return render_template("flow_list.html",app_data=app_data, flows=flow_results, partners=partner_linked)

@app.route("/partners")
def list_partners():
    partners = Partner.query.filter(Partner.waarp_id < 50 )
    partner_results = [
              {
                  "waarp_id": partner.waarp_id,
                  "hostid": partner.hostid,
                  "hostidssl": partner.hostidssl,
                  "type": partner.type,
                  "description": partner.description,
                  "isClient": partner.isClient,
                  "isServer": partner.isServer
                  } for partner in partners]
    return render_template("partner_list.html",app_data=app_data, partners=partner_results)


@app.route("/requests")
def show_request():
    flow_requests = FlowRequest.query.all()

    flow_request_results = [
              {
                  "request_id": flow.id,
                  "name": flow.name,
                  "active": flow.active,
                  "template": flow.template,
                  "origin": flow.origin,
                  "originDir": flow.originDir,
                  "description": flow.description,
                  "filewatcher": flow.filewatcher
                  } for flow in flow_requests]

    partner_requests = PartnerRequest.query.all()

    partner_request_results = [
              {
                  "request_id": partner.id,
                  "site": partner.site,
                  "type": partner.type,
                  "isClient": partner.isClient,
                  "isServer": partner.isServer,
                  "description": partner.description,
                  "hostid": partner.hostid,
                  "hostidssl": partner.hostidssl
                  } for partner in partner_requests]

    return render_template("requests_list.html", app_data=app_data, partner_requests=partner_request_results, flow_requests=flow_request_results)

@app.route("/partner/<waarp_id>")
def show_partner(waarp_id):
    safe_id = escape(waarp_id)
    partner_query = Partner.query.filter(Partner.waarp_id == safe_id).first()
    partner = {
       "hostid": partner_query.hostid,
       "site": partner_query.site,
       "type": partner_query.type
       }
    flows = Flow.query.filter(Flow.origin == safe_id )
    flow_results = [
              {
                  "waarp_id": flow.waarp_id,
                  "name": flow.name,
                  "description": flow.description,
                  "active": flow.active,
                  "origin": flow.origin
                  } for flow in flows]
    return render_template('partner_detail.html', app_data=app_data, partner=partner, flows=flow_results)

    

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, host="0.0.0.0")
