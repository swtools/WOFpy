
from sqlalchemy import create_engine, Table
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy import Boolean

from sqlalchemy.sql import join, select, func, label
from sqlalchemy.orm import mapper, scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import wof.base_mappings as wof_base

import private_config
engine = create_engine(private_config.swis_connection_string,
                       convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine))

Base = declarative_base()
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
    
    #Latitude = Column(Float)
    #Longitude = Column(Float)
    #LatLongDatumID = Column(Integer, ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    
    
    
    #Elevation_m = Column(Float)
    #VerticalDatum = Column(String)
    #LocalX = Column(Float)
    #LocalY = Column(Float)
    #LocalProjectionID = Column(Integer, ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    #PosAccuracy_m = Column(Float)
    #State = Column(String)
    #County = Column(String)
    #Comments = Column(String)
    
    #LatLongDatum = relationship("SpatialReference",
    #                                    primaryjoin='Site.LatLongDatumID==SpatialReference.SpatialReferenceId')
    
    #LocalProjection = relationship("SpatialReference",
    #                                    primaryjoin='Site.LocalProjectionID==SpatialReference.SpatialReferenceId')
    
    
class DataValue(Base, wof_base.BaseDataValue):
    __tablename__ = 'raw_data_value'
    
    ValueID = Column('id', Integer, primary_key=True)
    DataValue = Column('data_value', Float)
    #ValueAccuracy = Column(Float)
    #LocalDateTime = Column(DateTime)
    UTCOffset = Column('origin_utc_offset', Integer)
    DateTimeUTC = Column('datetime_utc', DateTime)
    SiteID = Column('site_id', Integer)
    VariableID = Column('parameter_id', Integer) 
    OffsetValue = Column('vertical_offset', Float)
    #OffsetTypeID = Column(Integer)
    #CensorCode = Column(String)
    #QualifierID = Column(Integer)
    
    #Using Instrument information for the Method
    MethodID = Column('instrument_id', Integer, ForeignKey('Units.UnitsID'))
    #SourceID = Column(Integer)
    #SampleID = Column(Integer)
    #DerivedFromID = Column(Integer)
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


#Source is Agency in SWIS.  Each site has an agency associated with it in
# the agency_site_association table
agency_site_association_table = Table(
    'agency_site_association',
    Base.metadata,
    Column('agency_id', Integer, ForeignKey('agency.id')),
    Column('site_id', Integer, ForeignKey('site.id')))

class Source(Base, wof_base.BaseSource):
    __tablename__ = 'agency'
    SourceID = Column('id', Integer, primary_key=True)
    Organization = Column('name', String)
    
    #Not a clear mapping in SWIS. It could come from project.description
    #TODO: SourceDescription
    
    
    Sites = relationship('Site',
                         secondary=agency_site_association_table,
                         backref='Sources')
    
    #TODO:
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


class QualityControlLevel(wof_base.BaseQualityControlLevel):
    #All of SWIS data values are "raw data"
    QualityControlLevelID = 1
    QualityControlLevelCode = "Raw Data"
    Definition = "Raw Data"
    Explanation = "Raw Data"
  

class SeriesCatalog(wof_base.BaseSeriesCatalog):
    
    
    
    def __init__(self, site=None, variable=None, value_count=None,
                 begin_date_time_utc=None, end_date_time_utc=None,
                 begin_date_time=None, end_date_time=None):
        
        self.Site = site
        self.Variable = variable
        self.ValueCount = value_count
        self.BeginDateTimeUTC = begin_date_time_utc
        self.EndDateTimeUTC = end_date_time_utc
        self.BeginDateTime = begin_date_time
        self.EndDateTime = end_date_time
    
        
                
        #TODO:
        #self.Method
        #self.SourceID,
        #self.Organization,
        #self.SourceDescription,
        #self.Source
        #self.QualityControlLevelID
        #self.QualityControlLevelCode
                    
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
    