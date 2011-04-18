
import wof
import WaterML

from xml.sax.saxutils import escape


def create_get_site_response(siteArg):
    
    if siteArg == None or siteArg == '':
        siteResultArr = wof.dao.get_all_sites()
    else:
        siteCodesArr = siteArg.split(',')
        siteCodesArr = [s.replace(wof.network+':','') for s in siteCodesArr]
        siteResultArr = wof.dao.get_sites_by_codes(siteCodesArr)

    siteInfoResponse = WaterML.SiteInfoResponseType()

    queryInfo = WaterML.QueryInfoType()
    criteria = WaterML.criteria(locationParam=siteArg) #TODO: check on how this should be done for multiple sites
    queryInfo.set_criteria(criteria)
    queryInfoNote = WaterML.NoteType()
    queryInfo.add_note(queryInfoNote)
    queryInfo.set_extension('')
    siteInfoResponse.set_queryInfo(queryInfo)
    
    for siteResult in siteResultArr:
        s = create_site_element(siteResult)
        siteInfoResponse.add_site(s)
    
    return siteInfoResponse

def create_get_site_info_response(siteArg, varArg=None):
    
    siteCode = siteArg.replace(wof.network+':','')    
    siteResult = wof.dao.get_site_by_code(siteCode)
    
    if (varArg == None or varArg == ''):
        seriesResultArr = wof.dao.get_series_by_sitecode(siteCode)
    else:
        varCode = varArg.replace(wof.network+':','')
        seriesResultArr = \
            wof.dao.get_series_by_sitecode_and_varcode(siteCode, varCode)
    
    siteInfoResponse = WaterML.SiteInfoResponseType()
    
    queryInfo = WaterML.QueryInfoType()
    criteria = WaterML.criteria(locationParam=siteArg, variableParam=varArg)
    queryInfo.set_criteria(criteria)
    queryInfoNote = WaterML.NoteType()
    queryInfo.add_note(queryInfoNote)
    queryInfo.set_extension('')
    siteInfoResponse.set_queryInfo(queryInfo)
       
    
    s = create_site_element(siteResult, seriesResultArr)
    siteInfoResponse.add_site(s)

    return siteInfoResponse

def create_variable_info_response(varArg):
    
    if (varArg == None or varArg == ''):
        variableResultArr = wof.dao.get_all_variables()
    else:
        varCodesArr = varArg.split(',')
        varCodesArr = [v.replace(wof.network+':','') for v in varCodesArr]
        variableResultArr = wof.dao.get_variables_by_codes(varCodesArr)
    
    variableInfoResponse = WaterML.VariablesResponseType()
    
    queryInfo = WaterML.QueryInfoType()
    criteria = WaterML.criteria(variableParam=varArg)
    queryInfo.set_criteria(criteria)
    queryInfoNote = WaterML.NoteType()
    queryInfo.add_note(queryInfoNote)
    queryInfo.set_extension('')
    variableInfoResponse.set_queryInfo(queryInfo)
    
    variables = WaterML.variables()
        
    for variableResult in variableResultArr:
        v = create_variable_element(variableResult)
        variables.add_variable(v)
    
    variableInfoResponse.set_variables(variables)
    
    return variableInfoResponse


