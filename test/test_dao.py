from wof import dao, models


class TestSite(models.BaseSite):
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


test_sites = {
    'SITE_A': TestSite(
        SiteID='1',
        SiteCode='SITE_A',
        SiteName='Site A',
        Latitude=50,
        Longitude=60),
    'SITE_B': TestSite(
        SiteID='2',
        SiteCode='SITE_B',
        SiteName='Site B',
        Latitude=55,
        Longitude=-13),
    'SITE_C': TestSite(
        SiteID='3',
        SiteCode='SITE_C',
        SiteName='Site C',
        Latitude=59,
        Longitude=10),
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
        UnitsAbbreviation = 'mg/L')
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

class TestDao(dao.BaseDao):
    def get_all_sites(self):
        return test_sites.values()

    def get_sites_by_codes(self, site_codes):
        return [test_sites[site_code] for site_code in site_codes]

    def get_all_variables(self):
        return test_variables.values()

    def get_variables_by_codes(self, variable_codes):
        return [test_variables[variable_code] for variable_code in variable_codes]
