import datetime
from xml.sax.saxutils import escape

import ConfigParser
import soaplib.core
import soaplib.core.server.wsgi
import werkzeug

import wof.flask
import wof.soap
import WaterML


class WOF(object):

    network = 'NETWORK'
    vocabulary = 'VOCABULARY'
    menu_group_name = 'MENU_GROUP_NAME'
    service_wsdl = 'SERVICE_WSDL'
    timezone = None
    timezone_abbr = None

    dao = None

    default_site = None
    default_variable = None
    default_start_date = None
    default_end_date = None

    def __init__(self, dao, config_file=None):
        self.dao = dao
        if config_file:
            self.config_from_file(config_file)

    def config_from_file(self, file_name):
        config = ConfigParser.RawConfigParser()
        config.read(file_name)

        self.network = config.get('WOF', 'Network')
        self.vocabulary = config.get('WOF', 'Vocabulary')
        self.menu_group_name = config.get('WOF', 'Menu_Group_Name')
        self.service_wsdl = config.get('WOF', 'Service_WSDL')
        self.timezone = config.get('WOF', 'Timezone')
        self.timezone_abbr = config.get('WOF', 'TimezoneAbbreviation')

        if config.has_section('Default_Params'):
            self.default_site = config.get('Default_Params', 'Site')
            self.default_variable = config.get('Default_Params', 'Variable')
            self.default_start_date = config.get('Default_Params', 'StartDate')
            self.default_end_date = config.get('Default_Params', 'EndDate')

    def create_get_site_response(self, siteArg=None):

        if siteArg == None or siteArg == '':
            siteResultArr = self.dao.get_all_sites()
        else:
            siteCodesArr = siteArg.split(',')
            siteCodesArr = [s.replace(self.network + ':', '')
                            for s in siteCodesArr]
            siteResultArr = self.dao.get_sites_by_codes(siteCodesArr)

        if len(siteResultArr) == 0:
            return None

        siteInfoResponse = WaterML.SiteInfoResponseType()

        queryInfo = WaterML.QueryInfoType()
        #TODO: check on how this should be done for multiple sites
        criteria = WaterML.criteria(locationParam=siteArg)
        queryInfo.set_criteria(criteria)
        queryInfoNote = WaterML.NoteType()
        queryInfo.add_note(queryInfoNote)
        queryInfo.set_extension('')
        siteInfoResponse.set_queryInfo(queryInfo)

        for siteResult in siteResultArr:
            s = self.create_site_element(siteResult)
            siteInfoResponse.add_site(s)

        return siteInfoResponse

    def create_get_site_info_response(self, siteArg, varArg=None):
        siteCode = siteArg.replace(self.network + ':', '')
        siteResult = self.dao.get_site_by_code(siteCode)

        if (varArg == None or varArg == ''):
            seriesResultArr = self.dao.get_series_by_sitecode(siteCode)
        else:
            varCode = varArg.replace(self.vocabulary + ':', '')
            seriesResultArr = self.dao.get_series_by_sitecode_and_varcode(
                siteCode, varCode)

        if len(seriesResultArr) == 0:
            return None

        siteInfoResponse = WaterML.SiteInfoResponseType()

        queryInfo = WaterML.QueryInfoType()
        criteria = WaterML.criteria(locationParam=siteArg,
                                    variableParam=varArg)
        queryInfo.set_criteria(criteria)
        queryInfoNote = WaterML.NoteType()
        queryInfo.add_note(queryInfoNote)
        queryInfo.set_extension('')
        siteInfoResponse.set_queryInfo(queryInfo)

        s = self.create_site_element(siteResult, seriesResultArr)
        siteInfoResponse.add_site(s)

        return siteInfoResponse

    def create_get_variable_info_response(self, varArg=None):

        if (varArg == None or varArg == ''):
            variableResultArr = self.dao.get_all_variables()
        else:
            varCodesArr = varArg.split(',')
            varCodesArr = [v.replace(self.vocabulary + ':', '')
                           for v in varCodesArr]
            variableResultArr = self.dao.get_variables_by_codes(varCodesArr)

        variableInfoResponse = WaterML.VariablesResponseType()

        # TODO: Should queryInfo be in thois response?  Suds doesn't
        # like when it is.  If it should be in the response, then the
        # WSDL needs to be updated

        #queryInfo = WaterML.QueryInfoType()
        #criteria = WaterML.criteria(variableParam=varArg)
        #queryInfo.set_criteria(criteria)
        #queryInfoNote = WaterML.NoteType()
        #queryInfo.add_note(queryInfoNote)
        #queryInfo.set_extension('')
        #variableInfoResponse.set_queryInfo(queryInfo)

        variables = WaterML.variables()
        for variableResult in variableResultArr:
            v = self.create_variable_element(variableResult)
            variables.add_variable(v)
        variableInfoResponse.set_variables(variables)
        return variableInfoResponse

    def create_get_values_response(self, siteArg, varArg, startDateTime=None,
                                   endDateTime=None):

        #TODO: Tim thinks the DAO should handle network and vocab parsing,
        #      not WOF
        siteCode = siteArg.replace(self.network + ':', '')
        varCode = varArg.replace(self.vocabulary + ':', '')

        valueResultArr = self.dao.get_datavalues(siteCode, varCode,
                                                 startDateTime, endDateTime)
        if not valueResultArr:
            raise Exception("ERROR: No data found for %s:%s for dates %s - %s" % (
                siteCode, varCode, startDateTime, endDateTime))

        timeSeriesResponse = WaterML.TimeSeriesResponseType()

        queryInfo = WaterML.QueryInfoType()
        timeParam = WaterML.timeParam(
            beginDateTime=startDateTime, endDateTime=endDateTime)
        criteria = WaterML.criteria(
            locationParam=siteArg, variableParam=varArg, timeParam=timeParam)
        queryInfo.set_criteria(criteria)
        queryInfoNote = WaterML.NoteType()
        queryInfo.add_note(queryInfoNote)
        queryInfo.set_extension('')
        timeSeriesResponse.set_queryInfo(queryInfo)

        timeSeries = WaterML.TimeSeriesType()

        #sourceInfo (which is a siteInfo) element
        siteResult = self.dao.get_site_by_code(siteCode)

        #TODO: Exception?
        if not siteResult:
            pass

        sourceInfo = self.create_site_info_element(siteResult)
        timeSeries.sourceInfo = sourceInfo

        #variable element
        varResult = self.dao.get_variable_by_code(varCode)

        #TODO: Exception?
        if not varResult:
            pass

        variable = self.create_variable_element(varResult)
        timeSeries.variable = variable

        #TODO: fill in some more of the attributes in this element
        values = WaterML.TsValuesSingleVariableType()

        values.count = len(valueResultArr)

        if varResult.VariableUnits:
            values.unitsAbbreviation = varResult.VariableUnits.UnitsAbbreviation
            values.unitsCode = varResult.VariableUnits.UnitsID

        #Need to keep track of unique methodIDs and sourceIDs
        methodIdSet = set()
        sourceIdSet = set()
        qualifierIdSet = set()
        offsetTypeIdSet = set()

        for valueResult in valueResultArr:
            v = self.create_value_element(valueResult)
            values.add_value(v)

            if valueResult.MethodID:
                methodIdSet.add(valueResult.MethodID)

            if valueResult.SourceID:
                sourceIdSet.add(valueResult.SourceID)

            if valueResult.QualifierID:
                qualifierIdSet.add(valueResult.QualifierID)

            if valueResult.OffsetTypeID:
                offsetTypeIdSet.add(valueResult.OffsetTypeID)

        #Add method elements for each unique methodID
        if methodIdSet:
            methodIdArr = list(methodIdSet)
            methodResultArr = self.dao.get_methods_by_ids(methodIdArr)
            for methodResult in methodResultArr:
                method = self.create_method_element(methodResult)
                values.add_method(method)

        #Add source elements for each unique sourceID
        if sourceIdSet:
            sourceIdArr = list(sourceIdSet)
            sourceResultArr = self.dao.get_sources_by_ids(sourceIdArr)
            for sourceResult in sourceResultArr:
                source = self.create_source_element(sourceResult)
                values.add_source(source)

        #Add qualifier elements
        if qualifierIdSet:
            qualIdArr = list(qualifierIdSet)
            qualResultArr = self.dao.get_qualifiers_by_ids(qualIdArr)
            for qualifierResult in qualResultArr:
                q = WaterML.qualifier(
                    qualifierID=qualifierResult.QualifierID,
                    default=None,
                    network=self.network,
                    vocabulary=self.vocabulary,
                    qualifierCode=qualifierResult.QualifierCode)
                values.add_qualifier(q)

        #Add offset elements
        if offsetTypeIdSet:
            offsetTypeIdArr = list(offsetTypeIdSet)
            offsetTypeResultArr = self.dao.get_offsettypes_by_ids(
                offsetTypeIdArr)
            for offsetTypeResult in offsetTypeResultArr:
                offset = self.create_offset_element(offsetTypeResult)
                values.add_offset(offset)

        timeSeries.values = values
        timeSeriesResponse.set_timeSeries(timeSeries)
        return timeSeriesResponse

    def create_offset_element(self, offsetTypeResult):
        #TODO: where does offsetIsVertical come from
        #TODO: where does offsetHorizDirectionDegrees come from?
        offset = WaterML.OffsetType(
            offsetTypeID=offsetTypeResult.OffsetTypeID,
            offsetValue=None,
            offsetDescription=offsetTypeResult.OffsetDescription,
            offsetIsVertical='true',
            offsetHorizDirectionDegrees=None)

        if offsetTypeResult.OffsetUnits:
            units = WaterML.UnitsType(
                UnitID=offsetTypeResult.OffsetUnits.UnitsID,
                UnitAbbreviation=offsetTypeResult.OffsetUnits.UnitsAbbreviation,
                UnitName=offsetTypeResult.OffsetUnits.UnitsName,
                UnitType=offsetTypeResult.OffsetUnits.UnitsType)

            offset.units = units

        return offset

    def create_method_element(self, methodResult):
        method = WaterML.MethodType(
            methodID=methodResult.MethodID,
            MethodDescription=methodResult.MethodDescription,
            MethodLink=methodResult.MethodLink)

        # need at least one MethodLink element to meet WaterML 1.0
        # schema validation
        if method.MethodLink == None:
            method.MethodLink = ''
        return method

    def create_source_element(self, sourceResult):
        source = WaterML.SourceType(
            sourceID=sourceResult.SourceID,
            Organization=sourceResult.Organization,
            SourceDescription=sourceResult.SourceDescription,
            SourceLink=sourceResult.SourceLink)

        contactInfo = self.create_contact_info_element(sourceResult)

        source.ContactInformation = contactInfo

        if sourceResult.Metadata:
            metadata = WaterML.MetaDataType(
                TopicCategory=sourceResult.Metadata.TopicCategory,
                Title=sourceResult.Metadata.Title,
                Abstract=sourceResult.Metadata.Abstract,
                ProfileVersion=sourceResult.Metadata.ProfileVersion,
                MetadataLink=sourceResult.Metadata.MetadataLink)

            source.Metadata = metadata

        return source

    def create_contact_info_element(self, sourceResult):

        if (sourceResult.Address and sourceResult.City and sourceResult.State
            and sourceResult.ZipCode):

            addressString = ", ".join([sourceResult.Address,
                                       sourceResult.City,
                                       sourceResult.State,
                                       sourceResult.ZipCode])

            contactInfo = WaterML.ContactInformationType(
                Email=sourceResult.Email,
                ContactName=sourceResult.ContactName,
                Phone=sourceResult.Phone,
                Address=addressString)

            return contactInfo

        return None

    #TODO: lots more stuff to fill out here
    def create_value_element(self, valueResult):
        datetime_string = _get_iso8061_datetime_string(
            valueResult, "LocalDateTime", "DateTimeUTC")

        value = WaterML.ValueSingleVariable(
                        qualityControlLevel=valueResult.QualityControlLevel,
                        methodID=valueResult.MethodID,
                        sourceID=valueResult.SourceID,
                        censorCode=valueResult.CensorCode,
                        sampleID=valueResult.SampleID,
                        offsetTypeID=valueResult.OffsetTypeID,
                        accuracyStdDev=valueResult.ValueAccuracy,
                        offsetValue=valueResult.OffsetValue,
                        dateTime=datetime_string,
                        qualifiers=valueResult.QualifierID,
                        valueOf_=str(valueResult.DataValue))

        # TODO: value.offset stuff?  Why does value element have all
        # this offset stuff
        #offsetTypeResult = valueResult.OffsetType
        #if offsetTypeResult != None:
        #    value.offsetDescription = offsetTypeResult.OffsetDescription
        #    value.offsetUnitsAbbreviation = offsetTypeResult.OffsetUnits.UnitsAbbreviation
        #    value.offsetUnitsCode = offsetTypeResult.OffsetUnits.UnitsID
        return value

    def create_site_element(self, siteResult, seriesResultArr=None):
        site = WaterML.site()
        siteInfo = self.create_site_info_element(siteResult)

        site.set_siteInfo(siteInfo)

        #need at least one note element to meet WaterML 1.0 schema validation
        if (not siteResult.County
            and not siteResult.State
            and not siteResult.Comments):

            siteInfo.add_note(WaterML.NoteType())
        else:
            if siteResult.County:
                countyNote = WaterML.NoteType(title="County",
                                              valueOf_=siteResult.County)
                siteInfo.add_note(countyNote)

            if siteResult.State:
                stateNote = WaterML.NoteType(title="State",
                                             valueOf_=siteResult.State)
                siteInfo.add_note(stateNote)

            if siteResult.Comments:
                commentsNote = WaterML.NoteType(
                    title="Site Comments",
                    valueOf_=escape(siteResult.Comments))
                siteInfo.add_note(commentsNote)

        seriesCatalog = WaterML.seriesCatalogType()
        if (seriesResultArr != None):
            seriesCatalog.menuGroupName = self.menu_group_name
            #TODO: Make sure this is set properly in config fileame
            seriesCatalog.serviceWsdl = self.service_wsdl

            for seriesResult in seriesResultArr:
                series = self.create_series_element(seriesResult)

                seriesCatalog.add_series(series)

        site.add_seriesCatalog(seriesCatalog)

        # need at least one extension element to meet WaterML 1.0
        # schema validation
        site.set_extension('')
        return site

    def create_site_info_element(self, siteResult):
        siteInfo = WaterML.SiteInfoType()
        siteInfo.set_siteName(siteResult.SiteName)

        #TODO: agencyName
        siteCode = WaterML.siteCode(network=self.network,
                                    siteID=siteResult.SiteID,
                                    valueOf_=siteResult.SiteCode,
                                    agencyName=None,
                                    defaultId=None)

        siteInfo.add_siteCode(siteCode)

        # TODO: Maybe remove this?  None of the other WOF services
        # return this info probably because it is not that useful
        timeZoneInfo = WaterML.timeZoneInfo(siteUsesDaylightSavingsTime=False,
                                            daylightSavingsTimeZone=None)
        timeZoneInfo.defaultTimeZone = WaterML.defaultTimeZone(
            ZoneOffset=self.timezone,
            ZoneAbbreviation=self.timezone_abbr)

        siteInfo.set_timeZoneInfo(timeZoneInfo)
        geoLocation = WaterML.geoLocation()
        geogLocation = WaterML.LatLonPointType(
            srs="EPSG:{0}".format(siteResult.LatLongDatum.SRSID),
            latitude=siteResult.Latitude,
            longitude=siteResult.Longitude)
        geoLocation.set_geogLocation(geogLocation)

        if (siteResult.LocalX and siteResult.LocalY):
            localSiteXY = WaterML.localSiteXY()
            localSiteXY.projectionInformation = \
                                        siteResult.LocalProjection.SRSName
            localSiteXY.X = siteResult.LocalX
            localSiteXY.Y = siteResult.LocalY
            geoLocation.add_localSiteXY(localSiteXY)

        siteInfo.set_geoLocation(geoLocation)
        siteInfo.set_verticalDatum(siteResult.VerticalDatum)

        # need at least one extension element to meet WaterML 1.0
        # schema validation

        siteInfo.set_extension('')

        # need at least one altname element to meet WaterML 1.0 schema
        # validation
        siteInfo.set_altname('')
        return siteInfo

    def create_series_element(self, seriesResult):
        series = WaterML.series()

        #Variable
        variable = self.create_variable_element(seriesResult.Variable)
        series.set_variable(variable)

        series.valueCount = WaterML.valueCount(
            valueOf_=str(seriesResult.ValueCount))

        beginDateTime = _get_iso8061_datetime_string(
            seriesResult, "BeginDateTime", "BeginDateTimeUTC")
        endDateTime = _get_iso8061_datetime_string(
            seriesResult, "EndDateTime", "EndDateTimeUTC")

        #TimeInterval
        variableTimeInt = WaterML.TimeIntervalType(
            beginDateTime=beginDateTime,
            endDateTime=endDateTime)
        series.variableTimeInterval = variableTimeInt

        #Method
        if seriesResult.Method:
            method = self.create_method_element(seriesResult.Method)
            series.Method = method

        #Source
        if seriesResult.Source:
            source = self.create_source_element(seriesResult.Source)
            series.Source = source

        #QualityControlLevel
        qualityControlLevel = WaterML.QualityControlLevelType(
                    qualityControlLevelID=seriesResult.QualityControlLevelID,
                    valueOf_=seriesResult.QualityControlLevelCode)

        series.QualityControlLevel = qualityControlLevel

        return series

    def create_variable_element(self, variableResult):
        variable = WaterML.VariableInfoType(
            variableName=variableResult.VariableName,
            valueType=variableResult.ValueType,
            dataType=variableResult.DataType,
            generalCategory=variableResult.GeneralCategory,
            sampleMedium=variableResult.SampleMedium,
            NoDataValue=variableResult.NoDataValue,
            variableDescription=variableResult.VariableDescription)

        variableCode = WaterML.variableCode()
        variableCode.vocabulary = self.vocabulary
        #TODO: What is this, should it always be true?
        variableCode.default = "true"
        variableCode.variableID = variableResult.VariableID
        variableCode.valueOf_ = variableResult.VariableCode

        variable.add_variableCode(variableCode)

        if variableResult.VariableUnits:
            units = WaterML.units(
                unitsAbbreviation=variableResult.VariableUnits.UnitsAbbreviation,
                unitsCode=variableResult.VariableUnitsID,
                unitsType=variableResult.VariableUnits.UnitsType,
                valueOf_=variableResult.VariableUnits.UnitsName)

            variable.set_units(units)

        timeSupport = WaterML.timeSupport()
        timeSupport.isRegular = variableResult.IsRegular

        if variableResult.TimeUnits:
            timeUnits = WaterML.UnitsType(
                UnitID=variableResult.TimeUnits.UnitsID,
                UnitName=variableResult.TimeUnits.UnitsName,
                UnitDescription=variableResult.TimeUnits.UnitsName,
                UnitType=variableResult.TimeUnits.UnitsType,
                UnitAbbreviation=variableResult.TimeUnits.UnitsAbbreviation)

            timeSupport.set_unit(timeUnits)

        # TODO: time interval is not the same as time support.
        # Time interval refers to a spacing between values for regular data,
        # which isn't stored in ODM.
        if variableResult.TimeSupport:
            # integer in WaterML 1.0
            timeSupport.timeInterval = str(int(variableResult.TimeSupport))
        variable.set_timeSupport(timeSupport)
        return variable

    def create_wml2_values_object(self, siteArg, varArg, startDateTime=None,
                                   endDateTime=None):
        siteCode = siteArg.replace(self.network + ':', '')
        varCode = varArg.replace(self.vocabulary + ':', '')
        valueResultArr = self.dao.get_datavalues(siteCode, varCode,
                                                 startDateTime, endDateTime)
        return valueResultArr


