from datetime import datetime as dt, timedelta, MINYEAR, MAXYEAR

from dateutil.parser import parse

from wof import dao, models


class TestSite(models.BaseSite):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestSpatialReference(models.BaseSpatialReference):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestVariable(models.BaseVariable):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestUnits(models.BaseUnits):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestSeries(models.BaseSeries):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestMethod(models.BaseMethod):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

   
class TestMetadata(models.BaseMetadata):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestSource(models.BaseSource):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    
class TestQualifier(models.BaseQualifier):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestOffsetType(models.BaseOffsetType):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestDataValue(models.BaseDataValue):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


test_spatialrefs = {
    'NAD83': TestSpatialReference(
        SpatialReferenceId = 2,
        SRSID = '4269',
        SRSName = 'NAD83',
        Notes = 'spatial ref note'),
    'UTM12N': TestSpatialReference(
        SpatialReferenceId = 105,
        SRSID = '26912',
        SRSName = 'NAD83 / UTM zone 12N',
        Notes = None)
    }

test_sites = {
    'SITE_A': TestSite(
        SiteID=1,
        SiteCode='SITE_A',
        SiteName='Site A',
        Latitude=50,
        Longitude=60),
    'SITE_B': TestSite(
        SiteID=2,
        SiteCode='SITE_B',
        SiteName='Site B',
        Latitude= 41.718473,
        Longitude=-111.946402,
        LatLongDatumID = 2,
        Elevation_m = 12.3,
        VerticalDatum = 'NGVD29',
        LocalX = 421276.323,
        LocalY = 4618952.04,
        LocalProjectionID = 105,
        State = 'Utah',
        County = 'Cache',
        Comments = 'Located in a neat place',
        LatLongDatum = test_spatialrefs['NAD83'],
        LocalProjection = test_spatialrefs['UTM12N']),
    'SITE_C': TestSite(
        SiteID=3,
        SiteCode='SITE_C',
        SiteName='Site C',
        Latitude=59,
        Longitude=10)
    }

test_units = {
    96: TestUnits(
        UnitsID = 96,
        UnitsName = 'degree celcius',
        UnitsType = 'Temperature',
        UnitsAbbreviation = 'degC'),
    100: TestUnits(
        UnitsID = 100,
        UnitsName = 'second',
        UnitsType = 'Time',
        UnitsAbbreviation = 's'),
    35: TestUnits(
        UnitsID = 35,
        UnitsName = 'cubic feet per second',
        UnitsType = 'Flow',
        UnitsAbbreviation = 'cfs'),
    102: TestUnits(
        UnitsID = 102,
        UnitsName = 'minute',
        UnitsType = 'Time',
        UnitsAbbreviation = 'min'),
    199: TestUnits(
        UnitsID = 199,
        UnitsName = 'milligrams per liter',
        UnitsType = 'Concentration',
        UnitsAbbreviation = 'mg/L'),
    52: TestUnits(
        UnitsID = 52,
        UnitsName = 'meter',
        UnitsType = 'Length',
        UnitsAbbreviation = 'm'),
    }

test_variables = {
    'Temp': TestVariable(
        VariableID = 1,
        VariableCode = 'Temp',
        VariableName = 'Temperature',
        VariableUnitsID = 96,
        VariableUnits = test_units[96],
        SampleMedium = 'Surface Water',
        ValueType = 'Field Observation',
        IsRegular = True,
        TimeSupport = 0,
        TimeUnitsID = 100,
        TimeUnits = test_units[100],
        DataType = 'Continuous',
        GeneralCategory = 'Water Quality',
        NoDataValue = -9999,
        VariableDescription = None),
    'Flow': TestVariable(
        VariableID = 2,
        VariableCode = 'Flow',
        VariableName = 'Discharge',
        VariableUnitsID = 35,
        VariableUnits = test_units[35],
        SampleMedium = 'Surface Water',
        ValueType = 'Field Observation',
        IsRegular = True,
        TimeSupport = 15,
        TimeUnitsID = 102,
        TimeUnits = test_units[102],
        DataType = 'Average',
        GeneralCategory = 'Hydrology',
        NoDataValue = -9999,
        VariableDescription = 'Average streamflow'),
    'TP': TestVariable(
        VariableID = 3,
        VariableCode = 'TP',
        VariableName = 'Phosphorus, total as P',
        VariableUnitsID = 199,
        VariableUnits = test_units[199],
        SampleMedium = 'Surface Water',
        ValueType = 'Sample',
        IsRegular = False,
        TimeSupport = 0,
        TimeUnitsID = 100,
        TimeUnits = test_units[100],
        DataType = 'Sporadic',
        GeneralCategory = 'Water Quality',
        NoDataValue = -9999,
        VariableDescription = None)
    }

