'''<DESCRIPTION> This script contains various scpi commands and query to check the system information,
 such as callibration date, hardware/ software versions, temperature,  battery in case of poratble
 </DESCRIPTION>'''
###START OF SCRIPT###
import numpy as np
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods

from SourceFiles import config
#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

test_success = True
'''<CMD> '*IDN?' </CMD>
<TOUSER>Device Identification response </TOUSER>'''
query = '*IDN?'
temp = Lucid_functions.send_scpi_query(query,handle)
print('Device Identification: ',temp)
if "Tabor Electronics" in temp:
    print("Pass")
else:
    test_success = False
    print("Fail")
print("Press enter for next frequency test")
input()

# Query only. This query will interrogate the Lucid unit for programming errors..
'''<CMD>":SYST:ERR?" </CMD>
<TOUSER>Following query will interrogate the Lucid unit for programming errors/TOUSER>'''
query = ":SYST:ERR?"
temp = Lucid_functions.send_scpi_query(query,handle)
print(temp)
if "0, no errors" in temp:
    print("Pass")
else:
    test_success = False
    print("Fail")
print("Press enter for next frequency test")
input()
    
'''<CMD>":SYST:TEMP?" </CMD>
<TOUSER>Following query will interrogate the Lucid unit for current temperature/TOUSER>'''
query = ":SYST:TEMP?"
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    print("Pass with temperature {}".format(temp))
else:
    test_success = False
    print("Fail")
print("Press enter for next frequency test")
input()

# Callibration date
'''<CMD>":SYST:TEMP?" </CMD>
<TOUSER>Following query will check the Lucid unit for caliration date/TOUSER>'''
query = ':SYST:INF:CAL?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    print("Callibration Date: {}".format(temp))
else:
    test_success = False
    print("Fail to access calibration date")
print("Press enter for next frequency test")
input()

# Query the instrument for its model number in a format similar to the following: LSxxxxx.
# The model number is programmed to a secure location in the flash memory and cannot be modified by the user.
'''<CMD>':SYST:INF:MOD?'</CMD>
<TOUSER>Following query will check the Lucid unit for model id/TOUSER>'''
query =':SYST:INF:MOD?'
mod_id = Lucid_functions.send_scpi_query(query,handle)
if mod_id:
    print("MODEL : {}".format(mod_id))
else:
    test_success = False
    print("Unable to get the model ")
print("Press enter for next frequency test")
input()

# Query the instrument for its serial number.
# The serial number is programmed to a secure location in the flash memory and cannot be modified by the user.
# The generator will return its serial number in a format similar to the following: 2xxxxx
'''<CMD>':SYST:INF:SER?' </CMD>
<TOUSER>Following query will check the Lucid unit for serial number/TOUSER>'''
query =':SYST:INF:SER?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    print("Serial number : {}".format(temp))
else:
    test_success = False
    print("Unable to get the serial number")
print("Press enter for next frequency test")
input()

# Query the instrument for its hardware revision level.
# The hardware revision includes the PCB revision.
# It is programmed to a secure location in the flash memory and cannot be modified by the user.
# The generator will return its hardware revisions in a format similar to the following: D
'''<CMD>':SYST:INF:HARD?'</CMD>
<TOUSER>Following query will check the Lucid unit for Hardware version/TOUSER>'''
query = ':SYST:INF:HARD?'
temp = Lucid_functions.send_scpi_query(query, handle)
if temp:
    print("Hardware information : {}".format(temp))
else:
    test_success = False
    print("Unable to get the Hardware information")
print("Press enter for next frequency test")
input()

# Query the instrument for its firmware revision level.
# It is programmed to a secure location in the flash.
# The generator will return its firmware revisions in a format stating date (DDMMYY)
# and revision number (VV) similar to the following: DDMMYYVV memory and cannot be modified by the user.
'''<CMD>':SYST:INF:FIRM?'</CMD>
<TOUSER>Following query will check the Lucid unit for Firmware version/TOUSER>'''
query = ':SYST:INF:FIRM?'
temp = Lucid_functions.send_scpi_query(query, handle)
if temp:
    print("Firmware  : {}".format(temp))
else:
    test_success = False
    print("Unable to get the Firmware information")
print("Press enter for next frequency test")
input()
    
    
#FPGA
'''<CMD>':SYST:INF:FIRM?'</CMD>
<TOUSER>Following query will check the Lucid unit for FPGA version/TOUSER>'''
query = ':SYST:INF:FPGA?'
temp = Lucid_functions.send_scpi_query(query, handle)
if temp:
    print("FPGA  : {}".format(temp))
else:
    test_success = False
    print("Unable to get the FPGA")
print("Press enter for next frequency test")
input()

# Query the instrument for its Tabor SCPI commands revision.
# It is programmed to a secure location in the flash memory and cannot be modified by the user.
'''<CMD>':SYSTem:INFormation:SCPIrevision?'</CMD>
<TOUSER>Following query will check the Lucid unit for SPCI version used/TOUSER>'''
query =':SYSTem:INFormation:SCPIrevision?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    print("SCPI version  : {}".format(temp))
else:
    test_success = False
    print("Unable to get the SCPI version")
print("Press enter for next frequency test")
input()

# Query the Lucid unit for the battery charging status. Only for Lucid Portable.
# The Lucid will return the Lucid battery charging status.
if "P" in mod_id:
    '''<CMD>':SYST:BAT?'</CMD>
    <TOUSER>Following query will check the Lucid portables battery/TOUSER>'''
    query = ':SYST:BAT?'
    temp = Lucid_functions.send_scpi_query(query, handle)
    if temp:
        print("Battery status  : {}".format(temp))
    else:
        test_success = False
        print("Unable to get the battery status")
print("Press enter for next frequency test")
input()

        
if test_success:
    print("Test completed for system details")
else:
    print("Run the script again")
###END OF SCRIPT###
