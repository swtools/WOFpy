import StringIO
import logging
import soaplib #soaplib 2.0.0-beta
import datetime

import wof.code

from soaplib.core.model.base import Base
from soaplib.core.service import rpc, soap, DefinitionBase
from soaplib.core.model.primitive import (String, Any, Integer, Float,
                                          DateTime, Boolean, Double)
from soaplib.core.model.clazz import Array, ClassModel, XMLAttribute
from soaplib.core.model.enum import Enum, EnumBase


logger = logging.getLogger(__name__)

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'


class WaterMLTypeBase(ClassModel):
    __namespace__ = "http://www.cuahsi.org/waterML/1.0/"



class Criteria(WaterMLTypeBase):
    locationParam = String
    variableParam = String
    timeParam = Any #type is not defined in WML1
  
class Note(WaterMLTypeBase):
    type = XMLAttribute('xs:string')
    href = XMLAttribute('xs:string')
    title = XMLAttribute('xs:string')
    show = XMLAttribute('xs:string')
    
    #What about the value of the element?
    
class QueryInfoType(WaterMLTypeBase):
    
    creationTime = DateTime
    queryURL = String
    querySQL = String
    
    criteria = Criteria
    
    note = Array(Note)
    #extension
    
    
class GeogLocationType(WaterMLTypeBase):
    srs = XMLAttribute

class LatLonBoxType(GeogLocationType):
    pass

class LatLonPointType(GeogLocationType):
    latitude = Double
    longitude = Double

class SiteCode(String):
    defaultId = XMLAttribute('xs:boolean')
    #network = XMLAttribute('xs:normalizedString')
    #siteID = XMLAttribute('xs:normalizedString')
    #agencyCode = XMLAttribute('xs:normalizedString')
    #agencyName = XMLAttribute('xs:normalizedString')

class SourceInfoType(WaterMLTypeBase):
    siteName = String
    siteCode = SiteCode
    

class SiteInfoType(SourceInfoType):
    siteName = String
    sitecode = String
    defaultId = Boolean
    geoLocation = GeogLocationType
    
class SiteInfoResponseType(WaterMLTypeBase):

    queryInfo = QueryInfoType
    site = Array(SiteInfoType) #site is an Array of elements with siteInfo, 0..* seriesCatalog and, extension






class DataSetInfoType(WaterMLTypeBase):
    pass


class VariableInfoType(WaterMLTypeBase):
    pass

dataTypeEnum = Enum(

    'Continuous',
    'Instantaneous',
    'Cumulative',
    'Incremental',
    'Average',
    'Maximum',
    'Minimum',
    'Constant Over Interval',
    'Categorical',
    'Best Easy Systematic Estimator',
    'Unknown',
    'Variance',
    type_name = 'dataTypeEnum'
)

class series(WaterMLTypeBase):
    dataType = dataTypeEnum #? is this how to do it?
    variable = VariableInfoType
    valueCount = Integer #this has a 'countIsEstimated' boolean attribute
    variableTimeInterval = TimePeriodType
    valueType = valueTypeEnum
    generalCategory = generalCategoryEnum
    sampleMedium = SampleMediumEnum
    Method = MthodType
    Source = SourceType
    QualityControlLevel = QualityControlLevelType
    menuGroupName = XMLAttribute('xs:string')
    serviceWsdl = XMLAttribute('xs:anyURI')

class seriesCatalogType(WaterMLTypeBase):
    note = Array(Note)
    
class ArrayOfOption(WaterMLTypeBase):
    pass

class UnitsType(WaterMLTypeBase):
    pass

class TimePeriodType(WaterMLTypeBase):
    pass

class TimeIntervalType(WaterMLTypeBase):
    pass

class TimeSingleType(WaterMLTypeBase):
    pass

class TimePeriodRealTimeType(WaterMLTypeBase):
    pass

class MethodType(WaterMLTypeBase):
    pass

class SourceType(WaterMLTypeBase):
    pass

class MetaDataType(WaterMLTypeBase):
    pass

class ContactInformationType(WaterMLTypeBase):
    pass

class QualityControlLevelType(WaterMLTypeBase):
    pass

class VariablesResponseType(WaterMLTypeBase):
    pass

class ArrayOfVariableInfoType(WaterMLTypeBase):
    pass

class TimeSeriesResponseType(WaterMLTypeBase):
    pass

