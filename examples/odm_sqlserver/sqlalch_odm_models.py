
from sqlalchemy import (Column, Integer, String, ForeignKey, Float, DateTime,
                        Boolean)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import wof.models as wof_base

Base = declarative_base()


def init_model(db_session):
    Base.query = db_session.query_property()


class Variable(Base, wof_base.BaseVariable):
    __tablename__ = 'Variables'

    VariableID = Column(Integer, primary_key=True)
    VariableCode = Column(String)
    VariableName = Column(String)
    VariableUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    SampleMedium = Column(String)
    ValueType = Column(String)
    IsRegular = Column(Boolean)
    TimeSupport = Column(Float)
    TimeUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    DataType = Column(String)
    GeneralCategory = Column(String)
    NoDataValue = Column(Float)
    
    VariableUnits = relationship("Units",
                        primaryjoin='Variable.VariableUnitsID==Units.UnitsID')
    
    TimeUnits = relationship("Units",
                        primaryjoin='Variable.TimeUnitsID==Units.UnitsID')

    def __repr__(self):
        return "<Variable('%s','%s')>" % (self.VariableCode, self.VariableName)

class Site(Base, wof_base.BaseSite):
    __tablename__ = 'Sites'
    
    SiteID = Column(Integer, primary_key = True)
    SiteCode = Column(String)
    SiteName = Column(String)
    Latitude = Column(Float)
    Longitude = Column(Float)
    LatLongDatumID = Column(Integer,
                        ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    Elevation_m = Column(Float)
    VerticalDatum = Column(String)
    LocalX = Column(Float)
    LocalY = Column(Float)
    LocalProjectionID = Column(Integer,
                        ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    State = Column(String)
    County = Column(String)
    Comments = Column(String)
    
    LatLongDatum = relationship("SpatialReference",
                                    primaryjoin='Site.LatLongDatumID==\
                                        SpatialReference.SpatialReferenceId')
    
    LocalProjection = relationship("SpatialReference",
                                    primaryjoin='Site.LocalProjectionID==\
                                        SpatialReference.SpatialReferenceId')
      
    def __repr__(self):
        return "<Site('%s','%s', ['%s' '%s'])>" % (self.SiteCode,
                                                   self.SiteName,
                                                   str(self.Latitude),
                                                   str(self.Longitude))

class DataValue(Base, wof_base.BaseDataValue):
    __tablename__ = 'DataValues'
    
    ValueID = Column(Integer, primary_key = True)
    DataValue = Column(Float)
    ValueAccuracy = Column(Float)
    LocalDateTime = Column(DateTime)
    UTCOffset = Column(Float)
    DateTimeUTC = Column(DateTime)
    SiteID = Column(Integer)
    VariableID = Column(Integer) 
    OffsetValue = Column(Float)
    OffsetTypeID = Column(Integer)
    CensorCode = Column(String)
    QualifierID = Column(Integer)
    MethodID = Column(Integer)
    SourceID = Column(Integer)
    SampleID = Column(Integer)
    QualityControlLevelID = Column(Integer)
    
    @property
    def QualityControlLevel(self):
        for name_code in wof_base.QualityControlLevelTypes:
            if self.QualityControlLevelID==name_code[1]:
                return name_code[0]
        
        return wof_base.QualityControlLevelTypes['RAW_DATA'][0]
    
class Qualifier(Base, wof_base.BaseQualifier):
    __tablename__ = 'Qualifiers'
    
    QualifierID = Column(Integer, primary_key=True)
    QualifierCode = Column(String)
    QualifierDescription = Column(String)

class OffsetType(Base, wof_base.BaseOffsetType):
    __tablename__ = 'OffsetTypes'
    
    OffsetTypeID = Column(Integer, primary_key = True)
    OffsetUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    OffsetDescription = Column(String)
    
    OffsetUnits = relationship("Units",
                primaryjoin='OffsetType.OffsetUnitsID==Units.UnitsID')


class Method(Base, wof_base.BaseMethod):
    __tablename__ ='Methods'
    
    MethodID = Column(Integer, primary_key=True)
    MethodDescription = Column(String)
    MethodLink = Column(String)
    
class Source(Base, wof_base.BaseSource):
    __tablename__='Sources'
    
    SourceID = Column(Integer, primary_key=True)
    Organization = Column(String)
    SourceDescription = Column(String)
    SourceLink = Column(String)
    ContactName = Column(String)
    Phone = Column(String)
    Email = Column(String)
    Address = Column(String)
    City = Column(String)
    State = Column(String)
    ZipCode = Column(String)
    MetadataID = Column(Integer, ForeignKey('ISOMetadata.MetadataID'))
    
    Metadata = relationship("Metadata",
                    primaryjoin='Source.MetadataID==Metadata.MetadataID')
    
class Metadata(Base, wof_base.BaseMetadata):
    __tablename__='ISOMetadata'
    
    MetadataID = Column(Integer, primary_key=True)
    TopicCategory = Column(String)
    Title = Column(String)
    Abstract = Column(String)
    ProfileVersion = Column(String)
    MetadataLink = Column(String)    

class QualityControlLevel(Base, wof_base.BaseQualityControlLevel):
    __tablename__='QualityControlLevels'
    
    QualityControlLevelID = Column(Integer, primary_key=True)
    QualityControlLevelCode = Column(String)

class Series(Base, wof_base.BaseSeries):
    __tablename__ = 'SeriesCatalog'
    
    SeriesID = Column(Integer, primary_key = True)
    SiteID = Column(Integer, ForeignKey('Sites.SiteID'))
    SiteCode = Column(String)
    SiteName = Column(String)
    VariableID = Column(Integer, ForeignKey('Variables.VariableID'))
    VariableCode = Column(String)
    VariableName = Column(String)
    VariableUnitsID = Column(Integer, ForeignKey('Units.UnitsID')) 
    VariableUnitsName = Column(String)
    SampleMedium = Column(String)
    ValueType = Column(String)
    TimeSupport = Column(Float)
    TimeUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    TimeUnitsName = Column(String)
    DataType = Column(String)
    GeneralCategory = Column(String)
    MethodID = Column(Integer, ForeignKey('Methods.MethodID'))
    MethodDescription = Column(String)
    SourceID = Column(Integer, ForeignKey('Sources.SourceID'))
    Organization = Column(String)
    SourceDescription = Column(String)
    QualityControlLevelID = Column(Integer) #TODO
    QualityControlLevelCode = Column(String)
    BeginDateTime = Column(DateTime)
    EndDateTime = Column(DateTime)
    BeginDateTimeUTC = Column(DateTime)
    EndDateTimeUTC = Column(DateTime)
    ValueCount = Column(Integer)
    
    Site = relationship("Site",
                primaryjoin='Series.SiteID==Site.SiteID')
    
    Variable = relationship("Variable",
                primaryjoin='Series.VariableID==Variable.VariableID')
    
    Method = relationship("Method",
                primaryjoin='Series.MethodID==Method.MethodID')
    
    Source = relationship("Source",
                primaryjoin='Series.SourceID==Source.SourceID')


class Units(Base, wof_base.BaseUnits):
    __tablename__ = 'Units'
    
    UnitsID = Column(Integer, primary_key=True)
    UnitsName = Column(String)
    UnitsType = Column(String)
    UnitsAbbreviation = Column(String)
    
class SpatialReference(Base, wof_base.BaseSpatialReference):
    __tablename__ = 'SpatialReferences'
    
    SpatialReferenceId = Column(Integer, primary_key=True)
    SRSID = Column(Integer)
    SRSName = Column(String)
    Notes = Column(String)
    
class VerticalDatum(Base, wof_base.BaseVerticalDatum):
    __tablename__ = 'VerticalDatumCV'
    Term = Column(String, primary_key=True)
    Definition = Column(String)
