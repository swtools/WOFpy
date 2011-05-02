
import urllib2

from lxml import etree

IOOS_SITE_FILE_URL = 'http://lighthouse.tamucc.edu/ioosobsreg.xml'
LOCAL_SITE_FILE_PATH = 'cbi_site_file.xml'

namespaces = {
    'gml': "http://www.opengis.net/gml",
    'xlink': "http://www.w3.org/1999/xlink",
    'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'ioos': "http://www.csc.noaa.gov/ioos"
}

schema_location = "http://www.csc.noaa.gov/ioos/schema obsRegistry.xsd"

def nspath(path, ns):
    return '{%s}%s' % (ns, path)

def fetch_ioos_site_file(site_file_url, local_site_file_path):
    response = urllib2.urlopen(site_file_url, )
    
    cbi_site_file = open(local_site_file_path, 'w')
    
    cbi_site_file.write(response.read())
    
    cbi_site_file.close()


def parse_site_file(local_site_file_path):
    site_file = open(local_site_file_path)
    
    tree = etree.parse(site_file)
    
    feature_member_list = tree.findall('//'+nspath('featureMember',
                                                   namespaces['gml']))
    
    for feature in feature_member_list:
        point_obs = feature.find(nspath('InsituPointObs', namespaces['ioos']))
        
        observation_name = point_obs.find(nspath('observationName', namespaces['ioos']))
        status = point_obs.find(nspath('status', namespaces['ioos']))
        platform_name = point_obs.find(nspath('platformName', namespaces['ioos']))
       
        horiz_position = point_obs.find(nspath('horizontalPosition', namespaces['ioos']))
        pos = horiz_position.find(nspath('Point', namespaces['gml'])+'/'+nspath('pos', namespaces['gml']))
        latitude = pos.text.split()[0]
        longitude = pos.text.split()[1]
         
        vert_position = point_obs.find(nspath('verticalPosition', namespaces['ioos']))
        #TODO: get units of measure attribute, uom
        
        operator = point_obs.find(nspath('operator', namespaces['ioos']))
        start_date = point_obs.find(nspath('startDate', namespaces['ioos']))
        end_date = point_obs.find(nspath('endDate', namespaces['ioos']))
        operator_uri = point_obs.find(nspath('operatorURI', namespaces['ioos']))
        platform_uri = point_obs.find(nspath('platformURI', namespaces['ioos']))
        data_uri = point_obs.find(nspath('dataURI', namespaces['ioos']))
        comments = point_obs.find(nspath('comments', namespaces['ioos']))


if __name__ == '__main__':
    try:
        f = open(LOCAL_SITE_FILE_PATH)
        f.close()
    except:
        print "Fetching IOOS site file from remote location."
        fetch_ioos_site_file(IOOS_SITE_FILE_URL, LOCAL_SITE_FILE_PATH)
    
    print "Parsing IOOS site file."
    parse_site_file(LOCAL_SITE_FILE_PATH)
    