test_methods = {
    5: TestMethod(
        MethodID = 5,
        MethodDescription = 'Temperature measured using a sensor.',
        MethodLink = 'http://www.campbellsci.com/'),
    26: TestMethod(
        MethodID = 26,
        MethodDescription = 'USGS real time streamflow gage.',
        MethodLink = 'http://waterdata.usgs.gov'),
    25: TestMethod(
        MethodID = 25,
        MethodDescription = 'Grab sample collected by smurfs in the field.',
        MethodLink = None)
    }

test_metadata = {
    1: TestMetadata(
        MetadataID = 1,
        TopicCategory = 'inlandWaters',
        Title = 'Good Title',
        Abstract = 'Nice Abstract',
        ProfileVersion = 'Unknown',
        MetadataLink = 'http://www.unknown.edu')
    }

test_sources = {
    1: TestSource(
        SourceID = 1,
        Organization = 'Thundercats',
        SourceDescription = 'Likes defeating evil; also likes milk',
        SourceLink = 'http://www.thundercats.edu',
        ContactName = 'Snarf',
        Phone = '555-555-5555',
        Email = 'snarf@gocats.outerspace',
        Address = 'Thundercats Lair',
        City = 'Meow City',
        State = 'Thundera',
        ZipCode = '23487',
        MetadataID = 1,
        Metadata = test_metadata[1])
    }

test_series = {
    'Temp': TestSeries(
        SeriesID = 1,
        Site = test_sites['SITE_A'],
        SiteID = test_sites['SITE_A'].SiteID,
        SiteCode = test_sites['SITE_A'].SiteCode,
        SiteName = test_sites['SITE_A'].SiteName,
        Variable = test_variables['Temp'],
        VariableID = test_variables['Temp'].VariableID,
        VariableCode = test_variables['Temp'].VariableCode,
        VariableName = test_variables['Temp'].VariableName,
        VariableUnitsID = test_variables['Temp'].VariableUnitsID,
        VariableUnitsName = test_units[96].UnitsName,
        SampleMedium = test_variables['Temp'].SampleMedium,
        ValueType = test_variables['Temp'].ValueType,
        TimeSupport = test_variables['Temp'].TimeSupport,
        TimeUnitsID = test_variables['Temp'].TimeUnitsID,
        TimeUnitsName = test_variables['Temp'].TimeUnits.UnitsName,
        DataType = test_variables['Temp'].DataType,
        GeneralCategory = test_variables['Temp'].GeneralCategory,
        Method = test_methods[5],
        MethodID = test_methods[5].MethodID,
        MethodDescription = test_methods[5].MethodDescription,
        Source = test_sources[1],
        SourceID = test_sources[1].SourceID,
        Organization = test_sources[1].Organization,
        SourceDescription = test_sources[1].SourceDescription,
        QualityControlLevelID = 1,
        QualityControlLevelCode = "QC'd",
        BeginDateTime = parse('2007-04-05T00:00-06'),
        EndDateTime = parse('2007-04-06T00:00-06'),
        BeginDateTimeUTC =  parse('2007-04-05T06:00Z'),
        EndDateTimeUTC =  parse('2007-04-06T06:00Z'),
        ValueCount = 2),
    'Flow': TestSeries(
        SeriesID = 2,
        Site = test_sites['SITE_A'],
        SiteID = test_sites['SITE_A'].SiteID,
        SiteCode = test_sites['SITE_A'].SiteCode,
        SiteName = test_sites['SITE_A'].SiteName,
        Variable = test_variables['Flow'],
        VariableID = test_variables['Flow'].VariableID,
        VariableCode = test_variables['Flow'].VariableCode,
        VariableName = test_variables['Flow'].VariableName,
        VariableUnitsID = test_variables['Flow'].VariableUnitsID,
        VariableUnitsName = test_units[35].UnitsName,
        SampleMedium = test_variables['Flow'].SampleMedium,
        ValueType = test_variables['Flow'].ValueType,
        TimeSupport = test_variables['Flow'].TimeSupport,
        TimeUnitsID = test_variables['Flow'].TimeUnitsID,
        TimeUnitsName = test_variables['Flow'].TimeUnits.UnitsName,
        DataType = test_variables['Flow'].DataType,
        GeneralCategory = test_variables['Flow'].GeneralCategory,
        Method = test_methods[26],
        MethodID = test_methods[26].MethodID,
        MethodDescription = test_methods[26].MethodDescription,
        Source = test_sources[1],
        SourceID = test_sources[1].SourceID,
        Organization = test_sources[1].Organization,
        SourceDescription = test_sources[1].SourceDescription,
        QualityControlLevelID = 1,
        QualityControlLevelCode = "QC'd",
        BeginDateTime = parse('2007-04-05T00:00-06'),
        EndDateTime = parse('2007-04-05T00:00-06'),
        BeginDateTimeUTC =  parse('2007-04-05T06:00Z'),
        EndDateTimeUTC =  parse('2007-04-05T06:00Z'),
        ValueCount = 1),
    'TP': TestSeries(
        SeriesID = 3,
        Site = test_sites['SITE_B'],
        SiteID = test_sites['SITE_B'].SiteID,
        SiteCode = test_sites['SITE_B'].SiteCode,
        SiteName = test_sites['SITE_B'].SiteName,
        Variable = test_variables['TP'],
        VariableID = test_variables['TP'].VariableID,
        VariableCode = test_variables['TP'].VariableCode,
        VariableName = test_variables['TP'].VariableName,
        VariableUnitsID = test_variables['TP'].VariableUnitsID,
        VariableUnitsName = test_units[199].UnitsName,
        SampleMedium = test_variables['TP'].SampleMedium,
        ValueType = test_variables['TP'].ValueType,
        TimeSupport = test_variables['TP'].TimeSupport,
        TimeUnitsID = test_variables['TP'].TimeUnitsID,
        TimeUnitsName = test_variables['TP'].TimeUnits.UnitsName,
        DataType = test_variables['TP'].DataType,
        GeneralCategory = test_variables['TP'].GeneralCategory,
        Method = test_methods[25],
        MethodID = test_methods[25].MethodID,
        MethodDescription = test_methods[25].MethodDescription,
        Source = test_sources[1],
        SourceID = test_sources[1].SourceID,
        Organization = test_sources[1].Organization,
        SourceDescription = test_sources[1].SourceDescription,
        QualityControlLevelID = 1,
        QualityControlLevelCode = "QC'd",
        BeginDateTime = parse('2007-04-05T00:00-06'),
        EndDateTime = parse('2007-04-06T00:00-06'),
        BeginDateTimeUTC =  parse('2007-04-05T06:00Z'),
        EndDateTimeUTC =  parse('2007-04-06T06:00Z'),
        ValueCount = 2)
    }

