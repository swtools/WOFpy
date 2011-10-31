import wof.models as wof_base


class Variable(wof_base.BaseVariable):
    # Properties common to all variables in this example
    SampleMedium = wof_base.SampleMediumTypes.SURFACE_WATER
    IsRegular = True
    ValueType = 'Field Observation'
    DataType = 'Average'
    NoDataValue = -9999
    TimeSupport = 1
    TimeUnitsID = 1
    GeneralCategory = wof_base.GeneralCategoryTypes.HYDROLOGY
    TimeUnits = wof_base.BaseUnits()
    TimeUnits.UnitsID = 1
    TimeUnits.UnitsName = 'day'
    TimeUnits.UnitsType = 'Time'
    TimeUnits.UnitsAbbreviation = 'd'


class Site(wof_base.BaseSite):
    # Properties common to all sites in this example
    LatLongDatum = wof_base.BaseSpatialReference()
    LatLongDatum.SRSID = 4269 # EPSG code
    LatLongDatum.SRSName = 'NAD83'
    State = 'Texas'


class Source(wof_base.BaseSource):
    # Only one in this example
    SourceID = 1
    ContactName = 'John Doe'
    Phone = '512-555-5555'
    Email = 'doe@email.com'
    Organization = 'Texas River Monitoring'
    SourceLink = 'http://trm.imaginary.gov/'
    SourceDescription = 'Observations along the Colorado River in Texas'
    Address = '123 Main St'
    City = 'Austin'
    State = 'TX'
    ZipCode = '78701'
    MetadataID = None
    Metadata = None
    

class Method(wof_base.BaseMethod):
    # Only one in this example
    MethodID = 1
    MethodDescription = 'Measured using an ACME FlowStage Measurer'
    

class QualityControlLevel(wof_base.BaseQualityControlLevel):
    # Only one in this example
    QualityControlLevelID = \
            wof_base.QualityControlLevelTypes['QUAL_CONTROLLED_DATA'][1]
    QualityControlLevelCode = \
            wof_base.QualityControlLevelTypes['QUAL_CONTROLLED_DATA'][0]


class DataValue(wof_base.BaseDataValue):
    # Properties common to all data values in this example
    UTCOffset = -6
    CensorCode = 'nc'
    MethodID = 1
    SourceID = 1
    QualityControlLevelID = \
            wof_base.QualityControlLevelTypes['QUAL_CONTROLLED_DATA'][1]
    QualityControlLevel = \
            wof_base.QualityControlLevelTypes['QUAL_CONTROLLED_DATA'][0]


class Series(wof_base.BaseSeries):
    # Properties common to all series in this example
    BeginDateTime = '2008-01-01T00:00-06'
    EndDateTime = '2008-04-30T00:00-06'
    BeginDateTimeUTC = '2008-01-01T06:00Z'
    EndDateTimeUTC = '2008-04-30T06:00Z'
    ValueCount = 121

    qc_level = QualityControlLevel()
    QualityControlLevelID = qc_level.QualityControlLevelID
    QualityControlLevelCode = qc_level.QualityControlLevelCode

    Method = Method()
    MethodID = Method.MethodID
    MethodDescription = Method.MethodDescription

    Source = Source()
    SourceID = Source.SourceID
    Organization = Source.Organization
    SourceDescription = Source.SourceDescription

    Variable = None
    Site = None
    
