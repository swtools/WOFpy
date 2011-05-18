import StringIO
import logging
import soaplib #soaplib 2.0.0-beta

import wofpy_soap

from soaplib.core.model.base import Base
from soaplib.core.service import rpc, soap, DefinitionBase
from soaplib.core.model.primitive import String, Any, Integer, Float
from soaplib.core.model.exception import Fault
from soaplib.core.model.clazz import Array, ClassModel

logger = logging.getLogger(__name__)

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'

#TODO: Input validation, error messages, test classes (use suds)
#TODO: For some reason, soaplib does not ignore <!--comments--> in the soap 
# requests so the default requests from soapUI will cause errors

def create_wof_service_class(wof_instance):
    class WOFService(DefinitionBase):
    
        wof_inst = wof_instance
          
        @soap(Array(String), String, _returns=Any)
        def GetSites(self, site, authToken):
            
            siteArg = ','.join(str(s) for s in site)
             
            logging.debug(site)
            logging.debug(siteArg)
            
            siteResponse = self.wof_inst.create_get_site_response(siteArg)
            outStream = StringIO.StringIO()
            siteResponse.export(outStream, 0, name_="sitesResponse",
                                namespacedef_= NSDEF)
            
            #TODO: Fault
            
            return outStream.getvalue()
        
        @soap(Array(String), String, _returns=String)
        def GetSitesXml(self, site, authToken): #This is the one that returns WITH <![CDATA[...]]>
            
            siteArg = ','.join(str(s) for s in site)
            
            siteResponse = self.wof_inst.create_get_site_response(siteArg)
       
            outStream = StringIO.StringIO()
            siteResponse.export(outStream, 0, name_="sitesResponse",
                                namespacedef_= NSDEF)
            
            #TODO: Fault
            
            return str(outStream.getvalue()).replace('\n','')
        
        #######################################################################
        
        @soap(String, String, _returns=String)
        def GetSiteInfo(self,site,authToken):
            
            try:
                siteInfoResponse = \
                            self.wof_inst.create_get_site_info_response(site)
                
                outStream = StringIO.StringIO()
                siteInfoResponse.export(outStream, 0, name_="siteInfoResponse",
                                        namespacedef_= NSDEF)
                
                #TODO: Fault
             
                return str(outStream.getvalue()).replace('\n','')
            
            except Exception as inst:
                return "ERROR: %s, %s" % (type(inst), inst)
        
        @soap(String, String, _returns=Any)
        def GetSiteInfoObject(self,site,authToken):
            
            try:
                siteInfoResponse = \
                            self.wof_inst.create_get_site_info_response(site)
            
                outStream = StringIO.StringIO()
                siteInfoResponse.export(outStream, 0, name_="siteInfoResponse",
                                    namespacedef_= NSDEF)
            
                #TODO: Fault
         
                return outStream.getvalue()
            
            except Exception as inst:
                return "ERROR: %s, %s" % (type(inst), inst)
        
        #######################################################################
        
        @soap(String, String, _returns=String)
        def GetVariableInfo(self, variable, authToken):
            
            variableInfoResponse = \
                    self.wof_inst.create_get_variable_info_response(variable)
            
            outStream = StringIO.StringIO()
            variableInfoResponse.export(outStream, 0,
                                        name_="variablesResponse",
                                        namespacedef_= NSDEF)
            
            #TODO: Fault
            
            return str(outStream.getvalue()).replace('\n','')
        
        @soap(String, String, _returns=Any)
        def GetVariableInfoObject(self, variable, authToken):
            
            variableInfoResponse = \
                    self.wof_inst.create_get_variable_info_response(variable)
            
            outStream = StringIO.StringIO()
            variableInfoResponse.export(outStream, 0,
                                        name_="variablesResponse",
                                        namespacedef_= NSDEF)
            
            #TODO: Fault
            
            return outStream.getvalue()
        
        #######################################################################
    
        @soap(String, String, String, String, _returns=String)
        def GetValues(self, location, variable, startDate, endDate):
            
            timeSeriesResponse = self.wof_inst.create_get_values_response(
                location,variable,startDate,endDate)
               
            outStream = StringIO.StringIO()
            timeSeriesResponse.export(outStream, 0, name_="timeSeriesResponse",
                                      namespacedef_= NSDEF)
            
            #TODO: Fault
            
            return str(outStream.getvalue()).replace('\n','')
        
        @soap(String, String, String, String, _returns=Any)
        def GetValuesObject(self, location, variable, startDate, endDate):
            
            timeSeriesResponse = self.wof_inst.create_get_values_response(
                location,variable,startDate,endDate)
               
            outStream = StringIO.StringIO()
            timeSeriesResponse.export(outStream, 0, name_="timeSeriesResponse",
                                      namespacedef_= NSDEF)
            
            #TODO: Fault
            
            return outStream.getvalue()
      
    return WOFService  
