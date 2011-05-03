
from sqlalchemy import (Column, Integer, String, ForeignKey, Float, DateTime,
                        Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import daos.base_models as wof_base

Base = declarative_base()


def clear_model(engine):
    Base.metadata.drop_all(engine)

def create_model(engine):
    Base.metadata.create_all(engine)

def init_model(db_session):
    Base.query = db_session.query_property()

class Site(Base, wof_base.BaseSite):
    __tablename__ = 'Sites'
    
    def __init__(self, code, name, latitude, longitude):
        self.SiteCode = code
        self.SiteName = name
        self.Latitude = latitude
        self.Longitude = longitude
    
    SiteID = Column(Integer, primary_key=True)
    SiteCode = Column(String)
    SiteName = Column(String)
    Latitude = Column(Float)
    Longitude = Column(Float)
    
    
class Parameter(Base):
    __tablename__ = 'Parameters'
    
    def __init__(self, code, name):
        self.ParamCode = code
        self.ParamName = name
    
    ParamID = Column(Integer, primary_key=True)
    ParamCode = Column(String)
    ParamName = Column(String)