test_qualifiers = {
    1: TestQualifier(
        QualifierID = 1,
        QualifierCode = 'USU-I',
        QualifierDescription = 'Value made up from thin air')
    }

test_offset_types = {
    1: TestOffsetType(
        OffsetTypeID = 1,
        OffsetUnitsID = test_units[52].UnitsID,
        OffsetDescription = 'Distance below water surface',
        OffsetUnits = test_units[52])
    }

test_datavalues = {
    'Temp1': TestDataValue(
        ValueID = 1,
        DataValue = 8.4,
        ValueAccuracy = None,
        LocalDateTime = parse('2007-04-05T00:00-06'),
        UTCOffset = -6,
        DateTimeUTC = parse('2007-04-05T06:00Z'),
        SiteID = 1,
        VariableID = 1,
        OffsetValue = 2.4,
        OffsetTypeID = 1,
        CensorCode = 'nc',
        QualifierID = None,
        MethodID = 5,
        SourceID = 1,
        SampleID = None,
        QualityControlLevel = 'QC Definition',
        QualityControlLevelID = 1),
    'Temp2': TestDataValue(
        ValueID = 2,
        DataValue = 10.4,
        ValueAccuracy = None,
        LocalDateTime = parse('2007-04-06T00:00-06'),
        UTCOffset = -6,
        DateTimeUTC = parse('2007-04-06T06:00Z'),
        SiteID = 1,
        VariableID = 1,
        OffsetValue = 2.5,
        OffsetTypeID = 1,
        CensorCode = 'nc',
        QualifierID = 1,
        MethodID = 5,
        SourceID = 1,
        SampleID = None,
        QualityControlLevel = 'QC Definition',
        QualityControlLevelID = 1),
    'Flow1': TestDataValue(
        ValueID = 3,
        DataValue = 110.2,
        ValueAccuracy = .8,
        LocalDateTime = parse('2007-04-05T00:00-06'),
        UTCOffset = -6,
        DateTimeUTC = parse('2007-04-05T06:00Z'),
        SiteID = 1,
        VariableID = 2,
        OffsetValue = None,
        OffsetTypeID = None,
        CensorCode = 'nc',
        QualifierID = None,
        MethodID = 26,
        SourceID = 1,
        SampleID = None,
        QualityControlLevel = 'QC Definition',
        QualityControlLevelID = 1),
    'TP1': TestDataValue(
        ValueID = 4,
        DataValue = .02,
        ValueAccuracy = None,
        LocalDateTime = parse('2007-04-05T00:00-06'),
        UTCOffset = -6,
        DateTimeUTC = parse('2007-04-05T06:00Z'),
        SiteID = 2,
        VariableID = 3,
        OffsetValue = None,
        OffsetTypeID = None,
        CensorCode = 'nc',
        QualifierID = None,
        MethodID = 25,
        SourceID = 1,
        SampleID = None,
        QualityControlLevel = 'QC Definition',
        QualityControlLevelID = 1),
    'TP2': TestDataValue(
        ValueID = 5,
        DataValue = .05,
        ValueAccuracy = None,
        LocalDateTime = parse('2007-04-06T00:00-06'),
        UTCOffset = -6,
        DateTimeUTC = parse('2007-04-06T06:00Z'),
        SiteID = 2,
        VariableID = 3,
        OffsetValue = None,
        OffsetTypeID = None,
        CensorCode = 'nc',
        QualifierID = None,
        MethodID = 25,
        SourceID = 1,
        SampleID = 101,
        QualityControlLevel = 'QC Definition',
        QualityControlLevelID = 1)
    }

