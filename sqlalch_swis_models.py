
import datetime

from sqlalchemy import (Table, Column, Integer, String, ForeignKey, Float,
                        DateTime, Boolean)

from sqlalchemy.sql import join, select, func, label
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.declarative import declarative_base

import wof.base_models as wof_base

Base = declarative_base()

def init_model(db_session):
    Base.query = db_session.query_property()

class Variable(Base, wof_base.BaseVariable):
    __tablename__ = 'parameter'

    VariableID = Column('id', Integer, primary_key=True)
    VariableCode = Column('parameter_code', String)
    VariableName = Column('parameter_description', String)
    #Speciation = Column(String)
    #VariableUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    #SampleMedium = Column(String)
    #ValueType = Column(String)
    #IsRegular = Column(Boolean)
    #TimeSupport = Column(Float)
    #TimeUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    #DataType = Column(String)
    #GeneralCategory = Column(String)
    #NoDataValue = Column(Float)
    
    #TODO: Might be good to have a Units table in the SWIS schema
    #VariableUnits = relationship("Units",
    #                            primaryjoin='Variable.VariableUnitsID==Units.UnitsID')
    
    #TimeUnits = relationship("Units",
    #                         primaryjoin='Variable.TimeUnitsID==Units.UnitsID')

class Site(Base, wof_base.BaseSite):
    __tablename__ = 'site'
    
    SiteID = Column('id', Integer, primary_key=True)
    SiteCode = Column('site_code', String)
    SiteName = Column('name', String)
    #Geom = GeometryColumn('geom', Point(2)) #TODO Andy
    
    @property
    def Latitude(self):
        #x, y = self.Geom.coords(db_session) #TODO Andy
        #return y
        return 0.0
    
    @property
    def Longitude(self):
        #x, y = self.Geom.coords(db_session) #TODO Andy
        #return x
        return 0.0
        
    #Elevation_m = Column(Float)
    #VerticalDatum = Column(String)
    
    #All sites are in WGS84
    LatLongDatum = wof_base.BaseSpatialReference()
    LatLongDatum.SRSID=4326
    LatLongDatum.IsGeographic=True
    LatLongDatum.SRSName="WGS84"

class DataValue(Base, wof_base.BaseDataValue):
    __tablename__ = 'raw_data_value'
    
    ValueID = Column('id', Integer, primary_key=True)
    DataValue = Column('data_value', Float)
    UTCOffset = Column('origin_utc_offset', Integer)
    DateTimeUTC = Column('datetime_utc', DateTime)
    SiteID = Column('site_id', Integer)
    VariableID = Column('parameter_id', Integer) 
    OffsetValue = Column('vertical_offset', Float)
    CensorCode = "nc" #Data are non-censored TODO: Check if this is always the case
    
    #ValueAccuracy = Column(Float) #TODO
    #QualifierID = Column(Integer)
    #OffsetTypeID = Column(Integer)
    
    #Using Instrument information for the Method
    MethodID = Column('instrument_id', Integer, ForeignKey('Method.MethodID'))
    
    SourceID = 1 #Only have one Source for SWIS data
    QualityControlLevelID = 1 #All of SWIS data values are "raw data"

#Using instrument information for Method of WaterML
class Method(Base, wof_base.BaseMethod):
    __tablename__ = 'instrument'
    
    MethodID = Column('id', Integer, primary_key=True)
    #MethodLink = None
    
    InstrumentModelID = Column('instrument_model_id', Integer,
                               ForeignKey('instrument_model.id'))
    
    InstrumentModel = relationship('InstrumentModel',
                            primaryjoin='Method.InstrumentModelID==\
                                        InstrumentModel.ModelID')
    
    @property
    def MethodDescription(self):
        if (self.InstrumentModel and
            self.InstrumentModel.InstrumentManufacturer):
            return "Measured with %s %s." \
                % (self.InstrumentModel.InstrumentManufacturer.ManufacturerName,
                   self.InstrumentModel.ModelName)
        else:
            return None

