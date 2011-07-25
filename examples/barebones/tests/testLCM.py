import logging

from wof import WOF

from LCM_dao import LCMDao

import private_config
import wof.models as wof_base

logging.basicConfig(level=logging.DEBUG)

dao = LCMDao(private_config.LCM_connection_string,'LCM_config.cfg')
#LCM_wof = WOF(dao)
#LCM_wof.config_from_file('LCM_config.cfg')

variableResultArr = dao.get_all_variables()
print variableResultArr
#for variableResult in variableResultArr:
#    print variableResult.VariableCode # This worked yay    
#    #variableResult.VariableUnits.UnitsID = variableResult.VariableUnits_UnitsID
#    #variableResult.VariableUnits.UnitsName = variableResult.VariableUnits_UnitsName
#    #variableResult.VariableUnits.UnitsType = variableResult.VariableUnits_UnitsName
#    print variableResult.VariableUnits_UnitsAbbreviation
#    print variableResult.VariableUnits.UnitsAbbreviation

r = variableResultArr
for i in range(len(r)):
    print i
    print r[i].VariableName
    
    r[i].VariableUnits = wof_base.BaseUnits()    
    r[i].VariableUnits.UnitsAbbreviation = str(r[i].VariableUnits_UnitsAbbreviation)
    r[0].VariableUnits.UnitsAbbreviation = "monkey"
    print r[0].VariableUnits.UnitsAbbreviation
    print r[1].VariableUnits.UnitsAbbreviation
    print r[2].VariableUnits.UnitsAbbreviation
    print r[3].VariableUnits.UnitsAbbreviation
    print r[4].VariableUnits.UnitsAbbreviation
    print "Next i"

print "let's see what happens after the loop assignment"
for re in r:
    print re.VariableName    
    print re.VariableUnits.UnitsAbbreviation
    
    #print r[i].VariableUnits_UnitsAbbreviation
#    print r.VariableUnitsID[i]
    