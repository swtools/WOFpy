import urllib


class CbiSosClient(object):
    
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url
        
    
    def get_capabilities(self):
        
        params = urllib.urlencode({'request':'GetCapabilities',
                                   'service':'SOS'})
        
        response = urllib.urlopen(self.endpoint_url+'?%s' % params)
        
        #TODO: might be able to do series catalog from this, look at
        # ObservationOffering elements of response xml
    
    
    def describe_sensor(self, sensor_id, ):
        
        #?request=DescribeSensor&service=SOS&version=1.0.0&outputformat=text/xml;subtype=%22sensorML/1.0.0%22&procedure=urn:ioos:sensor:wmo:41012::adcp0
        #or
        #?request=DescribeSensor&service=SOS&version=1.0.0&outputformat=text/xml;subtype=%22sensorML/1.0.0%22&procedure=urn:ioos:station:wmo:41012
        
        params = urllib.urlencode({'request':'DescribeSensor',
                                   'service':'SOS',
                                   'version':'1.0.0',
                                   'outputformat':'text/xml;subtype="sensorML/1.0.0"',
                                   'procedure':'urn:ioos:sensor:wmo:41012::adcp0'})
        
        pass
    
    
    def get_observations(self):
        pass
    
    
if __name__ == '__main__':
    c = CbiSosClient('http://lighthouse.tamucc.edu/sos')
    c.get_capabilities()