import datetime
from optparse import OptionParser
import os
import tempfile
import time
import urllib2

from lxml import etree
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

import cbi_cache_models as model

IOOS_SITE_FILE_URL = 'http://lighthouse.tamucc.edu/ioosobsreg.xml'
CBI_SOS_CAPABILITIES_URL = 'http://lighthouse.tamucc.edu/sos'
GCOOS_ONTOLOGY_FILE_URL = \
    'http://mmisw.org/ont?form=rdf&uri=http://mmisw.org/ont/gcoos/parameter'

CBI_CACHE_DIR = tempfile.gettempdir()
CBI_CACHE_DATABASE_URI = 'sqlite:////' + os.path.join(
    CBI_CACHE_DIR, 'cbi_dao_cache.db')
LOCAL_SITE_FILE_PATH = os.path.join(
    CBI_CACHE_DIR, 'cbi_site_file.xml')
LOCAL_PARAMETER_FILE_PATH = os.path.join(
    CBI_CACHE_DIR, 'cbi_parameter_file.xml')
LOCAL_CAPABILITIES_FILE_PATH = os.path.join(
    CBI_CACHE_DIR, 'cbi_sos_capabilities_file.xml')

print CBI_CACHE_DATABASE_URI

namespaces = {
    'gml': "http://www.opengis.net/gml",
    'xlink': "http://www.w3.org/1999/xlink",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'ioos': "http://www.csc.noaa.gov/ioos",
    'omvmmi': "http://mmisw.org/ont/mmi/20081020/ontologyMetadata/",
    'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
    'owl': "http://www.w3.org/2002/07/owl#",
    'omv': "http://omv.ontoware.org/2005/05/ontology#",
    'dc': "http://purl.org/dc/elements/1.1/",
    'oost': "http://www.oostethys.org/schemas/0.1.0/oostethys",
    'ows': "http://www.opengis.net/ows/1.1",
    'swe': "http://www.opengis.net/swe/1.0",
    'sos': "http://www.opengis.net/sos/1.0",
    'par_base': "http://mmisw.org/ont/gcoos/parameter/"
}

# TODO: make this variable to units map instead of using the GCOOS
# whacky units Should probably reference the units as they are named
# in the SOS:GetObservation method degC, etc.  Then need to lookup
# variable name in here to get appropriate units when building
# variable/units cache
ioos_variable_to_units_map = {

}


class Site(object):
    def __init__(self, code, name, latitude, longitude):
        self.code = code
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __key(self):
        return (self.code, self.name, self.latitude, self.longitude)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


class Unit(object):
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

    def __key(self):
        return (self.name, self.abbreviation)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


class Parameter(object):
    def __init__(self, code, name, description, unit):
        self.code = code
        self.name = name
        self.description = description
        self.unit = unit

    def __key(self):
        return (self.code, self.name)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


class Series(object):
    def __init__(self, site_code, var_code, start_time, end_time,
                 time_interval, time_interval_unit, is_current):
        self.site_code = site_code
        self.var_code = var_code
        self.start_time = start_time
        self.end_time = end_time
        self.time_interval = time_interval
        self.time_interval_unit = time_interval_unit
        self.is_current = is_current

    def __key(self):
        return (self.site_code, self.var_code, self.start_time, self.end_time,
                self.time_interval, self.time_interval_unit, self.is_current)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


def nspath(path, ns):
    return '{%s}%s' % (ns, path)


def fetch_ioos_site_file(site_file_url, local_site_file_path):
    response = urllib2.urlopen(site_file_url)
    cbi_site_file = open(local_site_file_path, 'w')
    cbi_site_file.write(response.read())
    cbi_site_file.close()


