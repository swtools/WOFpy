import wof.models as wof_base


class DataValue(wof_base.BaseDataValue):

    def __init__(self, data_value, date_time_utc, site_id,
                 variable_id):
        self.DataValue = data_value
        self.DateTimeUTC = date_time_utc
        self.SiteID = site_id
        self.VariableID = variable_id

    #UTCOffset = None
    #OffsetValue = None
    #OffsetTypeID = None
    #CensorCode = None
    #QualifierID = None
    #MethodID = None
    #SourceID = None
    #SampleID = None=
    #QualityControlLevel = None
    #QualityControlLevelID = None


class Source(wof_base.BaseSource):
    pass
