print("<DESCRIPTION> This script contains various scpi commands and query to check the system information, such as callibration date, hardware/ software versions, temperature,  battery in case of poratble</DESCRIPTION>")
###START OF SCRIPT###
import numpy as np
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods
from SourceFiles.for_the_gui import DevicePrint
from SourceFiles import config

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

test_success = True
devicePrintCmd.msg_user.set('Device Identification Test')
devicePrintCmd.Print()
query = '*IDN?'
temp = Lucid_functions.send_scpi_query(query,handle)
# print('Device Identification: ',temp)
if "Tabor Electronics" in temp:
    devicePrintCmd.msg_user.set(' Test Pass for Device Indetification')
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set(' Test Fail  for Device Indetification')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

# Query only. This query will interrogate the Lucid unit for programming errors..
devicePrintCmd.msg_user.set('System Error test')
devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Following query will interrogate the Lucid unit for programming errors')
devicePrintCmd.Print()
query = ":SYST:ERR?"
temp = Lucid_functions.send_scpi_query(query,handle)
if "0, no errors" in temp:
    devicePrintCmd.msg_user.set(' Test Pass for System Error query')
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set(' Test Fail for System Error query')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

devicePrintCmd.msg_user.set('Temperature test')
devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Following query will interrogate the Lucid unit for current temperatures')
devicePrintCmd.Print()
query = ":SYST:TEMP?"
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    devicePrintCmd.msg_user.set('Pass with temperature {}'.format(temp))
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set(' Test Fail for Temperature query')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

# Callibration date
devicePrintCmd.msg_user.set('Calibration date query test')
devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Following query will check the Lucid unit for caliration date')
devicePrintCmd.Print()
query = ':SYST:INF:CAL?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    devicePrintCmd.msg_user.set('Callibration Date: {0}'.format(temp))
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set('Fail to access calibration date')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

# Query the instrument for its model number in a format similar to the following: LSxxxxx.
# The model number is programmed to a secure location in the flash memory and cannot be modified by the user.
devicePrintCmd.msg_user.set('Following query will check the Lucid unit for model id')
devicePrintCmd.Print()

query =':SYST:INF:MOD?'
mod_id = Lucid_functions.send_scpi_query(query,handle)
if mod_id:
    devicePrintCmd.msg_user.set('MODEL : {}'.format(mod_id))
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set('Unable to get the model ')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

# Query the instrument for its serial number.
# The serial number is programmed to a secure location in the flash memory and cannot be modified by the user.
# The generator will return its serial number in a format similar to the following: 2xxxxx
devicePrintCmd.msg_user.set('Following query will check the Lucid unit for serial number')
devicePrintCmd.Print()

query =':SYST:INF:SER?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    devicePrintCmd.msg_user.set('Serial number : {}'.format(temp))
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set('Unable to get the serial number')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

# Query the instrument for its hardware revision level.
# The hardware revision includes the PCB revision.
# It is programmed to a secure location in the flash memory and cannot be modified by the user.
# The generator will return its hardware revisions in a format similar to the following: D
devicePrintCmd.msg_user.set('Following query will check the Lucid unit for Hardware version')
devicePrintCmd.Print()

query = ':SYST:INF:HARD?'
temp = Lucid_functions.send_scpi_query(query, handle)
if temp:
    devicePrintCmd.msg_user.set('Hardware information : {}'.format(temp))
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set('Unable to get the Hardware information')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

# Query the instrument for its firmware revision level.
# It is programmed to a secure location in the flash.
# The generator will return its firmware revisions in a format stating date (DDMMYY)
# and revision number (VV) similar to the following: DDMMYYVV memory and cannot be modified by the user.
devicePrintCmd.msg_user.set('Following query will check the Lucid unit for Firmware version ')
devicePrintCmd.Print()

query = ':SYST:INF:FIRM?'
temp = Lucid_functions.send_scpi_query(query, handle)
if temp:
    devicePrintCmd.msg_user.set('Firmware  : {}'.format(temp))
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set('Unable to get the Firmware information')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()
    
    
#FPGA
devicePrintCmd.msg_user.set('Following query will check the Lucid unit for FPGA version')
devicePrintCmd.Print()

query = ':SYST:INF:FPGA?'
temp = Lucid_functions.send_scpi_query(query, handle)
if temp:
    devicePrintCmd.msg_user.set('FPGA  : {}'.format(temp))
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set('Unable to get the FPGA')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

# Query the instrument for its Tabor SCPI commands revision.
# It is programmed to a secure location in the flash memory and cannot be modified by the user.
devicePrintCmd.msg_user.set('Following query will check the Lucid unit for SPCI version used')
devicePrintCmd.Print()

query =':SYSTem:INFormation:SCPIrevision?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    devicePrintCmd.msg_user.set('SCPI version  : {}'.format(temp))
    devicePrintCmd.Print()
else:
    test_success = False
    devicePrintCmd.msg_user.set('Unable to get the SCPI version')
    devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()

# Query the Lucid unit for the battery charging status. Only for Lucid Portable.
# The Lucid will return the Lucid battery charging status.
if "P" in mod_id:
    devicePrintCmd.msg_user.set('Following query will check the Lucid portables battery')
    devicePrintCmd.Print()
    query = ':SYST:BAT?'
    temp = Lucid_functions.send_scpi_query(query, handle)
    if temp:
        devicePrintCmd.msg_user.set('Battery status  : {}'.format(temp))
        devicePrintCmd.Print()
    else:
        test_success = False
        devicePrintCmd.msg_user.set('Unable to get the battery status')
        devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for next test')
devicePrintCmd.Print()
input()
        
if test_success:
    devicePrintCmd.msg_user.set('Test completed for system details')
    devicePrintCmd.Print()
else:
    devicePrintCmd.msg_user.set('Run the script again')
    devicePrintCmd.Print()
###END OF SCRIPT###