def parse_site_file(local_site_file_path):
    '''
    Reads an IOOS XML site file and returns a set of sites.
    '''
    site_set = set()
    site_file = open(local_site_file_path)
    tree = etree.parse(site_file)
    site_file.close()
    feature_member_list = tree.findall('.//' + nspath(
        'featureMember', namespaces['gml']))

    for feature in feature_member_list:
        point_obs = feature.find(nspath('InsituPointObs', namespaces['ioos']))

        # ex: gml:id="CBI-TAMUCC.009.bpr"  bpr is the param code
        gml_id = point_obs.attrib[nspath('id', namespaces['gml'])]
        param_code = gml_id.split('.')[2]

        observation_name = point_obs.findtext(
            nspath('observationName', namespaces['ioos']))

        #Parse Site info
        #ex 009: Port Aransas (87752371)
        platform_name = point_obs.findtext(nspath('platformName',
                                              namespaces['ioos']))

        horiz_position_node = point_obs.find(nspath('horizontalPosition',
                                               namespaces['ioos']))
        pos = horiz_position_node.findtext(
            nspath('Point', namespaces['gml'])
            + '/' + nspath('pos', namespaces['gml']))

        latitude = pos.split()[0]
        longitude = pos.split()[1]

        vert_position_node = point_obs.find(nspath('verticalPosition',
                                              namespaces['ioos']))
        vert_pos_units = vert_position_node.attrib['uom']

        vert_datum = point_obs.findtext(nspath('verticalDatum',
                                           namespaces['ioos']))

        operator = point_obs.findtext(nspath('operator', namespaces['ioos']))
        start_date = point_obs.findtext(nspath('startDate',
                                               namespaces['ioos']))
        end_date = point_obs.findtext(nspath('endDate', namespaces['ioos']))
        operator_uri = point_obs.findtext(nspath('operatorURI',
                                             namespaces['ioos']))
        platform_uri = point_obs.findtext(nspath('platformURI',
                                             namespaces['ioos']))
        data_uri = point_obs.findtext(nspath('dataURI', namespaces['ioos']))
        comments = point_obs.findtext(nspath('comments', namespaces['ioos']))

        site_code = platform_name.split(':')[0]
        site_name = platform_name.split(':')[1].strip()

        #Create a Site object and add it to the return set
        site = Site(site_code, site_name, latitude, longitude)
        site_set.add(site)

    return site_set


def fetch_cbi_capabilities_file(cbi_capabilities_file_url,
                                local_capabilities_file_path):

    response = urllib2.urlopen(cbi_capabilities_file_url)

    local_capabilities_file = open(local_capabilities_file_path, 'w')

    local_capabilities_file.write(response.read())

    local_capabilities_file.close()


def extract_parameters_from_capabilities_doc(local_capabilities_file_path):
    capabilities_file = open(local_capabilities_file_path)

    tree = etree.parse(capabilities_file)

    capabilities_file.close()

    #.//ows:Parameter[@name='observedProperty']/ows:AllowedValues/ows:Value

    param_name_elements = tree.findall(
        './/' + nspath("Parameter[@name='observedProperty']",
                       namespaces['ows'])
        + '/' + nspath("AllowedValues", namespaces['ows'])
        + '/' + nspath("Value", namespaces['ows'])
    )

    return [p.text for p in param_name_elements]


def extract_sites_from_capabilities_doc(local_capabilities_file_path):
    capabilities_file = open(local_capabilities_file_path)

    tree = etree.parse(capabilities_file)

    capabilities_file.close()

    #.//ows:Parameter[@name='observedProperty']/ows:AllowedValues/ows:Value

    site_code_elements = tree.findall(
        './/' + nspath("Parameter[@name='offering']", namespaces['ows'])
        + '/' + nspath("AllowedValues", namespaces['ows'])
        + '/' + nspath("Value", namespaces['ows'])
    )

    return [s.text for s in site_code_elements]


def parse_capabilities_for_series(local_capabilities_file_path):
    capabilities_file = open(local_capabilities_file_path)

    tree = etree.parse(capabilities_file)

    capabilities_file.close()

    obs_offerings = tree.findall('.//' + nspath(
        'ObservationOffering', namespaces['sos']))

    series_set = set()

    for offering in obs_offerings:
        site_code = offering.findtext(nspath('name', namespaces['gml']))

        time_period = offering.find(
            nspath('eventTime', namespaces['sos'])
            + '/' + nspath('TimePeriod', namespaces['gml']))

        start_time = time_period.findtext(
            nspath('beginPosition', namespaces['gml']))

        end_time = time_period.findtext(
            nspath('endPosition', namespaces['gml']))

        time_interval_node = time_period.find(
            nspath('timeInterval', namespaces['gml']))

        time_interval_unit = time_interval_node.attrib['unit']
        time_interval = time_interval_node.text

        properties = offering.findall(
            nspath('observedProperty', namespaces['sos']))

        is_current = not end_time

        for prop in properties:
            #TODO: It would be best if the observedProperty elements
            # had the variable names/codes as their inner text, but
            # they don't currently
            prop_link = prop.attrib[(nspath('href', namespaces['xlink']))]
            split_prop_link = prop_link.split('/')
            var_code = split_prop_link[len(split_prop_link) - 1]

            series = Series(site_code, var_code, start_time, end_time,
                            time_interval, time_interval_unit, is_current)

            series_set.add(series)

    return series_set


