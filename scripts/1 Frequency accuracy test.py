print("Test description :- This test gives out the value frequency and  power and compare the given threshold to conclude the result for Accuracy with given frequency")
print("Steps:- \n1) In this script we are using spectrum analyzer as a measuring device.\n2) We will set a center  frequency and  span to verify the signal frequency")

###########################
###START OF SCRIPT###
#Run this script on debug mode, keepimng the debugger on line number 30 for better results

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

print("Start spectrum analyzer")
# commands for spectrum analyzer
if config.spectrum:
    spectrum_analyzer,status = spectrum_methods.reset(config)
    if status:
        spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200,spectrum_analyzer)

#Global Parameters
frequencies = config.frequencies # list of frequencies for testing
power = config.power_default # power in dBm

for frequency in frequencies:
    # continous wave generation
    freq_query,power_query =SignalGeneration.continous_wave_generation(frequency, power) # continous signal generation
    print(f"Frequency = {freq_query}, Power ={power_query}")

    # commands for spectrum analyzer
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
    
    print(f"Keep Center frequency on Spectrum at Frequency = {freq_query}Hz with 200Mhz span and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}dBm")
    print(" Press on the Peak search button on Spectrum analyzer and Note down the frequency and power of desired signal")
    print("Press enter for next frequency test")
    input()
    
# disconnect instrument
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
