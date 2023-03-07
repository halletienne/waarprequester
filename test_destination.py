#!/usr/bin/env python3
## This help import current Flows/Partners/Sites/FlowTemplates into the Flask DB

from waarp import WaarpHelper
import os
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import logging



logging.getLogger().setLevel(logging.ERROR)

engine = create_engine('sqlite:////tmp/test_newmodel_dest.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    print("DB Initialisation")
    Base.metadata.create_all(bind=engine)




## Real start of function
# Set default value for SSL verification
def waarp_connect():
    ssl_verify = True

    config_file_path = os.path.join(os.environ['HOME'], '.waarp.env')

    if os.path.exists(config_file_path):
        print('Reading info from config file')
        config = configparser.ConfigParser()
        config.read(config_file_path)
        if 'SERVER' in config['WAARP-MANAGER']:
          server = config['WAARP-MANAGER'].get('SERVER')
        if 'USERNAME' in config['WAARP-MANAGER']:
          username = config['WAARP-MANAGER'].get('USERNAME')
        if 'PASSWORD' in config['WAARP-MANAGER']:
          password = config['WAARP-MANAGER'].get('PASSWORD')
        if 'SSL_VERIFY' in config['WAARP-MANAGER']:
          if config['WAARP-MANAGER'].get('SSL_VERIFY').lower() in ["false", "0", "no"]:
            ssl_verify = False

    waarp = WaarpHelper(waarp_manager_addr=server, 
      waarp_manager_user=username,
      waarp_manager_passwd=password,
      ssl_verify=ssl_verify)

    return waarp


def populate_db(db_session, waarp):
    from models import Flow, Partner, Site, FlowTemplate, Destination
    ## This inventory need higher privilege
    #waarp.link_inventory()
    waarp.flow_inventory()
    for flow_name in waarp.flows:
        print('f name is '+str(type(flow_name)))
        print(waarp.flows[flow_name])
        flow = waarp.flows[flow_name]
        print("%s %s %s %s %s %s %s "%(flow.name, flow['active'], flow['template'], flow['origin'], flow['originDir'], flow['description'], flow['filewatcher']))
        print("Destinations : %s"%flow.destinations)
        #f = Flow(flow.name, flow['active'] )
        #f = Flow()
        f = Flow(flow.id, flow.name, flow.active, flow.template, flow.origin, flow.originDir, flow.description, flow.filewatcher)
        db_session.add(f)
        for destination in flow.destinations:
            print("Dealing with dest %s"%destination)
            d = Destination(hostid=destination['partnerId'], path=destination['destinationDir'], flow_id=flow.id)
            db_session.add(d)

    db_session.commit()

    waarp.partner_inventory()
    for partner_name in waarp.partners:
        print('p name is '+str(type(partner_name)))
        print(waarp.partners[partner_name])
        partner = waarp.partners[partner_name]
        #print("%s %s %s %s %s %s %s "%(partner.name, partner['active'], partner['template'], partner['origin'], partner['originDir'], partner['description'], partner['filewatcher']))
        #f = Flow(flow.name, flow['active'] )
        #f = Flow()
        p = Partner(waarp_id=partner.id, site=partner.site, partner_type=partner.type, isClient=partner.isClient, isServer=partner.isServer, description=partner.description, hostid=partner.hostid, hostidssl=partner.hostidssl, ip=partner.ip)
        db_session.add(p)
    db_session.commit()

    waarp.site_inventory()
    for site_name in waarp.sites:
        print('s name is '+str(type(site_name)))
        print(waarp.sites[site_name])
        site = waarp.sites[site_name]
        #print("%s %s %s %s %s %s %s "%(partner.name, partner['active'], partner['template'], partner['origin'], partner['originDir'], partner['description'], partner['filewatcher']))
        #f = Flow(flow.name, flow['active'] )
        #f = Flow()
        s = Site(site.id, site.name, site.description)
        db_session.add(s)
    db_session.commit()
    waarp.template_inventory()
    for template_name in waarp.templates:
        print('s name is '+str(type(template_name)))
        print(waarp.templates[template_name])
        template = waarp.templates[template_name]
        t = FlowTemplate(template.id, template.name)
        db_session.add(t)
    db_session.commit()

init_db()
waarp=waarp_connect()
populate_db(db_session, waarp)