class TimeSeriesType(WaterMLTypeBase):
    pass

class TsValuesSingleVariableType(WaterMLTypeBase):
    pass

class ValueSingleVariable(WaterMLTypeBase):
    pass

class OffsetType(WaterMLTypeBase):
    pass


class WOFService(DefinitionBase):
        
    @soap(_returns=SiteInfoResponseType)
    def TestMethod(self):
        s = SiteInfoResponseType()
        s.queryInfo = QueryInfoType()
        
        s.queryInfo.creationTime = datetime.datetime(1984,2,11)
        s.queryInfo.querySQL = 'www.url.com'
        s.querySQL = 'query sql'
        
        s.criteria = Criteria()
        s.criteria.locationParam = "here"
        s.criteria.variableParam = "variable"
        
        
        
        return s
        
    @soap(Array(String), String, _returns=Any)
    def GetSites(self, site, authToken):
        
        siteArg = ','.join(str(s) for s in site)
        
        logging.debug(site)
        logging.debug(siteArg)
        
        
        siteResponse = wof.code.create_get_site_response(siteArg)
        outStream = StringIO.StringIO()
        siteResponse.export(outStream, 0, name_="sitesResponse",
                            namespacedef_= NSDEF)
        
        return outStream.getvalue()
    
    @soap(Array(String), String, _returns=String)
    def GetSitesXml(self, site, authToken): #This is the one that returns WITH <![CDATA[...]]>
        
        siteArg = ','.join(str(s) for s in site)
        
        siteResponse = wof.code.create_get_site_response(siteArg)
   
        outStream = StringIO.StringIO()
        siteResponse.export(outStream, 0, name_="sitesResponse",
                            namespacedef_= NSDEF)
        
        return str(outStream.getvalue()).replace('\n','')
    
    ###########################################################################
    
    @soap(String, String, _returns=String)
    def GetSiteInfo(self,site,authToken):
        
        siteInfoResponse = wof.code.create_get_site_info_response(site)
        
        outStream = StringIO.StringIO()
        siteInfoResponse.export(outStream, 0, name_="siteInfoResponse",
                                namespacedef_= NSDEF)
     
        return str(outStream.getvalue()).replace('\n','')
    
    @soap(String, String, _returns=Any)
    def GetSiteInfoObject(self,site,authToken):
        
        siteInfoResponse = wof.code.create_get_site_info_response(site)
        
        outStream = StringIO.StringIO()
        siteInfoResponse.export(outStream, 0, name_="siteInfoResponse",
                                namespacedef_= NSDEF)
     
        return outStream.getvalue()
    
    ###########################################################################
    
    @soap(String, String, _returns=String)
    def GetVariableInfo(self, variable, authToken):
        
        variableInfoResponse = wof.code.create_variable_info_response(variable)
        
        outStream = StringIO.StringIO()
        variableInfoResponse.export(outStream, 0, name_="variablesResponse",
                                    namespacedef_= NSDEF)
        
        return str(outStream.getvalue()).replace('\n','')
    
    @soap(String, String, _returns=Any)
    def GetVariableInfoObject(self, variable, authToken):
        
        variableInfoResponse = wof.code.create_variable_info_response(variable)
        
        outStream = StringIO.StringIO()
        variableInfoResponse.export(outStream, 0, name_="variablesResponse",
                                    namespacedef_= NSDEF)
        
        return outStream.getvalue()
    
    ###########################################################################

    @soap(String, String, String, String, _returns=String)
    def GetValues(self, location, variable, startDate, endDate):
        
        timeSeriesResponse = wof.code.create_get_values_response(
            location,variable,startDate,endDate)
           
        outStream = StringIO.StringIO()
        timeSeriesResponse.export(outStream, 0, name_="timeSeriesResponse",
                                  namespacedef_= NSDEF)
        
        return str(outStream.getvalue()).replace('\n','')
    
    @soap(String, String, String, String, _returns=Any)
    def GetValuesObject(self, location, variable, startDate, endDate):
        
        timeSeriesResponse = wof.code.create_get_values_response(
            location,variable,startDate,endDate)
           
        outStream = StringIO.StringIO()
        timeSeriesResponse.export(outStream, 0, name_="timeSeriesResponse",
                                  namespacedef_= NSDEF)
        
        return outStream.getvalue()
    