def create_get_values_response(siteArg, varArg, startDateTime=None, endDateTime=None):
    
    siteCode = siteArg.replace(wof.network+':','')
    varCode = varArg.replace(wof.network+':','')

    valueResultArr = wof.dao.get_datavalues(siteCode, varCode,
                                             startDateTime, endDateTime)
    
    timeSeriesResponse = WaterML.TimeSeriesResponseType()
    
    queryInfo = WaterML.QueryInfoType()
    timeParam = WaterML.timeParam(beginDateTime=startDateTime, endDateTime=endDateTime)
    criteria = WaterML.criteria(locationParam=siteArg, variableParam=varArg, timeParam=timeParam)
    queryInfo.set_criteria(criteria)
    queryInfoNote = WaterML.NoteType()
    queryInfo.add_note(queryInfoNote)
    queryInfo.set_extension('')
    timeSeriesResponse.set_queryInfo(queryInfo)
    
    timeSeries = WaterML.TimeSeriesType()
    
    #sourceInfo (which is a siteInfo) element
    siteResult = wof.dao.get_site_by_code(siteCode)
    sourceInfo = create_site_info_element(siteResult)
    timeSeries.sourceInfo = sourceInfo
    
    #variable element
    varResult = wof.dao.get_variable_by_code(varCode)
    variable = create_variable_element(varResult)
    timeSeries.variable = variable
    
    values = WaterML.TsValuesSingleVariableType() #TODO: fill in some more of the attributes in this element
    values.unitsAbbreviation = varResult.VariableUnits.UnitsAbbreviation
    values.unitsCode = varResult.VariableUnits.UnitsID
    values.count = len(valueResultArr)
    
    #Need to keep track of unique methodIDs and sourceIDs
    methodIdSet = set()
    sourceIdSet = set()
    qualifierIdSet = set()
    qualControlLevelIdSet = set()
    offsetTypeIdSet = set()
    
    for valueResult in valueResultArr:
        v = create_value_element(valueResult)
        values.add_value(v)
        
        if valueResult.MethodID:
            methodIdSet.add(valueResult.MethodID)
        
        if valueResult.SourceID:
            sourceIdSet.add(valueResult.SourceID)
        
        if valueResult.QualifierID:
            qualifierIdSet.add(valueResult.QualifierID)
        
        if valueResult.QualityControlLevelID:
            qualControlLevelIdSet.add(valueResult.QualityControlLevelID)
        
        if valueResult.OffsetTypeID:
            offsetTypeIdSet.add(valueResult.OffsetTypeID)

    #Add method elements for each unique methodID
    if methodIdSet:
        methodIdArr = list(methodIdSet)
        methodResultArr = wof.dao.get_methods_by_ids(methodIdArr)
        for methodResult in methodResultArr:
            method = create_method_element(methodResult)
            values.add_method(method)

    #Add source elements for each unique sourceID
    if sourceIdSet:
        sourceIdArr = list(sourceIdSet)
        sourceResultArr = wof.dao.get_sources_by_ids(sourceIdArr)
        for sourceResult in sourceResultArr:
            source = create_source_element(sourceResult)
            values.add_source(source)
    
    #Add qualifier elements
    if qualifierIdSet:
        qualIdArr = list(qualifierIdSet)
        qualResultArr = wof.dao.get_qualifiers_by_ids(qualIdArr)
        for qualifierResult in qualResultArr:
            q = WaterML.qualifier(
                qualifierID=qualifierResult.QualifierID,
                default=None,
                network=wof.network,
                vocabulary=wof.vocabulary,
                qualifierCode=qualifierResult.QualifierCode)
            values.add_qualifier(q)
        
    #Add qualityControlLevel elements
    if qualControlLevelIdSet:
        qualControlLvlIdArr = list(qualControlLevelIdSet)
        qualControlLevelResultArr = wof.dao.get_qualcontrollvls_by_ids(
            qualControlLvlIdArr)
        for qualControlLvlResult in qualControlLevelResultArr:
            qualControlLevel = create_qualityControlLevel_element(
                qualControlLvlResult)
            values.add_qualityControlLevel(qualControlLevel)
    
    #Add offset elements
    if offsetTypeIdSet:
        offsetTypeIdArr = list(offsetTypeIdSet)
        offsetTypeResultArr = wof.dao.get_offsettypes_by_ids(offsetTypeIdArr)
        for offsetTypeResult in offsetTypeResultArr:
            offset = create_offset_element(offsetTypeResult)
            values.add_offset(offset)
        
    
    timeSeries.values = values
    
    timeSeriesResponse.set_timeSeries(timeSeries)
    
    return timeSeriesResponse


def create_qualityControlLevel_element(qualControlLvlResult):
    qualityControlLevel = WaterML.QualityControlLevelType(
        qualityControlLevelID = qualControlLvlResult.QualityControlLevelID,
        valueOf_=qualControlLvlResult.Definition)

    return qualityControlLevel

def create_offset_element(offsetTypeResult):
    #TODO: where does offsetIsVertical come from
    #TODO: where does offsetHorizDirectionDegrees come from?
    offset = WaterML.OffsetType(offsetTypeID = offsetTypeResult.OffsetTypeID,
                                offsetValue=None,
                                offsetDescription=offsetTypeResult.OffsetDescription,
                                offsetIsVertical='true',
                                offsetHorizDirectionDegrees=None)
    if offsetTypeResult.OffsetUnits:
        units = WaterML.UnitsType(UnitID=offsetTypeResult.OffsetUnits.UnitsID,
                                  UnitAbbreviation=offsetTypeResult.OffsetUnits.UnitsAbbreviation,
                                  UnitName=offsetTypeResult.OffsetUnits.UnitsName,
                                  UnitType=offsetTypeResult.OffsetUnits.UnitsType)
        offset.units = units
    
    return offset

