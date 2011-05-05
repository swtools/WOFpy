import daos.base_models as wof_base

class DataValue(wof_base.BaseDataValue):
    
    def __init__(self, data_value, date_time_utc, offset_value, site_id,
                 variable_id):
        self.DataValue = data_value
        self.DateTimeUTC = date_time_utc
        self.OffsetValue = offset_value
        self.SiteID = site_id
        self.VariableID = variable_id
        
    #UTCOffset = None
    #OffsetValue = None
    #OffsetTypeID = None
    #CensorCode = None
    #QualifierID = None
    #MethodID = None
    #SourceID = None
    #SampleID = None
    #DerivedFromID = None
    #QualityControlLevel = None
    #QualityControlLevelID = None
    

class Variable(wof_base.BaseVariable):
    
    
    def __init__(self, variable_id, variable_code, variable_name):
        self.VariableID = variable_id
        self.VariableCode = variable_code
        self.VariableName = variable_name
    
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
    
    VariableUnits = None
    TimeUnits = None