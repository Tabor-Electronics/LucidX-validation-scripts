print("Script tests the Internal source frequency for the ref out of the Lucid module")
###START OF SCRIPT###
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import  config

#Establishing connection with LUCIDX
handle = config.handle #Lucid TCPIP address
Lucid_functions.reset(config.handle)


 #NOTE- Please keep it false if spectrum analyzer is not connected to same LAN network and run the script on debug mode
print("Start Spectrum Analyzer")
print("Connect REF out from Lucid to the Spectrum Analyzer")

rosc_query = Lucid_functions.send_scpi_query(":ROSC:SOUR?", handle)
print('Rosc source', rosc_query)
for r_freq in [100e6,10e6]:
    Lucid_functions.send_scpi_command(":ROSC:SOUR INT",handle)
    Lucid_functions.send_scpi_command(':ROSC:OUTP:FREQ {0}'.format(r_freq), handle)
    rosc_freq = Lucid_functions.send_scpi_query(":ROSC:OUTP:FREQ?", handle)
    print(f"Check the measuring device keeping the center frequney at {rosc_freq} and modify the span accordingly")
    print("Press enter to run the next test")
    input()
    

error = Lucid_functions.get_lucid_error(handle)  # Error SCPI query
# disconnect instrument
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###