#SWIS-specific table
class InstrumentModel(Base):
    __tablename__ = 'instrument_model'
    
    ModelID = Column('id', Integer, primary_key=True)
    ModelName = Column('instrument_model_name', String)
    ManufacturerID = Column('instrument_manufacturer_id', Integer,
                            ForeignKey('instrument_manufacturer.id'))
    
    InstrumentManufacturer = relationship('InstrumentManufacturer',
                                primaryjoin='InstrumentModel.ManufacturerID==\
                                            InstrumentManufacturer.\
                                            ManufacturerID')
    
#SWIS-specific table
class InstrumentManufacturer(Base):
    __tablename__ = 'instrument_manufacturer'
    
    ManufacturerID = Column('id', Integer, primary_key=True)
    ManufacturerName = Column('instrument_manufacturer_name', String)   


#Each site has an agency associated with it in
# the agency_site_association table
agency_site_association_table = Table(
    'agency_site_association',
    Base.metadata,
    Column('agency_id', Integer, ForeignKey('agency.id')),
    Column('site_id', Integer, ForeignKey('site.id')))

#TWDB is the Source/contact for all SWIS data
class Source(wof_base.BaseSource):
    SourceID = 1

    #TODO: Metadata
    Metadata = None


#TODO: Metadata
# Not a clear mapping.  project.name could be title, project.description could be abstract
#class Metadata(wof_base.BaseMetadata):
#    __tablename__='ISOMetadata'
#    
#    MetadataID = Column(Integer, primary_key=True)
#    TopicCategory = Column(String)
#    Title = Column(String)
#    Abstract = Column(String)
#    ProfileVersion = Column(String)
#    MetadataLink = Column(String)

class Qualifier(wof_base.BaseQualifier):
    #TODO
    QualifierID = None
    QualifierCode = None
    QualifierDescription = None

class QualityControlLevel(wof_base.BaseQualityControlLevel):
    #All of SWIS data values are "raw data"
    QualityControlLevelID = 1
    QualityControlLevelCode = "Raw Data"
    Definition = "Raw Data"
    Explanation = "Raw Data"
 
 
#TODO  Looks like SWIS only has one type of offset, 'vertical_offset'
# but need to find out what the units will be
class OffsetType(wof_base.BaseOffsetType):
    OffsetTypeID = 1
    OffsetUnitsID = None #TODO
    OffsetDescription = "Vertical"
    
    OffsetUnits = None #TODO

class SeriesCatalog(wof_base.BaseSeriesCatalog):

    def __init__(self, site=None, variable=None, value_count=None,
                 begin_date_time_utc=None, end_date_time_utc=None):
        
        self.Site = site
        self.Variable = variable
        self.ValueCount = value_count
        self.BeginDateTimeUTC = begin_date_time_utc
        self.EndDateTimeUTC = end_date_time_utc
    
        self.QualityControlLevelID = 1 #SWIS only has one QCLevel, "Raw Data"
        self.QualityControlLevelCode = "Raw Data"
    
        #TODO:
        #self.MethodID
        #self.Method
        
        #self.SourceID
        #self.Source
        
                    
    #SeriesID = None
    #SiteID = None
    #SiteCode = Column(String, primary_key=True)
    #SiteName = None
    #VariableID = None
    #VariableCode = Column(String, primary_key=True)
    #VariableName = None
    #Speciation = None
    #VariableUnitsID = None 
    #VariableUnitsName = None
    #SampleMedium = None
    #ValueType = None
    #TimeSupport = None
    #TimeUnitsID = None
    #TimeUnitsName = None
    #DataType = None
    #GeneralCategory = None
    #MethodID = None
    #MethodDescription = None
    #SourceID = None #TODO
    #Organization = None
    #SourceDescription = None
    #Citation = None
    #QualityControlLevelID = None #TODO
    #QualityControlLevelCode = None

    #Method = BaseMethod()
    pass
    