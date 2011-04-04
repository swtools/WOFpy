from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy import Boolean

from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


#TODO: How can this be put in init method of the DAO?
import private_config
engine = create_engine(private_config.database_connection_string,
                       convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Variable(Base):
    __tablename__ = 'Variables'

    VariableID = Column(Integer, primary_key=True)
    VariableCode = Column(String)
    VariableName = Column(String)
    Speciation = Column(String)
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

class Site(Base):
    __tablename__ = 'Sites'
    
    SiteID = Column(Integer, primary_key = True)
    SiteCode = Column(String)
    SiteName = Column(String)
    Latitude = Column(Float)
    Longitude = Column(Float)
    LatLongDatumID = Column(Integer, ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    Elevation_m = Column(Float)
    VerticalDatum = Column(String)
    LocalX = Column(Float)
    LocalY = Column(Float)
    LocalProjectionID = Column(Integer, ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    PosAccuracy_m = Column(Float)
    State = Column(String)
    County = Column(String)
    Comments = Column(String)
    
    LatLongDatum = relationship("SpatialReference",
                                        primaryjoin='Site.LatLongDatumID==SpatialReference.SpatialReferenceId')
    
    LocalProjection = relationship("SpatialReference",
                                        primaryjoin='Site.LocalProjectionID==SpatialReference.SpatialReferenceId')
      
    def __repr__(self):
        return "<Site('%s','%s', ['%s' '%s'])>" % (self.SiteCode, self.SiteName, str(self.Latitude), str(self.Longitude))

#TODO: Setup foreignkey relationships
class DataValue(Base):
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
    DerivedFromID = Column(Integer)
    QualityControlLevelID = Column(Integer)
    

class Qualifier(Base):
    __tablename__ = 'Qualifiers'
    
    QualifierID = Column(Integer, primary_key=True)
    QualifierCode = Column(String)
    QualifierDescription = Column(String)

class OffsetType(Base):
    __tablename__ = 'OffsetTypes'
    
    OffsetTypeID = Column(Integer, primary_key = True)
    OffsetUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    OffsetDescription = Column(String)
    
    OffsetUnits = relationship("Units", \
                                primaryjoin='OffsetType.OffsetUnitsID==Units.UnitsID')


class Method(Base):
    __tablename__ ='Methods'
    
    MethodID = Column(Integer, primary_key=True)
    MethodDescription = Column(String)
    MethodLink = Column(String)
    
class Source(Base):
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
    Citation = Column(String)
    MetadataID = Column(Integer, ForeignKey('ISOMetadata.MetadataID'))
    
    Metadata = relationship("ISOMetadata", backref="Source")
    
class ISOMetadata(Base):
    __tablename__ = 'ISOMetadata'
    
    MetadataID = Column(Integer, primary_key=True)
    TopicCategory = Column(String) #TODO: FK to TopicCategoryCV
    Title = Column(String)
    Abstract = Column(String)
    ProfileVersion = Column(String)
    MetadataLink = Column(String)
    

class QualityControlLevel(Base):
    __tablename__='QualityControlLevels'
    
    QualityControlLevelID = Column(Integer, primary_key=True)
    QualityControlLevelCode = Column(String)
    Definition = Column(String)
    Explanation = Column(String)

class SeriesCatalog(Base):
    __tablename__ = 'SeriesCatalog'
    
    SeriesID = Column(Integer, primary_key = True)
    SiteID = Column(Integer, ForeignKey('Sites.SiteID'))
    SiteCode = Column(String)
    SiteName = Column(String)
    VariableID = Column(Integer, ForeignKey('Variables.VariableID'))
    VariableCode = Column(String)
    VariableName = Column(String)
    Speciation = Column(String)
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
    SourceID = Column(Integer) #TODO
    Organization = Column(String)
    SourceDescription = Column(String)
    Citation = Column(String)
    QualityControlLevelID = Column(Integer) #TODO
    QualityControlLevelCode = Column(String)
    BeginDateTime = Column(DateTime)
    EndDateTime = Column(DateTime)
    BeginDateTimeUTC = Column(DateTime)
    EndDateTimeUTC = Column(DateTime)
    ValueCount = Column(Integer)
    
    Site = relationship("Site", primaryjoin='SeriesCatalog.SiteID==Site.SiteID')
    Variable = relationship("Variable", primaryjoin='SeriesCatalog.VariableID==Variable.VariableID')
    Method = relationship("Method", primaryjoin='SeriesCatalog.MethodID==Method.MethodID')
    
    #VariableUnits = relationship("Units", \
    #                                primaryjoin='SeriesCatalog.VariableUnitsID==Units.UnitsID')
    
    #TimeUnits = relationship("Units", \
    #                            primaryjoin='SeriesCatalog.TimeUnitsID==Units.UnitsID')

    def __repr__(self):
        return "<Series(SeriesID: '%s',Site: '%s', VarID: '%s', Beg: '%s', End: '%s')>" % (self.SeriesID, self.SiteID, self.VariableID, str(self.BeginDateTimeUTC), str(self.EndDateTimeUTC))


class Units(Base):
    __tablename__ = 'Units'
    
    UnitsID = Column(Integer, primary_key=True)
    UnitsName = Column(String)
    UnitsType = Column(String)
    UnitsAbbreviation = Column(String)
    
class SpatialReference(Base):
    __tablename__ = 'SpatialReferences'
    
    SpatialReferenceId = Column(Integer, primary_key=True)
    SRSID = Column(Integer)
    SRSName = Column(String)
    IsGeographic = Column(Boolean)
    Notes = Column(String)
    
class VerticalDatum(Base):
    __tablename__ = 'VerticalDatumCV'
    Term = Column(String, primary_key=True)
    Definition = Column(String)