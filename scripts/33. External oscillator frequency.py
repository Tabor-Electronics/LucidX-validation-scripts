"""
Test description :- This test gives out the value frequency and  power
and compare the given threshold to conclude the result for Accuracy with given frequency
1) In this script we are using spectrum analyzer as a measuring device
"""

###START OF SCRIPT###
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
#Establishing connection with LUCIDX
handle = config.handle #Lucid TCPIP address
#Establishing connection with LUCIDX
Lucid_functions.reset(config.handle)
#Establishing connection with spectrum analyzer as a measuring device
 #NOTE- Please keep it false if spectrum analyzer is not connected to same LAN network and run the script on debug mode
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
    if config.spectrum:
        spectrum_methods.get_marker_frequency(spectrum_analyzer)

    # print("Connect REF out and RF out to the oscilloscope and compare the output frequencies")
    error = Lucid_functions.get_lucid_error(handle)  # Error SCPI query