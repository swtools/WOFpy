__author__ = 'cyoun'

import StringIO
import logging

from spyne.decorator import rpc
from spyne.model.complex import Array
from spyne.model.primitive import Unicode, AnyXml
from spyne.model.fault import Fault
from spyne.service import ServiceBase
from spyne.util import memoize
import wof

logger = logging.getLogger(__name__)

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'

@memoize
def TWOFService(wof_inst,T, T_name):
    class WOFService(ServiceBase):

        @rpc(Array(Unicode), Unicode, _returns=AnyXml)
        def GetSites(ctx, site=None, authToken=None):
            try:
                if site is not None:
                    siteArg = ','.join(str(s) for s in site)
                else:
                    siteArg = None
                logging.debug(site)
                logging.debug(siteArg)
                siteResponse = wof_inst.create_get_site_response(siteArg)
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
        @rpc(Array(Unicode), Unicode, _returns=Unicode)
        def GetSitesXml(ctx, site=None, authToken=None):
            siteResult = WOFService.GetSites(ctx,site,authToken)
            return siteResult.replace('\n', '')

        @rpc(Unicode, Unicode, _returns=AnyXml)
        def GetSiteInfoObject(ctx, site, authToken=None):
            try:
                siteInfoResponse = \
                    wof_inst.create_get_site_info_response(site)
                outStream = StringIO.StringIO()
                siteInfoResponse.export(outStream, 0, name_="sitesResponse",
                                    namespacedef_=NSDEF)
                return outStream.getvalue()
            except Exception as inst:
                if type(inst) == Fault:
                    raise inst
                else:
                    raise Fault(faultstring=str(inst))

        @rpc(Unicode, Unicode, _returns=T)
        def GetSiteInfo(ctx, site, authToken=None):
            siteinfoResult = WOFService.GetSiteInfoObject(ctx,site,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return siteinfoResult
            return str(siteinfoResult.replace('\n', ''))

        @rpc(Unicode, Unicode, _returns=AnyXml)
        def GetVariableInfoObject(ctx, variable, authToken=None):
            try:
                variableInfoResponse = \
                    wof_inst.create_get_variable_info_response(variable)
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

        @rpc(Unicode, Unicode, _returns=T)
        def GetVariableInfo(ctx, variable, authToken=None):
            varinfoResult = WOFService.GetVariableInfoObject(ctx,variable,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return varinfoResult
            return varinfoResult.replace('\n', '')

        @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=AnyXml)
        def GetValuesObject(ctx, location, variable, startDate, endDate,authToken=None):
            try:
                timeSeriesResponse = wof_inst.create_get_values_response(
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

        @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=T)
        def GetValues(ctx, location, variable, startDate, endDate,authToken=None):
            valuesResult = WOFService.GetValuesObject(ctx,location,variable,startDate,endDate,authToken)
            if T_name == wof._SERVICE_PARAMS["r_type"]:
                return valuesResult
            return valuesResult.replace('\n', '')

    def _on_method_return_xml(ctx):
        # whatever etree element you return is the final xml
        # response, so to prevent the extraneous ("%sResult" %
        # method_name) result element, we just need to return an
        # element that has that element removed and replaced with
        # its child, which was the original response

        #TODO: how do we determine which method is being returned from?
        # Since I don't know, I am doing a dumb test for each one

        if 'xml' and not 'soap' in list(ctx.out_protocol.type):
            logger.info("protocol types: %s" % list(ctx.out_protocol.type))
            modify_return_xml_object(ctx)
            return ctx

        if wof._SERVICE_PARAMS["s_type"] in list(ctx.out_protocol.type):
            result_element_name_list = [
                'GetSitesResult',
                'GetSiteInfoObjectResult',
                'GetVariableInfoObjectResult',
                'GetValuesObjectResult']

            element = ctx.out_document
            for result_element_name in result_element_name_list:
                result_element = element.find(
                    './/{%s}%s' % (element.nsmap['tns'], result_element_name))

                if result_element is not None:
                    parent = result_element.getparent()
                    children = result_element.getchildren()
                    parent.replace(result_element, children[0])
                    return ctx
        return

    def modify_return_xml_object(ctx):
        method_name = ctx._MethodContext__descriptor.name
        logger.info("Modify WOF10 %s request" % method_name)
        result_element_name='%sResult' % method_name
        element = ctx.out_document
        result_element=element.find('.//{%s}%s' % (element.nsmap['ns0'], result_element_name))
        children = result_element.getchildren()
        ctx.out_document = children[0]
        return ctx

    WOFService.event_manager.add_listener('method_return_document', _on_method_return_xml)

    return WOFService