def fetch_gcoos_parameter_file(parameter_file_url, local_parameter_file_path):
    response = urllib2.urlopen(parameter_file_url)

    cbi_parameter_file = open(local_parameter_file_path, 'w')

    cbi_parameter_file.write(response.read())

    cbi_parameter_file.close()


def parse_parameter_file(param_names, local_parameter_file_path):
    """
    Reads a GCOOS XML site file and returns a set of parameters and a set
    of units.
    The list of parameters returned is constrained to those in the input
    param_names list.
    """
    param_set = set()
    units_set = set()

    param_file = open(local_parameter_file_path)
    tree = etree.parse(param_file)
    param_file.close()

    all_params = tree.findall('.//' + nspath('Parameters',
                                            namespaces['par_base']))

    for p in all_params:
        name = p.findtext(nspath('name', namespaces['par_base']))

        if name in param_names:
            description = p.findtext(nspath('description',
                                            namespaces['par_base']))

            #units are in the description, prefaced by "Unit: " and
            # ending with a semicolon (eg Unit: celsius;)
            start_index = description.find('Unit: ')
            end_index = description.find(';', start_index)
            unit_abbr = description[(start_index + 6):end_index]
            # TODO: Where to get unit names?
            unit = Unit(unit_abbr, unit_abbr)

            #TODO: Some of these units are not really that good,
            # like "Pa | bar |dbar |atm" for pressure, "ug L-1 (not kg m-3)",
            # "precent"
            # Maybe we need a units dictionary or something since the GCOOS
            # registry is not very good
            units_set.add(unit)
            param = Parameter(name, name, description, unit)
            param_set.add(param)
    return (param_set, units_set)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--dropall", dest="dropall", default=False,
                  help="Drop all from site cache database before rebuilding.")

    (options, args) = parser.parse_args()

    #Attempt to open local site file to see if it exists
    try:
        f = open(LOCAL_SITE_FILE_PATH)
        f.close()
    #If it doesn't exist, then fetch a new one from the remote location
    except:
        print "Fetching IOOS site file from remote location."
        fetch_ioos_site_file(IOOS_SITE_FILE_URL, LOCAL_SITE_FILE_PATH)

    #Attempt to open local capbilities file to see if it exists
    try:
        f = open(LOCAL_CAPABILITIES_FILE_PATH)
        f.close()
    except:
        print "Fetching CBI SOS Capabilities file from remote location."
        fetch_cbi_capabilities_file(CBI_SOS_CAPABILITIES_URL,
                                    LOCAL_CAPABILITIES_FILE_PATH)

    #Attempt to open local parameter file to see if it exists
    try:
        f = open(LOCAL_PARAMETER_FILE_PATH)
        f.close()
    #If it doesn't exist, then fetch a new one from the remote location
    except:
        print "Fetching GCOOS parameter file from remote location."
        fetch_gcoos_parameter_file(GCOOS_ONTOLOGY_FILE_URL,
                                   LOCAL_PARAMETER_FILE_PATH)

    engine = create_engine(CBI_CACHE_DATABASE_URI,
                           convert_unicode=True)
    if options.dropall:
        print "Dropping existing tables from cache."
        model.clear_model(engine)

    model.create_model(engine)

    db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=engine))

    model.init_model(db_session)

    print "Parsing IOOS site file."
    site_set = parse_site_file(LOCAL_SITE_FILE_PATH)

    print ("Extracting valid site codes from SOS capabilities "
           "file and removing non-matching sites from site cache.")

    capabilities_site_list = extract_sites_from_capabilities_doc(
        LOCAL_CAPABILITIES_FILE_PATH)

    valid_site_list = [s for s in site_set
                       if s.code in capabilities_site_list]

    cache_sites = [model.Site(s.code, s.name, s.latitude, s.longitude)
                   for s in valid_site_list]

    print "Extracting valid parameters from SOS capabilities file."
    param_names = extract_parameters_from_capabilities_doc(
        LOCAL_CAPABILITIES_FILE_PATH)

    print "Parsing GCOOS parameter file."

    (param_set, units_set) = parse_parameter_file(
        param_names, LOCAL_PARAMETER_FILE_PATH)

    cache_units = [model.Units(u.name, u.abbreviation) for u in units_set]

    cache_variables = []

    for p in param_set:
        v = model.Variable(p.code, p.name, p.description)

        #Find the matching unit in the cache_units list
        for cu in cache_units:
            if p.unit.name == cu.UnitsName:
                v.VariableUnits = cu

        cache_variables.append(v)

    print "Parsing SOS Capabilities file for Series Catalog."

    series_set = parse_capabilities_for_series(LOCAL_CAPABILITIES_FILE_PATH)

    print "Adding %s sites and %s variables to local cache." % (
        len(cache_sites), len(cache_variables))

    try:
        db_session.add_all(cache_sites)
        db_session.add_all(cache_units)
        db_session.add_all(cache_variables)
        db_session.commit()

        #Now try to add series

        print "Adding SeriesCatalog to local cache."

        cache_series_cats = []

        for series in series_set:

            #TODO: Not all sites in the SOS Capabilities document are in the
            # IOOS Reg file.  Why?

            #Find the site in the cache
            site = model.Site.query.filter(
                model.Site.SiteCode == series.site_code).first()

            #Find the variable in the cache
            variable = model.Variable.query.filter(
                model.Variable.VariableCode == series.var_code).first()

            #Need to check because of situation mentioned above
            if site and variable:
                series_cat = model.Series()

                series_cat.Site = site
                series_cat.SiteID = site.SiteID
                series_cat.SiteCode = site.SiteCode
                series_cat.SiteName = site.SiteName

                series_cat.Variable = variable
                series_cat.VariableID = variable.VariableID
                series_cat.VariableCode = variable.VariableCode
                series_cat.VariableName = variable.VariableName
                series_cat.VariableUnitsID = variable.VariableUnits.UnitsID
                series_cat.VariableUnitsName = variable.VariableUnits.UnitsName
                series_cat.SampleMedium = variable.SampleMedium
                series_cat.GeneralCategory = variable.GeneralCategory

                time_units = model.Units.query.filter(
                    model.Units.UnitsName == series.time_interval_unit).first()

                if not time_units:
                    time_units = model.Units(series.time_interval_unit,
                                             series.time_interval_unit)
                    time_units.UnitsType = "Time"

                    db_session.add(time_units)
                    db_session.commit()

                variable.TimeUnits = time_units
                variable.TimeUnitsID = time_units.UnitsID

                #TODO: WaterML1 only supports integers for time interval
                # but the CBI service offerings have 0.5 hour intervals
                #variable.TimeSupport = series.time_interval
                #series_cat.TimeSupport = series.time_interval
                series_cat.TimeUnitsID = time_units.UnitsID
                series_cat.TimeUnitsName = time_units.UnitsName

                #TODO: DataType = "Raw data" ?

                #TODO: is this the best way to do the datetime conversion?
                st = time.strptime(
                    series.start_time, "%Y-%m-%dT%H:%M:%SZ")

                series_cat.BeginDateTimeUTC = \
                    datetime.datetime(st[0], st[1], st[2], st[3], st[4], st[5])

                if series.end_time:
                    et = time.strptime(
                        series.end_time, "%Y-%m-%dT%H:%M:%SZ")
                    series_cat.EndDateTimeUTC = datetime.datetime(
                        et[0], et[1], et[2], et[3], et[4], et[5])

                series_cat.IsCurrent = series.is_current

                cache_series_cats.append(series_cat)

        db_session.add_all(cache_series_cats)
        db_session.commit()

        print "Finished."

    except Exception as inst:
        print "ERROR: %s, %s" % (type(inst), inst)