class TestDao(dao.BaseDao):
    def get_all_sites(self):
        return test_sites.values()

    def get_sites_by_codes(self, site_codes):
        return [test_sites[site_code] for site_code in site_codes]

    def get_all_variables(self):
        return test_variables.values()

    def get_variable_by_code(self, variable_code):
        return self.get_variables_by_codes([variable_code])[0]

    def get_variables_by_codes(self, variable_codes):
        return [test_variables[var_code] for var_code in variable_codes]

    def get_site_by_code(self, site_code):
        return test_sites[site_code]

    def get_series_by_sitecode(self, site_code):
        series_catalog = test_series.iteritems()
        return [v for k, v in series_catalog if v.SiteCode == site_code]

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        series_catalog = test_series.iteritems()
        return [v for k, v in series_catalog if v.SiteCode == site_code and
                v.VariableCode == var_code]

    def get_utc_datetime(self, date_string):
        local_date = parse(date_string)
        utc_time_zone = parse('2001-01-01T00Z').tzinfo
        if local_date.tzinfo:
            return local_date.astimezone(utc_time_zone)
        else:
            # No time zone supplied.  Assume local time (UTC-6)
            local_date = local_date + timedelta(hours=6)
            return local_date.replace(tzinfo=utc_time_zone)

    def datavalue_in_date_range(self, datavalue, begin_date_time,
                                end_date_time):

        if not begin_date_time:
            start_date = parse(dt(MINYEAR, 1, 1).isoformat() + 'Z')
        else:
            start_date = self.get_utc_datetime(begin_date_time)            
        if not end_date_time:
            end_date = parse(dt(MAXYEAR, 12, 31).isoformat() + 'Z')
        else:
            end_date = self.get_utc_datetime(end_date_time)            
            
        value_time = datavalue.DateTimeUTC

        return (value_time >= start_date and value_time <= end_date)
    
    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        vals = test_datavalues.iteritems()
        site_id = test_sites[site_code].SiteID
        var_id = test_variables[var_code].VariableID
        vals = [v for k, v in vals if v.SiteID == site_id and
                v.VariableID == var_id and
                self.datavalue_in_date_range(v,
                                             begin_date_time,
                                             end_date_time)]
        import operator
        vals.sort(key=operator.attrgetter('DateTimeUTC'))
        return vals

    def get_methods_by_ids(self, method_id_arr):
        return [test_methods[id] for id in method_id_arr]

    def get_sources_by_ids(self, source_id_arr):
        return [test_sources[id] for id in source_id_arr]

    def get_qualifiers_by_ids(self, qualifier_id_arr):
        return [test_qualifiers[id] for id in qualifier_id_arr]

    def get_offsettypes_by_ids(self, offset_type_id_arr):
        return [test_offset_types[id] for id in offset_type_id_arr]
    