import datetime

from sqlalchemy import (Table, Column, Integer, String, ForeignKey, Float,
                        DateTime, Boolean, )

from sqlalchemy.sql import join, select, func, label
from sqlalchemy.orm import mapper, relationship, column_property
from sqlalchemy.ext.declarative import declarative_base

import wof.models as wof_base

Base = declarative_base()


def init_model(db_session):
    Base.query = db_session.query_property()

#TODO: Andy, please check
param_to_medium_dict = {
    'water_ph': wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_y_velocity': wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_x_velocity': wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_temperature': wof_base.SampleMediumTypes.SURFACE_WATER,
    'upward_water_velocity': wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_turbidity': wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_total_dissolved_salts': wof_base.SampleMediumTypes.SURFACE_WATER,
    'seawater_salinity': wof_base.SampleMediumTypes.SURFACE_WATER,
    'northward_water_velocity': wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_electrical_conductivity': wof_base.SampleMediumTypes.SURFACE_WATER,
    'eastward_water_velocity': wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_dissolved_oxygen_percent_saturation':
        wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_dissolved_oxygen_concentration':
        wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_depth_vented': wof_base.SampleMediumTypes.SURFACE_WATER,
    'water_depth_non_vented': wof_base.SampleMediumTypes.SURFACE_WATER,
    'instrument_battery_voltage': wof_base.SampleMediumTypes.NOT_RELEVANT,
    'air_pressure': wof_base.SampleMediumTypes.AIR,
    'air_temperature': wof_base.SampleMediumTypes.AIR,
    'water_specific_conductance': wof_base.SampleMediumTypes.SURFACE_WATER
}

#TODO: Andy, please check
param_to_gen_category_dict = {
    'water_ph': wof_base.GeneralCategoryTypes.WATER_QUALITY,
    'water_y_velocity': wof_base.GeneralCategoryTypes.HYDROLOGY,
    'water_x_velocity': wof_base.GeneralCategoryTypes.HYDROLOGY,
    'water_temperature': wof_base.GeneralCategoryTypes.WATER_QUALITY,
    'upward_water_velocity': wof_base.GeneralCategoryTypes.HYDROLOGY,
    'water_turbidity': wof_base.GeneralCategoryTypes.WATER_QUALITY,
    'water_total_dissolved_salts': wof_base.GeneralCategoryTypes.WATER_QUALITY,
    'seawater_salinity': wof_base.GeneralCategoryTypes.WATER_QUALITY,
    'northward_water_velocity': wof_base.GeneralCategoryTypes.HYDROLOGY,
    'water_electrical_conductivity':
        wof_base.GeneralCategoryTypes.WATER_QUALITY,
    'eastward_water_velocity': wof_base.GeneralCategoryTypes.HYDROLOGY,
    'water_dissolved_oxygen_percent_saturation':
        wof_base.GeneralCategoryTypes.WATER_QUALITY,
    'water_dissolved_oxygen_concentration':
        wof_base.GeneralCategoryTypes.WATER_QUALITY,
    'water_depth_vented': wof_base.GeneralCategoryTypes.HYDROLOGY,
    'water_depth_non_vented': wof_base.GeneralCategoryTypes.HYDROLOGY,
    'instrument_battery_voltage':
         wof_base.GeneralCategoryTypes.INSTRUMENTATION,
    'air_pressure': wof_base.GeneralCategoryTypes.CLIMATE,
    'air_temperature': wof_base.GeneralCategoryTypes.CLIMATE,
    'water_specific_conductance': wof_base.GeneralCategoryTypes.WATER_QUALITY
}


class Variable(Base, wof_base.BaseVariable):
    __tablename__ = 'parameter'

    VariableID = Column('id', Integer, primary_key=True)
    VariableCode = Column('parameter_code', String)
    VariableName = Column('parameter_description', String)
    IsRegular = False
    ValueType = "Field Observation"
    DataType = "Sporadic"
    NoDataValue = -9999

    @property
    def SampleMedium(self):
        if self.VariableCode in param_to_medium_dict:
            return param_to_medium_dict[self.VariableCode]
        return wof_base.SampleMediumTypes.UNKNOWN

    @property
    def GeneralCategory(self):
        if self.VariableCode in param_to_gen_category_dict:
            return param_to_gen_category_dict[self.VariableCode]
        return wof_base.GeneralCategoryTypes.UNKNOWN

    #TODO
    #VariableUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    #TimeSupport = Column(Float)
    #TimeUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))

    #TODO: Need Units table in the SWIS schema
    #VariableUnits = relationship("Units",
    #                            primaryjoin='Variable.VariableUnitsID==Units.UnitsID')

    #TimeUnits = relationship("Units",
    #                         primaryjoin='Variable.TimeUnitsID==Units.UnitsID')


class Site(Base, wof_base.BaseSite):
    __tablename__ = 'site'

    SiteID = Column('id', Integer, primary_key=True)
    SiteCode = Column('site_code', String)
    SiteName = Column('name', String)
    #Geom = GeometryColumn('geom', Point(2)) #TODO Andy

    @property
    def Latitude(self):
        #x, y = self.Geom.coords(db_session) #TODO Andy
        #return y
        return 0.0

    @property
    def Longitude(self):
        #x, y = self.Geom.coords(db_session) #TODO Andy
        #return x
        return 0.0

    #Elevation_m = Column(Float)
    #VerticalDatum = Column(String)

    #All sites are in WGS84
    LatLongDatum = wof_base.BaseSpatialReference()
    LatLongDatum.SRSID = 4326
    LatLongDatum.SRSName = "WGS84"


