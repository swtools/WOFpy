from flaskext.sqlalchemy import SQLAlchemy
from wof import app

db = SQLAlchemy(app)

class Variable(db.Model):
    __tablename__ = 'Variables'

    VariableID = db.Column(db.Integer, primary_key=True)
    VariableCode = db.Column(db.String)
    VariableName = db.Column(db.String)
    Speciation = db.Column(db.String)
    VariableUnitsID = db.Column(db.Integer, db.ForeignKey('Units.UnitsID'))
    SampleMedium = db.Column(db.String)
    ValueType = db.Column(db.String)
    IsRegular = db.Column(db.Boolean)
    TimeSupport = db.Column(db.Float)
    TimeUnitsID = db.Column(db.Integer, db.ForeignKey('Units.UnitsID'))
    DataType = db.Column(db.String)
    GeneralCategory = db.Column(db.String)
    NoDataValue = db.Column(db.Float)
    
    VariableUnits = db.relationship("Units", \
                                    primaryjoin='Variable.VariableUnitsID==Units.UnitsID')
    
    TimeUnits = db.relationship("Units", \
                                primaryjoin='Variable.TimeUnitsID==Units.UnitsID')

    def __repr__(self):
        return "<Variable('%s','%s')>" % (self.VariableCode, self.VariableName)

