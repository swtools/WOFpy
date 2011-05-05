
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
    
    
class Variable(Base, wof_base.BaseVariable):
    __tablename__ = 'Variables'
    
    def __init__(self, code, name):
        self.VariableCode = code
        self.VariableName = name
    
    VariableID = Column(Integer, primary_key=True)
    VariableCode = Column(String)
    VariableName = Column(String)
    
    #Speciation = None
    #VariableUnitsID = None
    #SampleMedium = None
    #ValueType = None
    #IsRegular = None
    #TimeSupport = None
    #TimeUnitsID = None
    #DataType = None
    #GeneralCategory = None
    #NoDataValue = None
    
    #VariableUnits = None
    #TimeUnits = None