class DataValue(Base, wof_base.BaseDataValue):
    __tablename__ = 'raw_data_value'

    ValueID = Column('id', Integer, primary_key=True)
    DataValue = Column('data_value', Float)
    #UTCOffset = Column('origin_utc_offset', Integer)
    UTCOffset = 0 # TODO: add offset to datetimeutc to compute localdatetime
    DateTimeUTC = Column('datetime_utc', DateTime)
    LocalDateTime = DateTimeUTC
    SiteID = Column('site_id', Integer)
    VariableID = Column('parameter_id', Integer)
    OffsetValue = Column('vertical_offset', Float)
    #Data are non-censored TODO: Check if this is always the case
    CensorCode = "nc"

    #ValueAccuracy = Column(Float) #TODO
    #QualifierID = Column(Integer)
    #OffsetTypeID = Column(Integer)

    #Using Instrument information for the Method
    MethodID = Column('instrument_id', Integer, ForeignKey('Method.MethodID'))

    #Only have one Source for SWIS data
    SourceID = 1

    #All of SWIS data values are "raw data"
    QualityControlLevel = wof_base.QualityControlLevelTypes['RAW_DATA'][0]
    QualityControlLevelID = wof_base.QualityControlLevelTypes['RAW_DATA'][1]


#Using instrument information for Method of WaterML
class Method(Base, wof_base.BaseMethod):
    __tablename__ = 'instrument'

    MethodID = Column('id', Integer, primary_key=True)
    #MethodLink = None

    InstrumentModelID = Column('instrument_model_id', Integer,
                               ForeignKey('instrument_model.id'))

    InstrumentModel = relationship('InstrumentModel',
                            primaryjoin='Method.InstrumentModelID==\
                                        InstrumentModel.ModelID')

    @property
    def MethodDescription(self):
        if (self.InstrumentModel and
            self.InstrumentModel.InstrumentManufacturer):
            return "Measured with %s %s." % (
                self.InstrumentModel.InstrumentManufacturer.ManufacturerName,
                self.InstrumentModel.ModelName)
        else:
            return None


#SWIS-specific table
class InstrumentModel(Base):
    __tablename__ = 'instrument_model'

    ModelID = Column('id', Integer, primary_key=True)
    ModelName = Column('instrument_model_name', String)
    ManufacturerID = Column('instrument_manufacturer_id', Integer,
                            ForeignKey('instrument_manufacturer.id'))

    InstrumentManufacturer = relationship('InstrumentManufacturer',
                                primaryjoin='InstrumentModel.ManufacturerID==\
                                            InstrumentManufacturer.\
                                            ManufacturerID')


#SWIS-specific table
class InstrumentManufacturer(Base):
    __tablename__ = 'instrument_manufacturer'

    ManufacturerID = Column('id', Integer, primary_key=True)
    ManufacturerName = Column('instrument_manufacturer_name', String)


#Each site has an agency associated with it in
# the agency_site_association table
agency_site_association_table = Table(
    'agency_site_association',
    Base.metadata,
    Column('agency_id', Integer, ForeignKey('agency.id')),
    Column('site_id', Integer, ForeignKey('site.id')))


#TWDB is the Source/contact for all SWIS data
class Source(wof_base.BaseSource):
    SourceID = 1
    #TODO: Metadata
    Metadata = None


#TODO: Metadata
# Not a clear mapping.  project.name could be title,
# project.description could be abstract
#class Metadata(wof_base.BaseMetadata):
#    __tablename__='ISOMetadata'
#
#    MetadataID = Column(Integer, primary_key=True)
#    TopicCategory = Column(String)
#    Title = Column(String)
#    Abstract = Column(String)
#    ProfileVersion = Column(String)
#    MetadataLink = Column(String)

class Qualifier(wof_base.BaseQualifier):
    #TODO
    QualifierID = None
    QualifierCode = None
    QualifierDescription = None


#TODO  Looks like SWIS only has one type of offset, 'vertical_offset'
# but need to find out what the units will be
class OffsetType(wof_base.BaseOffsetType):
    OffsetTypeID = 1
    #TODO
    OffsetUnitsID = None
    OffsetDescription = "Vertical"
    #TODO
    OffsetUnits = None


class Series(wof_base.BaseSeries):

    def __init__(self, site=None, variable=None, value_count=None,
                 begin_date_time_utc=None, end_date_time_utc=None,
                 source=None):

        self.Site = site
        self.Variable = variable
        self.ValueCount = value_count
        self.BeginDateTimeUTC = begin_date_time_utc
        self.EndDateTimeUTC = end_date_time_utc
        self.BeginDateTime = begin_date_time_utc
        self.EndDateTime = end_date_time_utc

        #SWIS data are all "Raw Data"
        # though might have more than one QC level in the future
        self.QualityControlLevelID = \
                            wof_base.QualityControlLevelTypes['RAW_DATA'][1]
        self.QualityControlLevelCode = \
                            wof_base.QualityControlLevelTypes['RAW_DATA'][0]

        self.Source = source

    Source = None
    Variable = None
    Site = None
    Method = None
