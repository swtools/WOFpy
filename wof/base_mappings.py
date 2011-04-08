class BaseUnits(object):
    
    UnitsID = None
    UnitsName = None
    UnitsType = None
    UnitsAbbreviation = None
    
class BaseSpatialReference(object):
    
    SpatialReferenceId = None
    SRSID = None
    SRSName = None
    IsGeographic = None
    Notes = None

class BaseVariable(object):
    
    VariableID = None
    VariableCode = None
    VariableName = None
    Speciation = None
    VariableUnitsID = None
    SampleMedium = None
    ValueType = None
    IsRegular = None
    TimeSupport = None
    TimeUnitsID = None
    DataType = None
    GeneralCategory = None
    NoDataValue = None
    
    VariableUnits = BaseUnits()
    TimeUnits = BaseUnits()

class BaseSite(object):
      
    SiteID = None
    SiteCode = None
    SiteName = None
    Latitude = None
    Longitude = None
    LatLongDatumID = None #FK to SpatialReferences
    Elevation_m = None
    VerticalDatum = None
    LocalX = None
    LocalY = None
    LocalProjectionID = None #FK to SpatialReferences
    PosAccuracy_m = None
    State = None
    County = None
    Comments = None
    
    LatLongDatum = BaseSpatialReference()
    LocalProjection = BaseSpatialReference()
    

class BaseDataValue(object):
    
    ValueID = None
    DataValue = None
    ValueAccuracy = None
    LocalDateTime = None
    UTCOffset = None
    DateTimeUTC = None
    SiteID = None
    VariableID = None 
    OffsetValue = None
    OffsetTypeID = None
    CensorCode = None
    QualifierID = None
    MethodID = None
    SourceID = None
    SampleID = None
    DerivedFromID = None
    QualityControlLevelID = None
    

class BaseQualifier(object):
    
    QualifierID = None
    QualifierCode = None
    QualifierDescription = None

class BaseOffsetType(object):
    
    OffsetTypeID = None
    OffsetUnitsID = None
    OffsetDescription = None
    
    OffsetUnits = BaseUnits()


class BaseMethod(object):
     
    MethodID = None
    MethodDescription = None
    MethodLink = None
  
class BaseMetadata(object):
    
    MetadataID = None
    TopicCategory = None
    Title = None
    Abstract = None
    ProfileVersion = None
    MetadataLink = None
    
class BaseSource(object):
    
    SourceID = None
    Organization = None
    SourceDescription = None
    SourceLink = None
    ContactName = None
    Phone = None
    Email = None
    Address = None
    City = None
    State = None
    ZipCode = None
    Citation = None
    MetadataID = None
    
    Metadata = BaseMetadata()
    
class BaseQualityControlLevel(object):
    
    QualityControlLevelID = None
    QualityControlLevelCode = None
    Definition = None
    Explanation = None

class BaseSeriesCatalog(object):
    
    SeriesID = None
    SiteID = None
    SiteCode = None
    SiteName = None
    VariableID = None
    VariableCode = None
    VariableName = None
    Speciation = None
    VariableUnitsID = None 
    VariableUnitsName = None
    SampleMedium = None
    ValueType = None
    TimeSupport = None
    TimeUnitsID = None
    TimeUnitsName = None
    DataType = None
    GeneralCategory = None
    MethodID = None
    MethodDescription = None
    SourceID = None #TODO
    Organization = None
    SourceDescription = None
    Citation = None
    QualityControlLevelID = None #TODO
    QualityControlLevelCode = None
    BeginDateTime = None
    EndDateTime = None
    BeginDateTimeUTC = None
    EndDateTimeUTC = None
    ValueCount = None
    
    Site = BaseSite()
    Variable = BaseVariable()
    Method = BaseMethod()
    
    
class BaseVerticalDatum(object):
    
    Term = None
    Definition = None