def create_method_element(methodResult):
    method = WaterML.MethodType(methodID=methodResult.MethodID,
                                 MethodDescription=methodResult.MethodDescription,
                                 MethodLink=methodResult.MethodLink)


    #need at least one MethodLink element to meet WaterML 1.0 schema validation
    #TODO: Instead of creating empty elements like this one here for schema validation, should this be done in WaterML.py?
    if method.MethodLink == None:
        method.MethodLink = ''
        
    return method

def create_source_element(sourceResult):
    source = WaterML.SourceType(sourceID=sourceResult.SourceID, Organization=sourceResult.Organization,
                                    SourceDescription=sourceResult.SourceDescription,
                                    SourceLink=sourceResult.SourceLink)
        
    addressString = ", ".join([sourceResult.Address,
                               sourceResult.City, sourceResult.State, sourceResult.ZipCode])
        
    contactInfo = WaterML.ContactInformationType(Email=sourceResult.Email,
                                    ContactName=sourceResult.ContactName,
                                    Phone=sourceResult.Phone,
                                    Address=addressString)
    
    source.ContactInformation=contactInfo

    if sourceResult.Metadata:
        metadata = WaterML.MetaDataType(
            TopicCategory=sourceResult.Metadata.TopicCategory,
            Title=sourceResult.Metadata.Title,
            Abstract=sourceResult.Metadata.Abstract,
            ProfileVersion=sourceResult.Metadata.ProfileVersion,
            MetadataLink=sourceResult.Metadata.MetadataLink)
        
        source.Metadata = metadata
    
    return source

#TODO: lots more stuff to fill out here
def create_value_element(valueResult):
    
    isoDateTime = str(valueResult.LocalDateTime).replace(' ','T')
    
    value = WaterML.ValueSingleVariable(
                    codedVocabularyTerm=None,
                    metadataDateTime=None,
                    qualityControlLevel=valueResult.QualityControlLevelID,
                    methodID=valueResult.MethodID,
                    codedVocabulary=None,
                    sourceID=valueResult.SourceID,
                    oid=None,
                    censorCode=valueResult.CensorCode,
                    sampleID=valueResult.SampleID,
                    offsetTypeID=valueResult.OffsetTypeID,
                    accuracyStdDev=valueResult.ValueAccuracy,
                    offsetValue=valueResult.OffsetValue,
                    dateTime=isoDateTime,
                    qualifiers=valueResult.QualifierID,
                    valueOf_=valueResult.DataValue)
    
    
    #TODO: value.offset stuff?  Why does value element have all this offset stuff
    #offsetTypeResult = valueResult.OffsetType
    #if offsetTypeResult != None:
    #    value.offsetDescription = offsetTypeResult.OffsetDescription
    #    value.offsetUnitsAbbreviation = offsetTypeResult.OffsetUnits.UnitsAbbreviation
    #    value.offsetUnitsCode = offsetTypeResult.OffsetUnits.UnitsID
    
    
    return value

def create_site_element(siteResult, seriesResultArr = None):
    site = WaterML.site()
    siteInfo = create_site_info_element(siteResult)
    
    site.set_siteInfo(siteInfo)
    
    #need at least one note element to meet WaterML 1.0 schema validation
    if (not siteResult.County and not siteResult.State and not siteResult.Comments):
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
            commentsNote = WaterML.NoteType(title="Site Comments",
                                        valueOf_=escape(siteResult.Comments))
            siteInfo.add_note(commentsNote)

        
    seriesCatalog = WaterML.seriesCatalogType()
        
    if (seriesResultArr != None):
        seriesCatalog.menuGroupName = wof.menu_group_name
        seriesCatalog.serviceWsdl = wof.service_wsdl
        
        for seriesResult in seriesResultArr:
            series = create_series_element(seriesResult)
            
            seriesCatalog.add_series(series)
    
    site.add_seriesCatalog(seriesCatalog)

    #need at least one extension element to meet WaterML 1.0 schema validation
    site.set_extension('')

    return site


