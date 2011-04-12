import StringIO
import logging
import soaplib #soaplib 2.0.0-beta
import datetime

import wof.code

from soaplib.core.model.base import Base
from soaplib.core.service import rpc, soap, DefinitionBase
from soaplib.core.model.primitive import String, Any, Integer, Float, DateTime
from soaplib.core.model.primitive import Boolean, Double
from soaplib.core.model.clazz import Array, ClassModel, XMLAttribute


logger = logging.getLogger(__name__)

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'

class WaterMLTypeBase(ClassModel):
    __namespace__ = "http://www.cuahsi.org/waterML/1.0/"

class QueryInfoType(WaterMLTypeBase):
   
    #aaa = XMLAttribute(String)
    
    creationTime = DateTime
    queryURL = String
    querySQL = String
    #criteria
    #note
    #extension
    
    
class GeogLocationType(WaterMLTypeBase):
    srs = XMLAttribute

class LatLonBoxType(GeogLocationType):
    pass

class LatLonPointType(GeogLocationType):
    latitude = Double
    longitude = Double
    
class SiteInfoResponseType(WaterMLTypeBase):
    #__namespace__ = 'abc'
    #__type_name__ = 'def'
    queryInfo = QueryInfoType
    #site = site is an Array of elements with siteInfo, 0..* seriesCatalog and, extension

class SourceInfoType(WaterMLTypeBase):
    pass

class SiteInfoType(SourceInfoType):
    siteName = String
    sitecode = String
    defaultId = Boolean
    geoLocation = GeogLocationType


class DataSetInfoType(WaterMLTypeBase):
    pass


class seriesCatalogType(WaterMLTypeBase):
    pass

class VariableInfoType(WaterMLTypeBase):
    pass

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
        
        s.queryInfo.aaa = "hi james"
        s.queryInfo.creationTime = datetime.datetime(1984, 2, 11)
        s.queryInfo.queryURL = "www.james.com"
        s.queryInfo.querySQL = ''
        
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
    
