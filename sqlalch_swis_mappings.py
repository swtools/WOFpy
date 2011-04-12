
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy import Boolean

from sqlalchemy.sql import join
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
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
    #MethodID = Column(Integer)
    #SourceID = Column(Integer)
    #SampleID = Column(Integer)
    #DerivedFromID = Column(Integer)
    #QualityControlLevelID = Column(Integer)
       
    
#class SeriesCatalog(Base, wof_base.BaseSeriesCatalog):
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
    #BeginDateTime = None
    #EndDateTime = None
    #BeginDateTimeUTC = None
    #EndDateTimeUTC = None
    #ValueCount = None
    
    #Site = BaseSite()
    #Variable = BaseVariable()
    #Method = BaseMethod()
#    pass
    
    