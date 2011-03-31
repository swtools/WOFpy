from wof.code import *
from wof import NSDEF

import StringIO

import soaplib #soaplib 2.0.0-beta
from soaplib.core.service import rpc, soap, DefinitionBase
from soaplib.core.model.primitive import *
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import *
    

class WOFService(DefinitionBase):
        
    @rpc(Array(String), String, _returns=Any)
    def GetSites(self, site, authToken):
        
        siteArg = ','.join(str(s) for s in site)
            
        siteResponse = create_get_site_response(siteArg)
   
        outStream = StringIO.StringIO()
        siteResponse.export(outStream, 0, name_="sitesResponse", namespacedef_= NSDEF)
        
        return outStream.getvalue()
    
    @rpc(Array(String), String, _returns=String)
    def GetSitesXml(self, site, authToken): #This is the one that returns WITH <![CDATA[...]]>
        
        siteArg = ','.join(str(s) for s in site)
        
        siteResponse = create_get_site_response(siteArg)
   
        outStream = StringIO.StringIO()
        siteResponse.export(outStream, 0, name_="sitesResponse", namespacedef_= NSDEF)
        
        return str(outStream.getvalue()).replace('\n','')
    
    ############################################################################
    
    @rpc(String, String, _returns=String)
    def GetSiteInfo(self,site,authToken):
        
        siteInfoResponse = create_get_site_info_response(site)
        
        outStream = StringIO.StringIO()
        siteInfoResponse.export(outStream, 0, name_="siteInfoResponse", namespacedef_= NSDEF)
     
        return str(outStream.getvalue()).replace('\n','')
    
    @rpc(String, String, _returns=Any)
    def GetSiteInfoObject(self,site,authToken):
        
        siteInfoResponse = create_get_site_info_response(site)
        
        outStream = StringIO.StringIO()
        siteInfoResponse.export(outStream, 0, name_="siteInfoResponse", namespacedef_= NSDEF)
     
        return outStream.getvalue()
    
    ############################################################################
    
    @rpc(String, String, _returns=String)
    def GetVariableInfo(self, variable, authToken):
        
        variableInfoResponse = create_variable_info_response(variable)
        
        outStream = StringIO.StringIO()
        variableInfoResponse.export(outStream, 0, name_="variablesResponse", namespacedef_= NSDEF)
        
        return str(outStream.getvalue()).replace('\n','')
    
    @rpc(String, String, _returns=Any)
    def GetVariableInfoObject(self, variable, authToken):
        
        variableInfoResponse = create_variable_info_response(variable)
        
        outStream = StringIO.StringIO()
        variableInfoResponse.export(outStream, 0, name_="variablesResponse", namespacedef_= NSDEF)
        
        return outStream.getvalue()
    
    ############################################################################

    @rpc(String, String, String, String, _returns=String)
    def GetValues(self, location, variable, startDate, endDate):
        
        timeSeriesResponse = create_get_values_response(location,variable,startDate,endDate)
           
        outStream = StringIO.StringIO()
        timeSeriesResponse.export(outStream, 0, name_="timeSeriesResponse", namespacedef_= NSDEF)
        
        return str(outStream.getvalue()).replace('\n','')
    
    @rpc(String, String, String, String, _returns=Any)
    def GetValuesObject(self, location, variable, startDate, endDate):
        
        timeSeriesResponse = create_get_values_response(location,variable,startDate,endDate)
           
        outStream = StringIO.StringIO()
        timeSeriesResponse.export(outStream, 0, name_="timeSeriesResponse", namespacedef_= NSDEF)
        
        return outStream.getvalue()
    
