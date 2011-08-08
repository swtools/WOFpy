class SampleMediumTypes:
    SURFACE_WATER = 'Surface Water'
    GROUND_WATER = 'Ground Water'
    SEDIMENT = 'Sediment'
    SOIL = 'Soil'
    AIR = 'Air'
    TISSUE = 'Tissue'
    PRECIPITATION = 'Precipitation'
    UNKNOWN = 'Unknown'
    OTHER = 'Other'
    SNOW = 'Snow'
    NOT_RELEVANT = 'Not Relevant'


class GeneralCategoryTypes:
    WATER_QUALITY = 'Water Quality'
    CLIMATE = 'Climate'
    HYDROLOGY = 'Hydrology'
    GEOLOGY = 'Geology'
    BIOTA = 'Biota'
    UNKNOWN = 'Unknown'
    INSTRUMENTATION = 'Instrumentation'


QualityControlLevelTypes = {
    'UNKNOWN': ('Unknown', -9999),
    'RAW_DATA': ('Raw data', 0),
    'QUAL_CONTROLLED_DATA': ('Quality controlled data', 1),
    'DERIVED_PRODUCTS': ('Derived products', 2),
    'INTERPRETED_PRODUCTS': ('Interpreted products', 3),
    'KNOWLEDGE_PRODUCTS': ('Knowledge products', 4)
}


class BaseUnits(object):
    UnitsID = None
    UnitsName = None
    UnitsType = None
    UnitsAbbreviation = None


class BaseSpatialReference(object):
    SpatialReferenceId = None
    SRSID = None
    SRSName = None
    Notes = None


class BaseVariable(object):
    VariableID = None
    VariableCode = None
    VariableName = None
    VariableUnitsID = None
    SampleMedium = None
    ValueType = None
    IsRegular = None
    TimeSupport = None
    TimeUnitsID = None
    DataType = None
    GeneralCategory = None
    NoDataValue = None
    VariableDescription = None
    VariableUnits = BaseUnits()
    TimeUnits = BaseUnits()


class BaseSite(object):
    SiteID = None
    SiteCode = None
    SiteName = None
    Latitude = None
    Longitude = None
    #FK to SpatialReferences
    LatLongDatumID = None
    Elevation_m = None
    VerticalDatum = None
    LocalX = None
    LocalY = None
    #FK to SpatialReferences
    LocalProjectionID = None
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
    QualityControlLevel = None
    QualityControlLevelID = None

    def __repr__(self):
        return '<DataValue: (%s, %s)>' % (self.DataValue, self.DateTimeUTC)


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
    MetadataID = None
    Metadata = BaseMetadata()


class BaseQualityControlLevel(object):
    QualityControlLevelID = None
    QualityControlLevelCode = None


class BaseSeries(object):
    SeriesID = None
    SiteID = None
    SiteCode = None
    SiteName = None
    VariableID = None
    VariableCode = None
    VariableName = None
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
    SourceID = None
    Organization = None
    SourceDescription = None
    QualityControlLevelID = None
    QualityControlLevelCode = None
    BeginDateTime = None
    EndDateTime = None
    BeginDateTimeUTC = None
    EndDateTimeUTC = None
    ValueCount = None

    Site = BaseSite()
    Variable = BaseVariable()
    Method = BaseMethod()
    Source = BaseSource()


class BaseVerticalDatum(object):

    Term = None
    Definition = None
