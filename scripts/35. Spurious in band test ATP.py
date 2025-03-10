print("<DESCRIPTION> Test description- This test verifies, there is no spurious present in-band (between start and stop frequency ie span ) of the carrier above the defined error limit</DESCRIPTION>")
###########################
####START OF SCRIPT###
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
# Parameters
frequency_list =[1000,2000,3500,4000,550,2300,1500,3500,4000,3500,4000,550,2300,1500,3500,4000]
start_freq_tb = [500,1500,2400,2400,3400,3900,4900,5900,5900,6900,6900,7900,8900,9900,10900,10900]
stop_freq_tb = [1500,2400,3400,3400,3900,4900,5900,6900,6900,7900,7900,8900,9900,10900,11900,11900]
output = np.zeros(len(frequency_list)) # To store the output frequency from spectrum analyzer (optional step)
power_in_dBm = 5# power level required for the test in dBm
for freq in frequency_list:
    if freq<= 3000:
        SignalGeneration.continous_wave_generation(freq,power_in_dBm)
        print(f'Frequency = {freq}MHz, Power = {power_in_dBm}dBm')
    