def create_wof_app(dao, config_file):
    """
    Returns a fully instantiated WOF wsgi app (flask + soap)
    """
    wof_obj = WOF(dao, config_file)
    app = wof.flask.create_app(wof_obj)
    WOFService = wof.soap.create_wof_service_class(wof_obj)
    soap_app = soaplib.core.Application(
        services=[WOFService],
        tns='http://www.cuahsi.org/his/1.0/ws/',
        name='WaterOneFlow')
    soap_wsgi_app = soaplib.core.server.wsgi.Application(soap_app)
    app.wsgi_app = werkzeug.wsgi.DispatcherMiddleware(app.wsgi_app, {
        '/soap/wateroneflow': soap_wsgi_app
        })
    return app


def _get_iso8061_datetime_string(object, local_datetime_attr,
                                 utc_datetime_attr):
    """
    Returns a datetime string given an object and the names of the
    attributes for local time and utc date time
    """
    local_datetime = getattr(object, local_datetime_attr, None)
    if local_datetime:
        if type(local_datetime) == datetime.datetime:
            if not local_datetime.tzinfo:
                raise ValueError("local times must be timezone-aware")
            return local_datetime.isoformat()
        else:
            return local_datetime
    else:
        utc_datetime = getattr(object, utc_datetime_attr)
        if type(utc_datetime) == datetime.datetime:
            return utc_datetime.replace(tzinfo=None).isoformat() + 'Z'
        else:
            return utc_datetime
