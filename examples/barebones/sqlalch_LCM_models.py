import datetime

from sqlalchemy import (Table, Column, Integer, String, ForeignKey, Float,
                        DateTime, Boolean)

from sqlalchemy.sql import join, select, func, label
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.ext.declarative import declarative_base
from dateutil.parser import parse

import wof.models as wof_base

Base = declarative_base()

def init_model(db_session):
    Base.query = db_session.query_property()
    
class Variable(Base, wof_base.BaseVariable):
    __tablename__ = 'variables'

    VariableID = Column('rowid',Integer, primary_key=True)    
    VariableCode = Column(String)
    VariableName = Column(String)    
    
    SampleMedium = "Water"
    ValueType = "Field Observation"
    IsRegular = False
    #TimeSupport = Column(Float)
    #TimeUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    DataType = "Sporadic" 
    #GeneralCategory = "Unknown"
    
    NoDataValue = -9999
             
    VariableUnitsID = VariableID
        
    VariableUnits_UnitsID = VariableUnitsID
    VariableUnits_UnitsName = Column('Units',String)
    VariableUnits_UnitsAbbreviation = VariableUnits_UnitsName
    
    def __repr__(self):
        return "<Variable('%s','%s')>" % (self.VariableCode, self.VariableName)        

class Site(Base, wof_base.BaseSite):
    __tablename__ = 'sampling_sites'
    
    SiteID = Column('rowid',Integer, primary_key = True)
    SiteCode = Column('StationID',String)
    SiteName = Column('StationName',String)
    Latitude = Column(Float)
    Longitude = Column(Float)
    #LatLongDatumID = Column(Integer,
    #                    ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    #Elevation_m = Column(Float)
    #VerticalDatum = Column(String)
    #LocalX = Column(Float)
    #LocalY = Column(Float)
    #LocalProjectionID = Column(Integer,
    #                    ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    State = Column(String)
    County = Column(String)
    #Comments = Column(String)
    
    #LatLongDatum = relationship("SpatialReference",
    #                                primaryjoin='Site.LatLongDatumID==\
    #                                    SpatialReference.SpatialReferenceId')
    
    #LocalProjection = relationship("SpatialReference",
    #                                primaryjoin='Site.LocalProjectionID==\
    #                                    SpatialReference.SpatialReferenceId')
 
    def __repr__(self):
        return "<Site('%s','%s', ['%s' '%s'])>" % (self.SiteCode,
                                                   self.SiteName,
                                                   str(self.Latitude),
                                                   str(self.Longitude))

class DataValue(Base, wof_base.BaseDataValue):

    __tablename__ = 'LCM_Data'
    ValueID = Column('rowid',Integer, primary_key = True)    
    DataValue = Column('Result',Float)
    DateTimeUTC = Column(DateTime)
    UTCOffset = -5
    #DateString= Column('Date',String)
    #TimeString = Column('Time',String)
                   
    SiteCode = Column('Station',String,ForeignKey('sampling_sites.StationID')) #FK to sampling_sites)
    VariableCode = Column('Test',String,ForeignKey('variables.VariableCode')) #FK to variables)
    
    OffsetValue = Column('Depth',Float)
    OffsetTypeID = 1
    MethodID = ValueID
    MethodDescription = Column('Method',String)
    MethodLink =""
    
    #Assume data are non-censored 
    CensorCode = "nc"
    Site = relationship("Site",
                        primaryjoin='DataValue.SiteCode==\
                             Site.SiteCode')       
    Variable = relationship("Variable",
                        primaryjoin='DataValue.VariableCode==\
                             Variable.VariableCode')
    #
    #Assume all of LCM data values are "raw data"
    QualityControlLevel = wof_base.QualityControlLevelTypes['RAW_DATA'][0]
    QualityControlLevelID = wof_base.QualityControlLevelTypes['RAW_DATA'][1]

#LCM is the Source/contact for all LCM data
class Source(wof_base.BaseSource):
    SourceID = 1
    #TODO: Metadata
    Metadata = None
    
