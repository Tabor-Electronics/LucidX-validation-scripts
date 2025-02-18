
"""
Test description :- This test gives out the value frequency and  power
and compare the given threshold to conclude the result for Accuracy with given frequency
1) In this script we are using spectrum analyzer as a measuring device
"""

###########################
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import  LucidCmd

#Establishing connection with LUCIDX
handle = 'TCPIP::{0}::{1}::SOCKET'.format(config.lucid_ip_address,config.port)  #Lucid TCPIP address
Lucid_functions.reset(handle)
if config.spectrum:
    device_address = 'TCPIP::{0}::{1}::SOCKET'.format(config.spectrum_ip_address_india,config.port)  # Spectrum analyzer TCPIP  address
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(200,spectrum_analyzer)

for frequency in config.frequencies:
    SignalGeneration.continous_wave_generation(frequency, config.power_default) # continous signal generation

    if config.spectrum:# spectrum commands for automation
        cf = frequency  # center frequency on measuring device
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer) # set center frequency on spectrum
        freq_out,power_max = spectrum_methods.set_marker(spectrum_analyzer) #  Read marker x (frequency) and y (power)
        error_value=abs(float(freq_out) - cf)  # Calculating difference between input and output frequency
        power_error = abs(float(power_max)-config.power_default)  # Calculating difference between input and output power
        frequency_th = 0.1 #  frequency threshold in term of percentage of input frequency
        power_th = 1  #  power threshold in dBm
        if (error_value <( frequency_th*cf)) and (power_error <power_th): # Condition to conclude the test result
            print("Test pass for Frequency = {0} MHz".format(cf))
        else:
            print("Test fail  for Frequency = {0} MHz".format(cf))

# disconnect
Lucid_functions.disconnect_lucid(handle)

###END OF SCRIPT###
