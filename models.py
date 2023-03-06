from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Partner(Base):
    __tablename__ = 'partners'
    waarp_id = Column(Integer, primary_key=True)
    site = Column(Integer)
    type = Column(String(10))
    isClient = Column(Boolean())
    isServer = Column(Boolean())
    description = Column(String(20))
    hostid = Column(String(30))
    hostidssl = Column(String(30))


    def __init__(self, waarp_id, site=1, partner_type='r66', isClient=True, isServer=True, description='', hostid='', hostidssl=''):
        self.waarp_id = waarp_id
        self.site = site
        self.type = partner_type
        self.isClient = isClient
        self.isServer = isServer
        self.description = description
        self.hostid = hostid
        self.hostidssl = hostidssl

    def __repr__(self):
        return f'<Partner {self.hostid!r}>'


class Site(Base):
    __tablename__ = 'sites'
    waarp_id = Column(Integer, primary_key=True)
    name = Column(String(10))
    description = Column(String(20))


    def __init__(self, waarp_id, name='', description='', ):
        self.waarp_id = waarp_id
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Site {self.name!r}>'

class Destination(Base):
    __tablename__ = 'destinations'
    id = Column(Integer, primary_key=True)
    hostid = Column(Integer)
    path = Column(String(200))
    flow_id = Column(Integer)


    def __init__(self, hostid=1, path='', flow_id=1):
        self.hostid = hostid
        self.path = path
        self.flow_id = flow_id

    def __repr__(self):
        return f'<Destination {self.path!r}>'

class Flow(Base):
    __tablename__ = 'flows'
    waarp_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    active = Column(Boolean())
    template = Column(Integer)
    origin = Column(Integer)
    origindir = Column(String(40))
    # Destination ? 
    description = Column(String(20))
    filewatcher = Column(Boolean())



    def __init__(self, waarp_id, name='', active=True, template=3, origin=0, originDir='', description='', filewatcher=True):
        self.waarp_id = waarp_id
        self.name = name
        self.active = active
        self.template = template
        self.origin = origin
        self.origindir = originDir
        self.description = description
        self.filewatcher = filewatcher

    def __repr__(self):
        return f'<Flow {self.name!r}>'


class FlowTemplate(Base):
    __tablename__ = 'flowtemplates'
    waarp_id = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __init__(self, waarp_id, name='' ):
        self.waarp_id = waarp_id
        self.name = name

    def __repr__(self):
        return f'<FlowTemplate {self.name!r}>'


class PartnerRequest(Base):
    __tablename__ = 'partner_requests'
    id = Column(Integer, primary_key=True)
    site = Column(Integer)
    type = Column(String(10))
    isClient = Column(Boolean())
    isServer = Column(Boolean())
    description = Column(String(20))
    status = Column(String(20))
    additionalInformation = Column(String(400))
    hostid = Column(String(30))
    hostidssl = Column(String(30))


    def __init__(self, site=1, type='r66', isClient=True, isServer=True, description='', hostid='', hostidssl='', status='created', additionalInformation='', ):
        self.site = site
        self.type = type
        self.isClient = isClient
        self.isServer = isServer
        self.description = description
        self.hostid = hostid
        self.hostidssl = hostidssl
        self.status = status
        self.additionalInformation = additionalInformation

    def __repr__(self):
        return f'<PartnerRequest {self.hostid!r}>'



class FlowRequest(Base):
    __tablename__ = 'flow_requests'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    active = Column(Boolean())
    template = Column(Integer)
    origin = Column(Integer)
    originDir = Column(String(40))
    description = Column(String(20))
    status = Column(String(20))
    additionalInformation = Column(String(400))
    filewatcher = Column(Boolean())



    def __init__(self, name='', active=True, template=3, origin=0, originDir='', description='', filewatcher=True, status='created', additionalInformation=''):
        self.name = name
        self.active = active
        self.template = template
        self.origin = origin
        self.originDir = originDir
        self.description = description
        self.status = status
        self.additionalInformation = additionalInformation
        self.filewatcher = filewatcher

    def __repr__(self):
        return f'<FlowRequest {self.name!r}>'

class DestinationRequested(Base):
    __tablename__ = 'destinations_requested'
    id = Column(Integer, primary_key=True)
    hostid = Column(Integer)
    path = Column(String(200))
    flow_id = Column(Integer)


    def __init__(self, hostid=1, path='', ):
        self.hostid = hostid
        self.path = path

    def __repr__(self):
        return f'<Destination {self.path!r}>'
