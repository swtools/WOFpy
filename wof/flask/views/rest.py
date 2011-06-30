import StringIO
import datetime

from flask import (Flask, request, Markup, Response, render_template,
                   make_response, Module, current_app)

NSDEF = 'xmlns:gml="http://www.opengis.net/gml" \
    xmlns:xlink="http://www.w3.org/1999/xlink" \
    xmlns:xsd="http://www.w3.org/2001/XMLSchema" \
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
    xmlns:wtr="http://www.cuahsi.org/waterML/" \
    xmlns="http://www.cuahsi.org/waterML/1.0/"'

try:
    from flask import Blueprint
    rest = Blueprint(__name__, __name__)
except ImportError:
    rest = Module(__name__)


@rest.route('/')
def index():

    return render_template('index.html',
                           p=current_app.wof_inst.network,
                           s=current_app.wof_inst.default_site,
                           v=current_app.wof_inst.default_variable,
                           sd=current_app.wof_inst.default_start_date,
                           ed=current_app.wof_inst.default_end_date)


@rest.route('/GetSites', methods=['GET'])
def get_sites():

    siteArg = request.args.get('site', None)

    siteResponse = current_app.wof_inst.create_get_site_response(siteArg)

    if not siteResponse:
        return "Error: No site found for code [%s]" % (siteArg)

    outStream = StringIO.StringIO()
    siteResponse.export(outStream, 0, name_="sitesResponse",
                        namespacedef_=NSDEF)

    response = Response(response=outStream.getvalue(), status=200,
                        headers=None, mimetype='text/xml')

    return response


@rest.route('/GetSiteInfo', methods=['Get'])
def get_site_info():
    siteArg = request.args.get('site', None)
    varArg = request.args.get('variable', None)

    if siteArg == None:
        return "Must enter a single site code (site)"

    siteInfoResponse = current_app.wof_inst.create_get_site_info_response(
        siteArg, varArg)

    if not siteInfoResponse:
        return "Error: No site info found for site code [%s] \
            and var code [%s]" % (siteArg, varArg)

    outStream = StringIO.StringIO()
    siteInfoResponse.export(outStream, 0, name_="sitesResponse",
                            namespacedef_=NSDEF)

    response = Response(response=outStream.getvalue(), status=200,
                        headers=None, mimetype='text/xml')

    return response


@rest.route('/GetVariableInfo', methods=['GET'])
def get_variable_info():
    varArg = request.args.get('variable', None)

    variableInfoResponse = current_app.wof_inst.\
                           create_get_variable_info_response(varArg)

    outStream = StringIO.StringIO()
    variableInfoResponse.export(outStream, 0, name_="variablesResponse",
                                namespacedef_=NSDEF)

    response = Response(response=outStream.getvalue(), status=200,
                        headers=None, mimetype='text/xml')

    return response


@rest.route('/GetValues', methods=['GET'])
def get_values():

    #can also use "format=wml2" to get the waterml2 response
    formatArg = request.args.get('format', None)
    if formatArg and formatArg.lower() == 'wml2':
        return get_values_wml2()

    siteArg = request.args.get('location', None)
    varArg = request.args.get('variable', None)
    startDateTime = request.args.get('startDate', None)
    endDateTime = request.args.get('endDate', None)

    if (siteArg == None or varArg == None):
        return "Must enter a site code (location) and a variable code \
            (variable)"

    timeSeriesResponse = current_app.wof_inst.create_get_values_response(
        siteArg, varArg, startDateTime, endDateTime)

    outStream = StringIO.StringIO()
    timeSeriesResponse.export(outStream, 0, name_="timeSeriesResponse",
                              namespacedef_=NSDEF)

    response = Response(response=outStream.getvalue(), status=200,
                        headers=None, mimetype='text/xml')

    return response


@rest.route('/GetValuesWML2', methods=['GET'])
def get_values_wml2():
    """
    Experimental/Demo WaterML2-formatted Values response.
    """

    #TODO: Make this better once WaterML2 Schema is better understood
    # and/or best practices for using it are agreed to.

    siteArg = request.args.get('location', None)
    varArg = request.args.get('variable', None)
    startDateTime = request.args.get('startDate', None)
    endDateTime = request.args.get('endDate', None)

    if (siteArg == None or varArg == None):
        return "Must enter a site code (location) and a variable code \
            (variable)"

    siteCode = siteArg.replace(current_app.wof_inst.network + ':', '')
    varCode = varArg.replace(current_app.wof_inst.network + ':', '')

    data_values = current_app.wof_inst.dao.get_datavalues(siteCode, varCode,
                                                          startDateTime,
                                                          endDateTime)

    site_result = current_app.wof_inst.dao.get_site_by_code(siteCode)
    variable_result = current_app.wof_inst.dao.get_variable_by_code(varCode)

    current_date = str(datetime.datetime.now())

    response = make_response(render_template('wml2_values_template.xml',
                                            current_date=current_date,
                                            data_values=data_values,
                                            site_result=site_result,
                                            variable_result=variable_result))

    response.headers['Content-Type'] = 'text/xml'

    return response
