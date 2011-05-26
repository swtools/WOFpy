import suds

swis = suds.client.Client('http://127.0.0.1:8080/soap/wateroneflow.wsdl')


known_site_codes = [
    'ARA', 'ARROYD', 'ARROYS', 'BAFF', 'BAYT', 'BIRD', 'BLB', 'BOBH',
    'BOLI', 'BRAZOSD', 'BRAZOSS', 'BZ1U', 'BZ1UX', 'BZ2L', 'BZ2U',
    'BZ3L', 'BZ3U', 'BZ4L', 'BZ4U', 'BZ5L', 'BZ5U', 'BZ6U', 'CANEY',
    'CED1', 'CED2', 'CHKN', 'CONT', 'COP', 'COWT', 'DELT', 'DOLLAR',
    'EAST', 'EEMAT', 'ELTORO', 'EMATC', 'EMATH', 'EMATT', 'FISH',
    'FRES', 'FRPT', 'GIW1',  'GWSB1', 'GWSB2', 'HANN', 'ICFR', 'INGL',
    'ISABEL', 'JARD', 'JDM1', 'JDM2', 'JDM3', 'JDM4', 'JFK', 'JOB',
    'LAVC', 'LM-ARR', 'MANS', 'MATA', 'MCF1', 'MCF2', 'MES', 'MIDG',
    'MIDSAB', 'MOSQ', 'NUE', 'NUECWN', 'NUECWS', 'NUELOW', 'NUEPP',
    'NUERIV', 'NUEUP', 'OLDR', 'OSO', 'RED', 'RIOA', 'RIOF', 'SAB1',
    'SAB2', 'SANT', 'SB1S', 'SB1W', 'SB2S', 'SB2W', 'SB3S', 'SB3W',
    'SB5S', 'SB5W', 'SB6W', 'SBBP', 'SBR1', 'SBR2', 'SBR3', 'SBR4',
    'SBR5', 'SBWS', 'SLNDCUT', 'SWBR', 'TRIN', 'UPBAFF', 'USAB'   
]

#print swis.service.GetSitesXml('')

#print swis.service.GetSites('SWIS:BAYT')


#for site_code in known_site_codes:
#    print site_code
    #TODO: this will fail because swis2 doesn't have siteinfo for all the sites
#    print swis.service.GetSiteInfoObject('SWIS:'+site_code)

#print swis.service.GetSiteInfo('swis:USU-swis-Confluence')

print swis.service.GetVariableInfoObject('SWIS:USU40')

#print swis.service.GetVariableInfo('')

#print swis.service.GetValuesObject('USU-swis-Paradise','USU36')