import datetime
from xml.sax.saxutils import escape

import ConfigParser
import WaterML
import core
import logging

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
    default_unitid = None
    default_samplemedium = None

    _config = None
    _templates = None

    def __init__(self, dao, config_file=None, templates=None):
        self.dao = dao
        if templates:
            self._templates = templates
        if config_file:
            self.config_from_file(config_file)

    def config_from_file(self, file_name):
        if self._templates:
            config = core.WOFConfig(file_name,templates=self._templates)
        else:
            config = core.WOFConfig(file_name)
        self._config = config


        self.network = config.network
        self.vocabulary = config.vocabulary
        self.menu_group_name = config.menu_group_name
        self.service_wsdl = config.service_wsdl
        self.timezone = config.timezone
        self.timezone_abbr = config.timezone_abbr


        self.default_site = config.default_site
        self.default_variable = config.default_variable
        self.default_start_date = config.default_start_date
        self.default_end_date = config.default_end_date
        self.default_unitid = config.default_unitid
        self.default_samplemedium = config.default_samplemedium

    def create_get_site_response(self, siteArg=None):

        if siteArg == None or siteArg == '':
            siteResultArr = self.dao.get_all_sites()
        else:
            siteCodesArr = siteArg.split(',')
            siteCodesArr = [s.replace(self.network + ':', '')
                            for s in siteCodesArr]
            siteResultArr = self.dao.get_sites_by_codes(siteCodesArr)

        #if len(siteResultArr) == 0:
        #    return None

        siteInfoResponse = WaterML.SiteInfoResponseType()

        queryInfo = WaterML.QueryInfoType()
        #TODO: check on how this should be done for multiple sites
        criteria = WaterML.criteria(locationParam=siteArg)
        queryInfo.set_criteria(criteria)
        queryInfoNote = WaterML.NoteType()
        queryInfo.add_note(queryInfoNote)
        queryInfo.set_extension('')
        siteInfoResponse.set_queryInfo(queryInfo)

        if siteResultArr:
            for siteResult in siteResultArr:
                s = self.create_site_element(siteResult)
                siteInfoResponse.add_site(s)
        else:
            #site = WaterML.site()
            #siteInfoResponse.add_site(site)
            raise Exception("Site,'%s', Not Found" % siteArg)

        return siteInfoResponse

    def create_get_site_info_response(self, siteArg, varArg=None):
        if siteArg is None:
            raise Exception("Site Not Found")
        siteCode = siteArg.replace(self.network + ':', '')
        siteResult = self.dao.get_site_by_code(siteCode)

        if (varArg == None or varArg == ''):
            seriesResultArr = self.dao.get_series_by_sitecode(siteCode)
        else:
            varCode = varArg.replace(self.vocabulary + ':', '')
            seriesResultArr = self.dao.get_series_by_sitecode_and_varcode(
                siteCode, varCode)

        if seriesResultArr is None or len(seriesResultArr) == 0:
            raise Exception("Site,'%s', Not Found" % siteArg)

        siteInfoResponse = WaterML.SiteInfoResponseType()

        queryInfo = WaterML.QueryInfoType()
        criteria = WaterML.criteria(locationParam=siteArg,
                                    variableParam=varArg)
        queryInfo.set_criteria(criteria)
        queryInfoNote = WaterML.NoteType()
        queryInfo.add_note(queryInfoNote)
        queryInfo.set_extension('')
        siteInfoResponse.set_queryInfo(queryInfo)

        if siteResult:
            s = self.create_site_element(siteResult, seriesResultArr)
            siteInfoResponse.add_site(s)
        else:
            #site = WaterML.site()
            #siteInfoResponse.add_site(site)
            raise Exception("Site,'%s', Not Found" % siteArg)

        return siteInfoResponse

    def create_get_variable_info_response(self, varArg=None):

        if (varArg == None or varArg == ''):
            variableResultArr = self.dao.get_all_variables()
        else:
            varCodesArr = varArg.split(',')
            varCodesArr = [v.replace(self.vocabulary + ':', '')
                           for v in varCodesArr]
            variableResultArr = self.dao.get_variables_by_codes(varCodesArr)

        if not variableResultArr:
            raise Exception("Variable,'%s', Not Found" % varArg)

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

        if not valueResultArr:
            timeSeries = WaterML.TimeSeriesType()
            timeSeriesResponse.set_timeSeries(timeSeries)
            return timeSeriesResponse

        #if not valueResultArr:
        #    raise Exception("Values Not Found for %s:%s for dates %s - %s" % (
        #        siteCode, varCode, startDateTime, endDateTime))

        if isinstance(valueResultArr,dict):
            for key in valueResultArr.keys():
                valueResultArr = valueResultArr[key]
                break

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

    def check_censorCode(self, censorCode):
        default = "nc"
        valueList = [
              "lt"
              ,"gt"
              ,"nc"
              ,"nd"
              ,"pnq"
            ]
        if (censorCode in valueList):
            return censorCode
        else:
            return default
    def check_QualityControlLevel(self, QualityControlLevel):
        default = "Unknown"
        valueList = [
             "Raw data"
          ,"Quality controlled data"
          ,"Derived products"
          ,"Interpreted products"
          ,"Knowledge products"
          ,"Unknown"
        ]
        if (QualityControlLevel in valueList):
            return QualityControlLevel
        else:
            return default

    #TODO: lots more stuff to fill out here
    def create_value_element(self, valueResult):
        datetime_string = core._get_iso8061_datetime_string(
            valueResult, "LocalDateTime", "DateTimeUTC")
        clean_censorCode =self.check_censorCode(valueResult.CensorCode)
        clean_qcl = self.check_QualityControlLevel(valueResult.QualityControlLevel)

        value = WaterML.ValueSingleVariable(
                        qualityControlLevel=clean_qcl,
                       # qualityControlLevel=valueResult.QualityControlLevel,
                        methodID=valueResult.MethodID,
                        sourceID=valueResult.SourceID,
                        #censorCode=valueResult.CensorCode,
                        censorCode=clean_censorCode,
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

        beginDateTime = core._get_iso8061_datetime_string(
            seriesResult, "BeginDateTime", "BeginDateTimeUTC")
        endDateTime = core._get_iso8061_datetime_string(
            seriesResult, "EndDateTime", "EndDateTimeUTC")

        #TimeInterval
        if beginDateTime is None:
            beginDateTime = datetime.datetime.now().isoformat()
        if endDateTime is None:
            endDateTime = datetime.datetime.now().isoformat()
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

    def check_dataTypeEnum(self, datatype):
        default = "Unknown"
        valueList = [
          "Continuous"
          ,"Instantaneous"
          ,"Cumulative"
          ,"Incremental"
          ,"Average"
          ,"Maximum"
          ,"Minimum"
          ,"Constant Over Interval"
          ,"Categorical"
          ,"Best Easy Systematic Estimator "
          ,"Unknown"
          ,"Variance"
          ,"Median"
          ,"Mode"
          ,"Best Easy Systematic Estimator"
          ,"Standard Deviation"
          ,"Skewness"
          ,"Equivalent Mean"
          ,"Sporadic"
          ,"Unknown"
        ]
        if datatype is None:
            logging.warn('Datatype is not specified')
            return default
        if (datatype in valueList):
            return datatype
        else:
            logging.warn('value outside of enum for datatype ' + datatype)
            return default

    def check_UnitsType(self, UnitsType):
        default = "Dimensionless"
        valueList = [
              "Angle"
              ,"Area"
              ,"Dimensionless"
              ,"Energy"
              ,"Energy Flux"
              ,"Flow"
              ,"Force"
              ,"Frequency"
              ,"Length"
              ,"Light"
              ,"Mass"
              ,"Permeability"
              ,"Power"
              ,"Pressure/Stress"
              ,"Resolution"
              ,"Scale"
              ,"Temperature"
              ,"Time"
              ,"Velocity"
              ,"Volume"
            ]
        if UnitsType is None:
            logging.warn('UnitsType is not specified ')
            return default
        if (UnitsType in valueList):
            return UnitsType
        else:
            logging.warn('value outside of enum for UnitsType ' + UnitsType)
            return default

    def check_SampleMedium(self, SampleMedium):
        default = "Unknown"
        valueList = [
          "Surface Water"
          ,"Ground Water"
          ,"Sediment"
          ,"Soil"
          ,"Air"
          ,"Tissue"
          ,"Precipitation"
          ,"Unknown"
          ,"Other"
          ,"Snow"
          ,"Not Relevant"
        ]
        if SampleMedium is None:
            logging.warn('SampleMedium is not specified')
            return default
        if (SampleMedium in valueList):
            return SampleMedium
        else:
            logging.warn('default returned: value outside of enum for SampleMedium ' + SampleMedium)
            return default

    def check_generalCategory(self, generalCategory):
        default = "Unknown"
        valueList = [
          "Water Quality"
          ,"Climate"
          ,"Hydrology"
          ,"Geology"
          ,"Biota"
          ,"Unknown"
          ,"Instrumentation"
        ]
        if generalCategory is None:
            logging.warn('GeneralCategory is not specified')
            return default
        if (generalCategory in valueList):
            return generalCategory
        else:
            logging.warn('default returned: value outside of enum for generalCategory ' + generalCategory)
            return default

    def check_valueType(self, valueType):
        default = "Unknown"
        valueList = [
          "Field Observation"
          ,"Sample"
          ,"Model Simulation Result"
          ,"Derived Value"
          ,"Unknown"
        ]
        if valueType is None:
            logging.warn('ValueType is not specified')
            return default
        if (valueType in valueList):
            return valueType
        else:
            logging.warn('default returned: value outside of enum for valueType ' + valueType)
            return default

    def create_variable_element(self, variableResult):
        clean_datatype = self.check_dataTypeEnum( variableResult.DataType)
        clean_medium = self.check_SampleMedium(variableResult.SampleMedium)
        clean_category = self.check_generalCategory(variableResult.GeneralCategory)
        clean_valuetype = self.check_valueType(variableResult.ValueType)
        variable = WaterML.VariableInfoType(
            variableName=variableResult.VariableName,
            #valueType=variableResult.ValueType,
            valueType=clean_valuetype,
                       # dataType=variableResult.DataType,
            dataType =clean_datatype,
            #generalCategory=variableResult.GeneralCategory,
            generalCategory=clean_category,
                        #sampleMedium=variableResult.SampleMedium,
            sampleMedium=clean_medium,
            NoDataValue=variableResult.NoDataValue,
            variableDescription=variableResult.VariableDescription)

        #For specimen data
        v_code = variableResult.VariableCode
        v_code_i = v_code.find('::')
        if v_code_i != -1:
            v_code = v_code[0:v_code_i]

        variableCode = WaterML.variableCode()
        variableCode.vocabulary = self.vocabulary
        #TODO: What is this, should it always be true?
        variableCode.default = "true"
        variableCode.variableID = variableResult.VariableID
        variableCode.valueOf_ = v_code

        variable.add_variableCode(variableCode)
        clean_variableUnits = self.check_UnitsType(variableResult.VariableUnits.UnitsType)

        if variableResult.VariableUnits:
            units = WaterML.units(
                unitsAbbreviation=variableResult.VariableUnits.UnitsAbbreviation,
                unitsCode=variableResult.VariableUnitsID,
                #unitsType=variableResult.VariableUnits.UnitsType,
                unitsType=clean_variableUnits,
                valueOf_=variableResult.VariableUnits.UnitsName)

            variable.set_units(units)

        timeSupport = WaterML.timeSupport()
        timeSupport.isRegular = variableResult.IsRegular

        if variableResult.TimeUnits:
            timeUnits = WaterML.UnitsType(
                UnitID=variableResult.TimeUnits.UnitsID,
                UnitName=variableResult.TimeUnits.UnitsName,
                UnitDescription=variableResult.TimeUnits.UnitsName,
                #UnitType=variableResult.TimeUnits.UnitsType,
                UnitType="Time",
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
