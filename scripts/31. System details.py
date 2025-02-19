###START OF SCRIPT###
import numpy as np
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods

from SourceFiles import config
#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

test_success = True
query = '*IDN?'
temp = Lucid_functions.send_scpi_query(query,handle)
print(temp)
if "Tabor Electronics" in temp:
    print("Pass")
else:
    test_success = False
    print("Fail")

# Query only. This query will interrogate the Lucid unit for programming errors..

query = ":SYST:ERR?"
temp = Lucid_functions.send_scpi_query(query,handle)
print(temp)
if "0, no errors" in temp:
    print("Pass")
else:
    test_success = False
    print("Fail")

query = ":SYST:TEMP?"
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    print("Pass with temperature {}".format(temp))
else:
    test_success = False
    print("Fail")

# Callibration date
query = ':SYST:INF:CAL?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    print("Callibration Date: {}".format(temp))
else:
    test_success = False
    print("Fail to access calibration date")

# Query the instrument for its model number in a format similar to the following: LSxxxxx.
# The model number is programmed to a secure location in the flash memory and cannot be modified by the user.
query =':SYST:INF:MOD?'
mod_id = Lucid_functions.send_scpi_query(query,handle)
if mod_id:
    print("MODEL : {}".format(mod_id))
else:
    test_success = False
    print("Unable to get the model ")

# Query the instrument for its serial number.
# The serial number is programmed to a secure location in the flash memory and cannot be modified by the user.
# The generator will return its serial number in a format similar to the following: 2xxxxx
query =':SYST:INF:SER?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    print("Serial number : {}".format(temp))
else:
    test_success = False
    print("Unable to get the serial number")

    # Query the instrument for its hardware revision level.
    # The hardware revision includes the PCB revision.
    # It is programmed to a secure location in the flash memory and cannot be modified by the user.
    # The generator will return its hardware revisions in a format similar to the following: D
    query = ':SYST:INF:HARD?'
    temp = Lucid_functions.send_scpi_query(query, handle)
    if temp:
        print("Hardware information : {}".format(temp))
    else:
        test_success = False
        print("Unable to get the Hardware information")

# Query the instrument for its firmware revision level.
# It is programmed to a secure location in the flash.
# The generator will return its firmware revisions in a format stating date (DDMMYY)
# and revision number (VV) similar to the following: DDMMYYVV memory and cannot be modified by the user.
query = ':SYST:INF:FIRM?'
temp = Lucid_functions.send_scpi_query(query, handle)
if temp:
    print("Firmware  : {}".format(temp))
else:
    test_success = False
    print("Unable to get the Firmware information")

query = ':SYST:INF:FPGA?'
temp = Lucid_functions.send_scpi_query(query, handle)
if temp:
    print("FPGA  : {}".format(temp))
else:
    test_success = False
    print("Unable to get the FPGA")

# Query the instrument for its Tabor SCPI commands revision.
# It is programmed to a secure location in the flash memory and cannot be modified by the user.
query =':SYSTem:INFormation:SCPIrevision?'
temp = Lucid_functions.send_scpi_query(query,handle)
if temp:
    print("SCPI version  : {}".format(temp))
else:
    test_success = False
    print("Unable to get the SCPI version")

    # Query the Lucid unit for the battery charging status. Only for Lucid Portable.
    # The Lucid will return the Lucid battery charging status.
    if "P" in mod_id:
        query = ':SYST:BAT?'
        temp = Lucid_functions.send_scpi_query(query, handle)
        if temp:
            print("Battery status  : {}".format(temp))
        else:
            test_success = False
            print("Unable to get the battery status")

        # Query the Lucid unit for the battery charging status. Only for Lucid Portable.
        # The Lucid will return the Lucid battery charging status.
        if "P" in mod_id:
            query = ':SYST:BAT?'
            temp = Lucid_functions.send_scpi_query(query, handle)
            if temp:
                print("Battery status  : {}".format(temp))
            else:
                test_success = False
                print("Unable to get the battery status")
if test_success:
    print("Test completed for system details")
else:
    print("Run the script again")