#   Not present in LCM database  
#class Qualifier(Base, wof_base.BaseQualifier):    
#    __tablename__ = 'Qualifiers'
#    
#    QualifierID = Column(Integer, primary_key=True)
#    QualifierCode = Column(String)
#    QualifierDescription = Column(String)

#class OffsetType(Base, wof_base.BaseOffsetType):
#    __tablename__ = 'OffsetTypes'
#    OffsetTypeID = Column(Integer, primary_key = True)
#    OffsetUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
#    OffsetDescription = Column(String)
#    
#    OffsetUnits = relationship("Units",
#                primaryjoin='OffsetType.OffsetUnitsID==Units.UnitsID')

#   Not present in LCM database  
#class Method(Base, wof_base.BaseMethod):
#    __tablename__ ='Methods'
#    
#    MethodID = Column(Integer, primary_key=True)
#    MethodDescription = Column(String)
#    MethodLink = Column(String)
#    

#   Not present in LCM database   
#class Metadata(Base, wof_base.BaseMetadata):
#    __tablename__='ISOMetadata'
#    
#    MetadataID = Column(Integer, primary_key=True)
#    TopicCategory = Column(String)
#    Title = Column(String)
#    Abstract = Column(String)
#    ProfileVersion = Column(String)
#    MetadataLink = Column(String)    

#   Not present in LCM database  
#class QualityControlLevel(Base, wof_base.BaseQualityControlLevel):
#    __tablename__='QualityControlLevels'
#    
#    QualityControlLevelID = Column(Integer, primary_key=True)
#    QualityControlLevelCode = Column(String)
#

class Series(wof_base.BaseSeries):

    def __init__(self, site=None, variable=None, value_count=None,
                 begin_date_time_utc=None, end_date_time_utc=None,
                 source=None):
        if not type(begin_date_time_utc) is datetime.datetime:
            begin_date_time_utc = parse(begin_date_time_utc)
        if not type(end_date_time_utc) is datetime.datetime:
            end_date_time_utc = parse(end_date_time_utc)
            
        self.Site = site
        self.Variable = variable
        self.ValueCount = value_count
        self.BeginDateTimeUTC = begin_date_time_utc
        self.EndDateTimeUTC = end_date_time_utc
        self.BeginDateTime = \
            begin_date_time_utc + datetime.timedelta(hours=-5)
        self.EndDateTime = \
            end_date_time_utc + datetime.timedelta(hours=-5)

        #SWIS data are all "Raw Data"
        # though might have more than one QC level in the future
        self.QualityControlLevelID = \
                            wof_base.QualityControlLevelTypes['RAW_DATA'][1]
        self.QualityControlLevelCode = \
                            wof_base.QualityControlLevelTypes['RAW_DATA'][0]

        self.Source = source

    Source = None
    Variable = None
    Site = None
    Method = None

#   Not present in LCM database  
#class Units(Base,wof_base.BaseUnits):
#    __tablename__ = 'Units'
#    #UnitsID = Variable.VariableID
#    UnitsID = Column('rowid',Integer, primary_key=True)
#    #UnitsName = Variable.OriginalUnits
#    UnitsName = Column('Units',String)
#    #UnitsType = Column(String)
#    #UnitsAbbreviation = Variable.OriginalUnits
#    UnitsAbbreviation = UnitsName

#   Not present in LCM database  
#class SpatialReference(Base, wof_base.BaseSpatialReference):
#    __tablename__ = 'SpatialReferences'
#    
#    SpatialReferenceId = Column(Integer, primary_key=True)
#    SRSID = Column(Integer)
#    SRSName = Column(String)
#    Notes = Column(String)

#   Not present in LCM database  
#class VerticalDatum(Base, wof_base.BaseVerticalDatum):
#    __tablename__ = 'VerticalDatumCV'
#    Term = Column(String, primary_key=True)
#    Definition = Column(String)
