print("Test description :- This test gives out the value frequency and  power and compare the given threshold to conclude the result for accuracy of power  given frequency")
print("Steps:- \n1) In this script we are using spectrum analyzer as a measuring device.\n2) We will set a center  frequency and  span to verify the signal power in dBm")
###########################
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

print("Start spectrum analyzer")
# commands for spectrum analyzer
if config.spectrum:
    device_address = 'TCPIP::{0}::{1}::SOCKET'.format(config.spectrum_ip_address_india,config.port)  # Spectrum analyzer TCPIP  address
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(200,spectrum_analyzer)
    
#Global Parameters
frequency = config.frequency_default # frequency in MHz
power = config.power_list # list of power for testing

for powe in config.power_list:
    # continous wave generation
    freq_query,power_query = SignalGeneration.continous_wave_generation(frequency, powe) # continous signal generation
    print(f"Frequency = {freq_query}, Power ={power_query}")
    
    # commands for spectrum analyzer
    if config.spectrum:# spectrum commands for automation
        cf = frequency  # center frequency on measuring device
        spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)
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
            
    print(f"Keep Center frequency at 1GHz with Frequency = {freq_query}Hz span and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}")
    print(" Press on the Peak search button on Spectrum analyzer and Note down the frequency and power of desired signal")
    print("Press enter for next power test")
    input()
    
# disconnect instrument
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
