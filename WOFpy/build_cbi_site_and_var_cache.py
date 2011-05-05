
import urllib2
import os

from optparse import OptionParser
from lxml import etree
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

import daos.cbi.cbi_cache_models as model

cbi_cache_connection_string = 'sqlite:///' + os.path.join(
    os.path.dirname(__file__), 'daos', 'cbi', 'cbi_cache.db')


IOOS_SITE_FILE_URL = 'http://lighthouse.tamucc.edu/ioosobsreg.xml'

GCOOS_ONTOLOGY_FILE_URL = \
    'http://mmisw.org/ont?form=rdf&uri=http://mmisw.org/ont/gcoos/parameter'

local_site_file_path = os.path.join(
    os.path.dirname(__file__), 'daos', 'cbi', 'cbi_site_file.xml')

local_parameter_file_path = os.path.join(
    os.path.dirname(__file__), 'daos', 'cbi', 'cbi_parameter_file.xml'
)

namespaces = {
    'gml': "http://www.opengis.net/gml",
    'xlink': "http://www.w3.org/1999/xlink",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'ioos': "http://www.csc.noaa.gov/ioos"
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

class Parameter(object):
    def __init__(self, code, name):
        self.code = code
        self.name = name
        
    
    def __key(self):
        return (self.code, self.name)
        
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
    Reads an IOOS XML site file and returns a set of sites and a set of
    paramaters.
    '''
    
    parameter_set = set()
    site_set = set()
    site_list = []
    
    site_file = open(local_site_file_path)
    
    tree = etree.parse(site_file)
    
    feature_member_list = tree.findall('//'+nspath('featureMember',
                                                   namespaces['gml']))
    
    for feature in feature_member_list:
        point_obs = feature.find(nspath('InsituPointObs', namespaces['ioos']))
        
        gml_id = point_obs.attrib[nspath('id', namespaces['gml'])]
        param_code = gml_id.split('.')[2]
        
        observation_name = point_obs.find(nspath('observationName',
                                                 namespaces['ioos']))
        
        #Create a Parameter object and add it to the return set
        parameter = Parameter(param_code, observation_name.text)
        parameter_set.add(parameter)
        
        #Parse Site info
        status = point_obs.find(nspath('status', namespaces['ioos']))
        platform_name = point_obs.find(nspath('platformName',
                                              namespaces['ioos']))
       
        horiz_position = point_obs.find(nspath('horizontalPosition',
                                               namespaces['ioos']))
        pos = horiz_position.find(nspath('Point', namespaces['gml'])+'/'+
                                  nspath('pos', namespaces['gml']))
        latitude = pos.text.split()[0]
        longitude = pos.text.split()[1]
         
        vert_position = point_obs.find(nspath('verticalPosition',
                                              namespaces['ioos']))
        vert_pos_units = vert_position.attrib['uom']
        
        vert_datum = point_obs.find(nspath('verticalDatum',
                                           namespaces['ioos']))
        
        operator = point_obs.find(nspath('operator', namespaces['ioos']))
        start_date = point_obs.find(nspath('startDate', namespaces['ioos']))
        end_date = point_obs.find(nspath('endDate', namespaces['ioos']))
        operator_uri = point_obs.find(nspath('operatorURI',
                                             namespaces['ioos']))
        platform_uri = point_obs.find(nspath('platformURI',
                                             namespaces['ioos']))
        data_uri = point_obs.find(nspath('dataURI', namespaces['ioos']))
        comments = point_obs.find(nspath('comments', namespaces['ioos']))
        
        
        site_code = platform_name.text.split(':')[0]
        site_name = platform_name.text.split(':')[1]
        
        #Create a Site object and add it to the return set
        site = Site(site_code, site_name, latitude, longitude)
        site_set.add(site)
   

    return (site_set, parameter_set)


def fetch_gcoos_parameter_file(parameter_file_url, local_parameter_file_path):
    response = urllib2.urlopen(parameter_file_url)
    
    cbi_parameter_file = open(local_parameter_file_path, 'w')
    
    cbi_parameter_file.write(response.read())
    
    cbi_parameter_file.close()


def parse_parameter_file(local_parameter_file_path):
    '''
    Reads an GCOOS XML site file and returns a set of sites and a set of
    paramaters.
    '''
    pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d","--dropall", dest="dropall", default=False,
                  help="Drop all from site cache database before rebuilding.")
    
    (options, args) = parser.parse_args()

    #Attempt to open local site file to see if it exists
    try:
        f = open(local_site_file_path)
        f.close()
    except: #If it doesn't exist, then fetch a new one from the remote location
        print "Fetching IOOS site file from remote location."
        fetch_ioos_site_file(IOOS_SITE_FILE_URL, local_site_file_path)
    
    #Attempt to open local parameter file to see if it exists
    try:
        f = open(local_parameter_file_path)
        f.close()
    except: #If it doesn't exist, then fetch a new one from the remote location
        print "Fetching GCOOS parameter file from remote location."
        fetch_gcoos_parameter_file(GCOOS_ONTOLOGY_FILE_URL,
                                   local_parameter_file_path)
    
    
    engine = create_engine(cbi_cache_connection_string,
                           convert_unicode=True)
    if options.dropall:
        model.clear_model(engine)
    
    model.create_model(engine)
    
    db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=engine))
    
    model.init_model(db_session)

    print "Parsing IOOS site file."
    (sites, params) = parse_site_file(local_site_file_path)
    
        
    cache_sites = [model.Site(s.code, s.name, s.latitude, s.longitude)
                   for s in sites]
        
    cache_variables = [model.Variable(p.code, p.name) for p in params]
    
    #TODO: Maybe should read the parameters from the SOS Capabilities
    # and then find them in the GCOOS parameter file
    
    print "Adding %s sites and %s variables to local cache." % (
        len(cache_sites), len(cache_variables))
    
    try:
        db_session.add_all(cache_sites)
        db_session.add_all(cache_variables)
        db_session.commit()
    
        print "Finished."
    except Exception as inst:
        print "ERROR: %s, %s" % (type(inst), inst)
    
    
    
    
    
    
    
    
    
    