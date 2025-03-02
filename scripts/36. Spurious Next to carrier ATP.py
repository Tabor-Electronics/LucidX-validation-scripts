'''
Test - 2.8 Spurious next to carrier 
Test description- This test verifies, there is no spurious present next the the carrier above the defined error limit
Equipment required - 
Lucid device - LS1291D
Spectrum analyzer- Agilent Technologies, E4440A (PSA Series spectrum analyzer)
what is happening in thi sscript ?
 - After initializing the device, all the parameter are define in 2nd section,
 - span and center frequency is selected according to the signal frequency (using if/else condition)
 - using 3 marker, the script is checking the peak, peak right and peak left, 
 - if all these marker values are same, then we conclude that there is not spurious above -60dBc neXt to the carrier.
 -and if the marker value is not then we check if the power level is above threshold, then we conclude the final results
-  A test report will be generated at the end of the script and is saved as a text file in the same directory '''''
###START OF SCRIPT###
import time
import numpy as np
from functions_v1 import Lucid_functions,SignalGeneration
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
#Establishing connection with LUCIDX
handle = config.handle #Lucid TCPIP address
#Establishing connection with LUCIDX
Lucid_functions.reset(config.handle)
#Establishing connection with spectrum analyzer as a measuring device
 #NOTE- Please keep it false if spectrum analyzer is not connected to same LAN network and run the script on debug mode
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

####################################################################
# Input Parameters
frequency_list =list(np.arange(20,110,10))#+list(np.arange(150,1000,50)))+list(np.arange(1000,3000,500))#list(np.arange(1000,12000,1000))#+list(np.arange(150,1050,50))+list(np.arange(1250,12250,250)) # list of frequencies to be tested
power_in_dBm = 5.0 # power level required for the test in dBm

for i in range(len(frequency_list)): # iterating over each frequency (main loop)
    center_frequency = frequency_list[i]
    SignalGeneration.continous_wave_generation(center_frequency,power_in_dBm)
    print(f'Frequency = {center_frequency}MHz, Power = {power_in_dBm}dBm')