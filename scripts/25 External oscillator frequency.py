print("Script tests the external source frequency fro the ref out of the Lucid module")
print("Steps:\n1) Connect an external source to the Ref in (input port) of the lucid module.\n2) Provide a signal of 10MHz and 100Mhz\n3) Connect the RF out and REF out (output ports) to the measuring device")
print("Note: It may be tested on Spectrum Analyzer or Oscilloscope")
###START OF SCRIPT###
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
#Establishing connection with LUCIDX
handle = config.handle #Lucid TCPIP address
Lucid_functions.reset(config.handle)

print("Start spectrum analyzer")

# commands for spectrum analyzer
if config.spectrum:
    spectrum_address = 'TCPIP::192.90.70.36::5025::SOCKET' # Spectrum analyzer TCPIP  address
    spectrum_analyzer = spectrum_methods.connect_spectrum_via_lan(spectrum_address)
    status_sa = spectrum_methods.reset_and_clear_sa(spectrum_analyzer) # reset and clear the measuring device spectrum analyzer
    if status_sa: # checking the reset status
        print("Factory reset done Spectrum Analyzer")
    else:
        print("Error while reseting spectrum aanlyzer")

rosc_query = Lucid_functions.send_scpi_query(":ROSC:SOUR?",handle)
print('Rosc source',rosc_query)
if "EXT" in rosc_query:
    rosc_freq = Lucid_functions.send_scpi_query(":ROSC:SOUR:FREQ?", handle)
    print("Reference oscillator frequency: ",rosc_freq)
    print(f"Check the measuring device keeping the center frequney at {rosc_freq} and modify the span")
    print("Press enter to end the test")
    input()
else:
    print("Extrenal source not detected")

error = Lucid_functions.get_lucid_error(handle)  # Error SCPI query
# disconnect instrument
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###