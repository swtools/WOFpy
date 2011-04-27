
import StringIO

import wof
import wof.code
import swis_dao

from flask import (Flask, request, Markup, Response, render_template,
                   make_response, Module)


NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'

rest = Module(__name__)

@rest.route('/wsdl/<network>.wsdl')
def get_wsdl(network):
#TODO: The WSDL should be served separately from the Flask application
    if network == 'lbr' or network == 'swis':
        #TODO: should have different serv_loc based on network
        serv_loc = 'http://crwr-little.austin.utexas.edu:8080/soap/WOFService'
        response = make_response(render_template('wsdl_temp.wsdl',
                                                 serv_loc=serv_loc,
                                                 network=network))
        
        response.headers['Content-Type'] = 'text/xml'
        
        return response
    else:
        return "Network '"+network+"' not registered."

@rest.route('/')
def index():
    
    if isinstance(wof.dao, swis_dao.SwisDao):
        return render_template('index.html', p=wof.network, s='BAYT',
                           v='seawater_salinity',sd='2007-03-23T12:00:00',
                           ed='2007-03-24T12:00:00')
    
    return render_template('index.html', p=wof.network, s='USU-LBR-Paradise',
                           v='USU36',sd='2007-08-17T12:00:00',
                           ed='2007-08-18T12:00:00')


@rest.route('/GetSites', methods=['GET'])
def get_sites():
    
    siteArg = request.args.get('site',None)
    
    siteResponse = wof.code.create_get_site_response(siteArg)
   
    if not siteResponse:
        return "Error: No site found for code [%s]" % (siteArg)
   
    outStream = StringIO.StringIO()
    siteResponse.export(outStream, 0, name_="sitesResponse",
                        namespacedef_= NSDEF)
    
    response = Response(response=outStream.getvalue(), status=200,
                        headers=None, mimetype='text/xml')

    return response


@rest.route('/GetSiteInfo', methods=['Get'])
def get_site_info():
    siteArg = request.args.get('site',None)
    varArg = request.args.get('variable',None)
    
    if siteArg == None:
        return "Must enter a single site code (site)"
    
    siteInfoResponse = wof.code.create_get_site_info_response(siteArg,varArg)
    
    if not siteInfoResponse:
        return "Error: No site info found for site code [%s] and var code [%s]" % (
            siteArg, varArg)
    
    outStream = StringIO.StringIO()
    siteInfoResponse.export(outStream, 0, name_="sitesResponse",
                            namespacedef_= NSDEF)
    
    response = Response(response=outStream.getvalue(), status=200,
                        headers=None, mimetype='text/xml')

    return response


@rest.route('/GetVariableInfo', methods=['GET'])
def get_variable_info():
    varArg = request.args.get('variable',None)
    
    variableInfoResponse = wof.code.create_get_variable_info_response(varArg)
    
    outStream = StringIO.StringIO()
    variableInfoResponse.export(outStream, 0, name_="variablesResponse",
                                namespacedef_= NSDEF)
    
    response = Response(response=outStream.getvalue(), status=200,
                        headers=None, mimetype='text/xml')

    return response
    

@rest.route('/GetValues', methods=['GET'])
def get_values():
    
    siteArg = request.args.get('location',None)
    varArg = request.args.get('variable',None)
    startDateTime = request.args.get('startDate',None) #TODO
    endDateTime = request.args.get('endDate',None) #TODO
    
    if (siteArg == None or varArg == None):
        return "Must enter a site code (location) and a variable code (variable)"

    timeSeriesResponse = wof.code.create_get_values_response(
        siteArg,varArg,startDateTime,endDateTime)

    outStream = StringIO.StringIO()
    timeSeriesResponse.export(outStream, 0, name_="timeSeriesResponse",
                              namespacedef_= NSDEF)

    response = Response(response=outStream.getvalue(), status=200,
                        headers=None, mimetype='text/xml')

    return response
