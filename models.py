from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Partner(Base):
    __tablename__ = 'partners'
    id = Column(Integer, primary_key=True)
    site = Column(Integer)
    type = Column(String(10))
    isClient = Column(Boolean())
    isServer = Column(Boolean())
    description = Column(String(20))
    hostid = Column(String(30))
    hostidssl = Column(String(30))


    def __init__(self, id, site=1, type='r66', isClient=True, isServer=True, description='', hostid='', hostidssl=''):
        self.id = id
        self.site = site
        self.type = type
        self.isClient = isClient
        self.isServer = isServer
        self.description = description
        self.hostid = hostid
        self.hostidssl = hostidssl

    def __repr__(self):
        return f'<Partner {self.hostid!r}>'


class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    description = Column(String(20))


    def __init__(self, id, name='', description='', ):
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Site {self.name!r}>'


class Flow(Base):
    __tablename__ = 'flows'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    active = Column(Boolean())
    template = Column(Integer)
    origin = Column(Integer)
    originDir = Column(String(40))
    # Destination ? 
    description = Column(String(20))
    filewatcher = Column(Boolean())



    def __init__(self, id, name='', active=True, template=3, origin=0, originDir='', description='', filewatcher=True):
        self.id = id
        self.name = name
        self.active = active
        self.template = template
        self.origin = origin
        self.originDir = originDir
        self.description = description
        self.filewatcher = filewatcher

    def __repr__(self):
        return f'<Flow {self.name!r}>'


class FlowTemplate(Base):
    __tablename__ = 'flowtemplates'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    def __init__(self, id, name='' ):
        self.id = id
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
    hostid = Column(String(30))
    hostidssl = Column(String(30))


    def __init__(self, id, site=1, type='r66', isClient=True, isServer=True, description='', hostid='', hostidssl=''):
        self.id = id
        self.site = site
        self.type = type
        self.isClient = isClient
        self.isServer = isServer
        self.description = description
        self.hostid = hostid
        self.hostidssl = hostidssl

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
    # Destination ? 
    description = Column(String(20))
    filewatcher = Column(Boolean())



    def __init__(self, id, name='', active=True, template=3, origin=0, originDir='', description='', filewatcher=True):
        self.id = id
        self.name = name
        self.active = active
        self.template = template
        self.origin = origin
        self.originDir = originDir
        self.description = description
        self.filewatcher = filewatcher

    def __repr__(self):
        return f'<FlowRequest {self.name!r}>'        