def create_site_info_element(siteResult):
    siteInfo = WaterML.SiteInfoType()
    siteInfo.set_siteName(siteResult.SiteName)
    
    #TODO: agencyIName
    siteCode = WaterML.siteCode(network=wof.network,
                                siteID=siteResult.SiteID,
                                valueOf_=siteResult.SiteCode,
                                agencyName=None,
                                defaultId=None)
    
    siteInfo.add_siteCode(siteCode)
    
    
    geoLocation = WaterML.geoLocation()
    
    geogLocation = WaterML.LatLonPointType(srs="EPSG:{0}".format(siteResult.LatLongDatum.SRSID),
                                       latitude=siteResult.Latitude,
                                       longitude=siteResult.Longitude)

    geoLocation.set_geogLocation(geogLocation)
    
    if (siteResult.LocalX and siteResult.LocalY):
        localSiteXY = WaterML.localSiteXY()
        localSiteXY.projectionInformation = siteResult.LocalProjection.SRSName
        localSiteXY.X = siteResult.LocalX
        localSiteXY.Y = siteResult.LocalY
        geoLocation.add_localSiteXY(localSiteXY)
    
    siteInfo.set_geoLocation(geoLocation)

    siteInfo.set_verticalDatum(siteResult.VerticalDatum)

    #need at least one extension element to meet WaterML 1.0 schema validation
    siteInfo.set_extension('')

    #need at least one altname element to meet WaterML 1.0 schema validation
    siteInfo.set_altname('')
    
    return siteInfo

def create_series_element(seriesResult):
    series = WaterML.series()
            
    variable = create_variable_element(seriesResult.Variable)
    series.set_variable(variable)
    
    series.valueCount = WaterML.valueCount(valueOf_=seriesResult.ValueCount)
    
    #TODO: should we use BeginDateTime or BeginDateTimeUTC?
    # Most services use the non-UTC one
    if seriesResult.BeginDateTime and seriesResult.EndDateTime:
        isoBeginDateTime = str(seriesResult.BeginDateTime).replace(' ','T')
        isoEndDateTime = str(seriesResult.EndDateTime).replace(' ','T')
    else:
        isoBeginDateTime = str(seriesResult.BeginDateTimeUTC).replace(' ','T')
        isoEndDateTime = str(seriesResult.EndDateTimeUTC).replace(' ','T')
    
    variableTimeInt = WaterML.TimeIntervalType(beginDateTime=isoBeginDateTime,
                                              endDateTime=isoEndDateTime)
    
    series.variableTimeInterval = variableTimeInt

    method = create_method_element(seriesResult.Method)
   
    series.Method = method
    
    source = WaterML.SourceType(sourceID=seriesResult.SourceID,
                                Organization=seriesResult.Organization,
                                SourceDescription=seriesResult.SourceDescription,
                                Metadata=None, #TODO: Source Metadata
                                ContactInformation=None, #TODO: Source ContactInformation
                                SourceLink=None) #TODO: Source Link
    
    series.Source = source
    
    qualityControlLevel = WaterML.QualityControlLevelType(
                    qualityControlLevelID=seriesResult.QualityControlLevelID,
                    valueOf_=seriesResult.QualityControlLevelCode)
    
    series.QualityControlLevel = qualityControlLevel
    
    return series

def create_variable_element(variableResult):
    variable = WaterML.VariableInfoType(variableName=variableResult.VariableName,
                                        valueType=variableResult.ValueType,
                                        dataType=variableResult.DataType,
                                        generalCategory=variableResult.GeneralCategory,
                                        sampleMedium=variableResult.SampleMedium,
                                        NoDataValue=variableResult.NoDataValue)
    
    variableCode = WaterML.variableCode()
    variableCode.vocabulary = wof.vocabulary
    variableCode.default = "true" #TODO
    variableCode.variableID = variableResult.VariableID
    variableCode.valueOf_ = variableResult.VariableCode
    
    variable.add_variableCode(variableCode)
    
    units = WaterML.units(unitsAbbreviation=variableResult.VariableUnits.UnitsAbbreviation,
                          unitsCode=variableResult.VariableUnitsID,
                          unitsType=variableResult.VariableUnits.UnitsType,
                          valueOf_=variableResult.VariableUnits.UnitsName)
    
    variable.set_units(units)
    
    timeSupport = WaterML.timeSupport()
    timeSupport.isRegular = variableResult.IsRegular
    
    timeUnits = WaterML.UnitsType(UnitID=variableResult.TimeUnits.UnitsID,
                                  UnitName=variableResult.TimeUnits.UnitsName,
                                  UnitDescription=variableResult.TimeUnits.UnitsName,
                                  UnitType=variableResult.TimeUnits.UnitsType,
                                  UnitAbbreviation=variableResult.TimeUnits.UnitsAbbreviation)
    
    timeSupport.set_unit(timeUnits)
    
    #TODO: time interval is not the same as time support.  Time interval refers to a spacing between values for regular data, which isn't stored in ODM.
    if variableResult.TimeSupport:
        timeSupport.timeInterval = str(int(variableResult.TimeSupport)) #integer in WaterML 1.0
    variable.set_timeSupport(timeSupport)
    
    return variable
