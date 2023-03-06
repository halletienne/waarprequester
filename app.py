#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from database import db_session
from markupsafe import escape
from models import Flow, Partner, Site, FlowTemplate, PartnerRequest, FlowRequest, FlowTemplate
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
    flow_count = Flow.query.count()
    partner_count = Partner.query.count()
    flow_request_count = FlowRequest.query.count()
    partner_request_count = PartnerRequest.query.count()
    return render_template("index.html",app_data=app_data, flow_count=flow_count, partner_count=partner_count, flow_request_count=flow_request_count, partner_request_count=partner_request_count)
    

#  Listing
## Flows listing
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

## Partners listing
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


## Requests listing
@app.route("/requests")
def show_requests():
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

    existing_partners = Partner.query.all()
    existing_partners_results = [
              {
                  "waarp_id": partner.waarp_id,
                  "site": partner.site,
                  "type": partner.type,
                  "isClient": partner.isClient,
                  "isServer": partner.isServer,
                  "description": partner.description,
                  "hostid": partner.hostid,
                  "hostidssl": partner.hostidssl
                  } for partner in existing_partners]

    return render_template("requests_list.html", app_data=app_data, partner_requests=partner_request_results, flow_requests=flow_request_results, partners=existing_partners_results)


# Creation Form
## Flow Request Form
@app.route("/flow_request_form", methods=['GET', 'POST'])
def flow_request_creation():
    # Extract available templates
    flow_templates = FlowTemplate.query.all()
    flow_templates_results = [
              {
                  "waarp_id": flow_template.waarp_id,
                  "name": flow_template.name
                  } for flow_template in flow_templates]

    # Extract all available partners
    partners = Partner.query.filter()
    partner_results = [
              {
                  "waarp_id": partner.waarp_id,
                  "hostid": partner.hostid,
                  }for partner in partners]

    # Extract requested partners
    partners_requested = PartnerRequest.query.filter()
    partner_requested_results = [
              {
                  "id": partner.id,
                  "hostid": partner.hostid,
                  }for partner in partners_requested]

    if request.method == 'POST': 
        # Prcess FlowRequest Creation
        flow_requested={
            'flowname': request.form['flowname'],
            'template': request.form['flowtemplate'],
            'description': request.form['description'],
            'origin': request.form['origin'],
            'originDir': request.form['origindir'],
            }
        if request.form.get('filewatcher'):
            flow_requested['filewatcher'] = True
        else:
            flow_requested['filewatcher'] = False

        if request.form.get('isActive'):
            flow_requested['isActive'] = True
        else:
            flow_requested['isActive'] = False

        fr = FlowRequest(flow_requested['flowname'],flow_requested['isActive'],flow_requested['template'],flow_requested['origin'],flow_requested['originDir'],flow_requested['description'],flow_requested['filewatcher'])
        db_session.add(fr)
        db_session.commit()
        return render_template("flow_request_creation.html", app_data=app_data, flow_requested=flow_requested, flow_templates=flow_templates_results, partners=partner_results, partners_requested=partner_requested_results)

    else:
        return render_template("flow_request_creation.html", app_data=app_data, flow_templates=flow_templates_results, partners=partner_results, partners_requested=partner_requested_results)

## Partner request form
@app.route("/partner_request_form", methods=['GET', 'POST'])
def partner_request_creation():
    sites = Site.query.all()
    site_results = [
              {
                  "waarp_id": site.waarp_id,
                  "name": site.name,
                  "description": site.description
                  } for site in sites]
    if request.method == 'POST': 
        partner_requested={
            'site': request.form['site'],
            'type': request.form['type'],
            'description': request.form['description'],
            'hostid': request.form['hostid'],
            'hostidssl': request.form['hostidssl']
            }
        if request.form.get('isClient'):
            partner_requested['isClient'] = True
        else:
            partner_requested['isClient'] = False

        if request.form.get('isServer'):
            partner_requested['isServer'] = True
        else:
            partner_requested['isServer'] = False

        pr = PartnerRequest(partner_requested['site'],partner_requested['type'],partner_requested['isClient'],partner_requested['isServer'],partner_requested['description'],partner_requested['hostid'],partner_requested['hostidssl'])
        db_session.add(pr)
        db_session.commit()

        return render_template("partner_request_creation.html", app_data=app_data, partner_requested=partner_requested,site_results=site_results)
    else:
        return render_template("partner_request_creation.html", app_data=app_data,site_results=site_results)

# Detail
## Partner
@app.route("/partner/<int:waarp_id>")
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

# Show Request detail
## Flow request detail
@app.route("/flow_request_detail/<int:flowrequest_id>")
def flow_request_detail(flowrequest_id):
    safe_id = escape(flowrequest_id)
    flowrequest_query = FlowRequest.query.filter(FlowRequest.id == safe_id).first()
    flowrequest = {
                  "request_id": flowrequest_query.id,
                  "name": flowrequest_query.name,
                  "active": flowrequest_query.active,
                  "template": flowrequest_query.template,
                  "origin": flowrequest_query.origin,
                  "originDir": flowrequest_query.originDir,
                  "description": flowrequest_query.description,
                  "filewatcher": flowrequest_query.filewatcher
                  }
    return render_template("flow_request_detail.html", app_data=app_data, flowrequest=flowrequest)


## Flow request detail
@app.route("/partner_request_detail/<int:partnerrequest_id>")
def partner_request_detail(partnerrequest_id):
    safe_id = escape(partnerrequest_id)
    partnerrequest_query = PartnerRequest.query.filter(PartnerRequest.id == safe_id).first()
    partnerrequest = {
                  "request_id": partnerrequest_query.id,
                  "type": partnerrequest_query.type,
                  "site": partnerrequest_query.site,
                  "hostid": partnerrequest_query.hostid,
                  "hostidssl": partnerrequest_query.hostidssl,
                  "description": partnerrequest_query.description,
                  "isClient": partnerrequest_query.isClient,
                  "isServer": partnerrequest_query.isServer
                  }

    return render_template("partner_request_detail.html", app_data=app_data, partnerrequest=partnerrequest)


# Requests deletion
## Flow requests deletion
@app.route("/delete_flow_request/<int:flowrequest_id>")
def delete_flow_request(flowrequest_id):
    safe_id = escape(flowrequest_id)
    db_session.delete(FlowRequest.query.filter(FlowRequest.id == safe_id).first())
    db_session.commit()
    return redirect(url_for('show_requests'))


## Partner requests deletion
@app.route("/delete_partner_request/<int:partnerrequest_id>")
def delete_partner_request(partnerrequest_id):
    safe_id = escape(partnerrequest_id)
    db_session.delete(PartnerRequest.query.filter(PartnerRequest.id == safe_id).first())
    db_session.commit()
    return redirect(url_for('show_requests'))






    
@app.route("/info")
def show_info():
    return render_template('example.html', app_data=app_data)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, host="0.0.0.0")