class Site(db.Model):
    __tablename__ = 'Sites'
    
    SiteID = db.Column(db.Integer, primary_key = True)
    SiteCode = db.Column(db.String)
    SiteName = db.Column(db.String)
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    LatLongDatumID = db.Column(db.Integer, db.ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    Elevation_m = db.Column(db.Float)
    VerticalDatum = db.Column(db.String)
    LocalX = db.Column(db.Float)
    LocalY = db.Column(db.Float)
    LocalProjectionID = db.Column(db.Integer, db.ForeignKey('SpatialReferences.SpatialReferenceId')) #FK to SpatialReferences
    PosAccuracy_m = db.Column(db.Float)
    State = db.Column(db.String)
    County = db.Column(db.String)
    Comments = db.Column(db.String)
    
    LatLongDatum = db.relationship("SpatialReference", \
                                        primaryjoin='Site.LatLongDatumID==SpatialReference.SpatialReferenceId')
    
    LocalProjection = db.relationship("SpatialReference", \
                                        primaryjoin='Site.LocalProjectionID==SpatialReference.SpatialReferenceId')
      
    def __repr__(self):
        return "<Site('%s','%s', ['%s' '%s'])>" % (self.SiteCode, self.SiteName, str(self.Latitude), str(self.Longitude))

#TODO: Setup foreignkey relationships
class DataValue(db.Model):
    __tablename__ = 'DataValues'
    
    ValueID = db.Column(db.Integer, primary_key = True)
    DataValue = db.Column(db.Float)
    ValueAccuracy = db.Column(db.Float)
    LocalDateTime = db.Column(db.DateTime)
    UTCOffset = db.Column(db.Float)
    DateTimeUTC = db.Column(db.DateTime)
    SiteID = db.Column(db.Integer)
    VariableID = db.Column(db.Integer) 
    OffsetValue = db.Column(db.Float)
    OffsetTypeID = db.Column(db.Integer)
    CensorCode = db.Column(db.String)
    QualifierID = db.Column(db.Integer)
    MethodID = db.Column(db.Integer)
    SourceID = db.Column(db.Integer)
    SampleID = db.Column(db.Integer)
    DerivedFromID = db.Column(db.Integer)
    QualityControlLevelID = db.Column(db.Integer)
    

class Qualifier(db.Model):
    __tablename__ = 'Qualifiers'
    
    QualifierID = db.Column(db.Integer, primary_key=True)
    QualifierCode = db.Column(db.String)
    QualifierDescription = db.Column(db.String)

class OffsetType(db.Model):
    __tablename__ = 'OffsetTypes'
    
    OffsetTypeID = db.Column(db.Integer, primary_key = True)
    OffsetUnitsID = db.Column(db.Integer, db.ForeignKey('Units.UnitsID'))
    OffsetDescription = db.Column(db.String)
    
    OffsetUnits = db.relationship("Units", \
                                primaryjoin='OffsetType.OffsetUnitsID==Units.UnitsID')


class Method(db.Model):
    __tablename__ ='Methods'
    
    MethodID = db.Column(db.Integer, primary_key=True)
    MethodDescription = db.Column(db.String)
    MethodLink = db.Column(db.String)
    
class Source(db.Model):
    __tablename__='Sources'
    
    SourceID = db.Column(db.Integer, primary_key=True)
    Organization = db.Column(db.String)
    SourceDescription = db.Column(db.String)
    SourceLink = db.Column(db.String)
    ContactName = db.Column(db.String)
    Phone = db.Column(db.String)
    Email = db.Column(db.String)
    Address = db.Column(db.String)
    City = db.Column(db.String)
    State = db.Column(db.String)
    ZipCode = db.Column(db.String)
    Citation = db.Column(db.String)
    MetadataID = db.Column(db.Integer, db.ForeignKey('ISOMetadata.MetadataID'))
    
    Metadata = db.relationship("ISOMetadata", backref="Source")
    
class ISOMetadata(db.Model):
    __tablename__ = 'ISOMetadata'
    
    MetadataID = db.Column(db.Integer, primary_key=True)
    TopicCategory = db.Column(db.String) #TODO: FK to TopicCategoryCV
    Title = db.Column(db.String)
    Abstract = db.Column(db.String)
    ProfileVersion = db.Column(db.String)
    MetadataLink = db.Column(db.String)
    

class QualityControlLevel(db.Model):
    __tablename__='QualityControlLevels'
    
    QualityControlLevelID = db.Column(db.Integer, primary_key=True)
    QualityControlLevelCode = db.Column(db.String)
    Definition = db.Column(db.String)
    Explanation = db.Column(db.String)

class SeriesCatalog(db.Model):
    __tablename__ = 'SeriesCatalog'
    
    SeriesID = db.Column(db.Integer, primary_key = True)
    SiteID = db.Column(db.Integer, db.ForeignKey('Sites.SiteID'))
    SiteCode = db.Column(db.String)
    SiteName = db.Column(db.String)
    VariableID = db.Column(db.Integer, db.ForeignKey('Variables.VariableID'))
    VariableCode = db.Column(db.String)
    VariableName = db.Column(db.String)
    Speciation = db.Column(db.String)
    VariableUnitsID = db.Column(db.Integer, db.ForeignKey('Units.UnitsID')) 
    VariableUnitsName = db.Column(db.String)
    SampleMedium = db.Column(db.String)
    ValueType = db.Column(db.String)
    TimeSupport = db.Column(db.Float)
    TimeUnitsID = db.Column(db.Integer, db.ForeignKey('Units.UnitsID'))
    TimeUnitsName = db.Column(db.String)
    DataType = db.Column(db.String)
    GeneralCategory = db.Column(db.String)
    MethodID = db.Column(db.Integer, db.ForeignKey('Methods.MethodID'))
    MethodDescription = db.Column(db.String)
    SourceID = db.Column(db.Integer) #TODO
    Organization = db.Column(db.String)
    SourceDescription = db.Column(db.String)
    Citation = db.Column(db.String)
    QualityControlLevelID = db.Column(db.Integer) #TODO
    QualityControlLevelCode = db.Column(db.String)
    BeginDateTime = db.Column(db.DateTime)
    EndDateTime = db.Column(db.DateTime)
    BeginDateTimeUTC = db.Column(db.DateTime)
    EndDateTimeUTC = db.Column(db.DateTime)
    ValueCount = db.Column(db.Integer)
    
    Site = db.relationship("Site", primaryjoin='SeriesCatalog.SiteID==Site.SiteID')
    Variable = db.relationship("Variable", primaryjoin='SeriesCatalog.VariableID==Variable.VariableID')
    Method = db.relationship("Method", primaryjoin='SeriesCatalog.MethodID==Method.MethodID')
    
    #VariableUnits = db.relationship("Units", \
    #                                primaryjoin='SeriesCatalog.VariableUnitsID==Units.UnitsID')
    
    #TimeUnits = db.relationship("Units", \
    #                            primaryjoin='SeriesCatalog.TimeUnitsID==Units.UnitsID')

    def __repr__(self):
        return "<Series(SeriesID: '%s',Site: '%s', VarID: '%s', Beg: '%s', End: '%s')>" % (self.SeriesID, self.SiteID, self.VariableID, str(self.BeginDateTimeUTC), str(self.EndDateTimeUTC))


class Units(db.Model):
    __tablename__ = 'Units'
    
    UnitsID = db.Column(db.Integer, primary_key=True)
    UnitsName = db.Column(db.String)
    UnitsType = db.Column(db.String)
    UnitsAbbreviation = db.Column(db.String)
    
class SpatialReference(db.Model):
    __tablename__ = 'SpatialReferences'
    
    SpatialReferenceId = db.Column(db.Integer, primary_key=True)
    SRSID = db.Column(db.Integer)
    SRSName = db.Column(db.String)
    IsGeographic = db.Column(db.Boolean)
    Notes = db.Column(db.String)
    
class VerticalDatum(db.Model):
    __tablename__ = 'VerticalDatumCV'
    Term = db.Column(db.String, primary_key=True)
    Definition = db.Column(db.String)