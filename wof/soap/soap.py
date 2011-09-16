import StringIO
import logging
import soaplib

from lxml import etree
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

        def on_method_return_xml(self, element):
            # whatever etree element you return is the final xml
            # response, so to prevent the extraneous ("%sResult" %
            # method_name) result element, we just need to return an
            # element that has that element removed and replaced with
            # its child, which was the original response

            #TODO: how do we determine which method is being returned from?
            # Since I don't know, I am doing a dumb test for each one

            result_element_name_list = [
                'GetSitesResult',
                'GetSiteInfoObjectResult',
                'GetVariableInfoObjectResult',
                'GetValuesObjectResult']

            for result_element_name in result_element_name_list:
                result_element = element.find(
                    './/{%s}%s' % (element.nsmap['s0'], result_element_name))

                if result_element is not None:
                    parent = result_element.getparent()
                    children = result_element.getchildren()
                    parent.replace(result_element, children[0])
                    return element

            return element

        #_out_variable_names ????
        @soap(Array(String), String, _returns=Any)
        def GetSites(self, site, authToken):
            try:
                siteArg = ','.join(str(s) for s in site)
                logging.debug(site)
                logging.debug(siteArg)
                siteResponse = self.wof_inst.create_get_site_response(siteArg)
                outStream = StringIO.StringIO()
                siteResponse.export(outStream, 0, name_="sitesResponse",
                                    namespacedef_=NSDEF)
                return outStream.getvalue()

            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        # This is the one that returns WITH <![CDATA[...]]>
        @soap(Array(String), String, _returns=String)
        def GetSitesXml(self, site, authToken):
            try:
                siteArg = ','.join(str(s) for s in site)
                siteResponse = self.wof_inst.create_get_site_response(siteArg)
                outStream = StringIO.StringIO()
                siteResponse.export(outStream, 0, name_="sitesResponse",
                                    namespacedef_=NSDEF)
                return (outStream.getvalue()).replace('\n', '')

            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @soap(String, String, _returns=String)
        def GetSiteInfo(self, site, authToken):

            try:
                siteInfoResponse = \
                            self.wof_inst.create_get_site_info_response(site)
                outStream = StringIO.StringIO()
                siteInfoResponse.export(outStream, 0, name_="sitesResponse",
                                        namespacedef_=NSDEF)
                return (outStream.getvalue()).replace('\n', '')

            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @soap(String, String, _returns=Any)
        def GetSiteInfoObject(self, site, authToken):

            try:
                siteInfoResponse = \
                            self.wof_inst.create_get_site_info_response(site)
                outStream = StringIO.StringIO()
                siteInfoResponse.export(outStream, 0, name_="sitesResponse",
                                    namespacedef_=NSDEF)
                return outStream.getvalue()

            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @soap(String, String, _returns=String)
        def GetVariableInfo(self, variable, authToken):
            try:
                variableInfoResponse = \
                        self.wof_inst.create_get_variable_info_response(variable)
                outStream = StringIO.StringIO()
                variableInfoResponse.export(outStream, 0,
                                            name_="variablesResponse",
                                            namespacedef_=NSDEF)
                return (outStream.getvalue()).replace('\n', '')

            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @soap(String, String, _returns=Any)
        def GetVariableInfoObject(self, variable, authToken):
            try:
                variableInfoResponse = \
                        self.wof_inst.create_get_variable_info_response(variable)
                outStream = StringIO.StringIO()
                variableInfoResponse.export(outStream, 0,
                                            name_="variablesResponse",
                                            namespacedef_=NSDEF)
                return outStream.getvalue()

            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @soap(String, String, String, String, _returns=String)
        def GetValues(self, location, variable, startDate, endDate):
            try:
                timeSeriesResponse = self.wof_inst.create_get_values_response(
                    location, variable, startDate, endDate)
                outStream = StringIO.StringIO()
                timeSeriesResponse.export(
                    outStream, 0, name_="timeSeriesResponse",
                    namespacedef_=NSDEF)
                return (outStream.getvalue()).replace('\n', '')

            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @soap(String, String, String, String, _returns=Any)
        def GetValuesObject(self, location, variable, startDate, endDate):
            try:
                timeSeriesResponse = self.wof_inst.create_get_values_response(
                    location, variable, startDate, endDate)
                outStream = StringIO.StringIO()
                timeSeriesResponse.export(
                    outStream, 0, name_="timeSeriesResponse",
                    namespacedef_=NSDEF)
                return outStream.getvalue()

            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

    return WOFService
