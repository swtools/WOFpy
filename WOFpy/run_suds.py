import suds

lbr = suds.client.Client('http://127.0.0.1:8080/lbr/soap/wateroneflow.wsdl')


#print lbr.service.GetSitesXml('')

#print lbr.service.GetSites('')

#print lbr.service.GetSiteInfoObject('LBR:USU-LBR-Confluence')

#print lbr.service.GetSiteInfo('LBR:USU-LBR-Confluence')

print lbr.service.GetVariableInfoObject('LBR:USU40')

#print lbr.service.GetVariableInfo('')

#print lbr.service.GetValuesObject('USU-LBR-Paradise','USU36')