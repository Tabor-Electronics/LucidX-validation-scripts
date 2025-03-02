print("Test description :- This test gives out the value frequency and  power and compare the given threshold to conclude the result for resolution of power  given frequency")
print("Steps:- \n1) In this script we are using spectrum analyzer as a measuring device.\n2) We will set a center  frequency and  span to verify the signal power in dBm")

###########################
###START OF SCRIPT###
#Run this script on debug mode, keepimng the debugger on line number 32 for better results

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
    spectrum_analyzer,status = spectrum_methods.reset(config)
    if status:
        spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200,spectrum_analyzer)

#Global Parameters
frequency = 2e3 # frequency in MHz
x= config.power_default
resolution =config.power_resolution
power_list= [x, x+resolution, x-resolution]

for power in power_list:
    # continous wave generation
    freq_query, power_query = SignalGeneration.continous_wave_generation(frequency,power)  # continous signal generation
    print(f"Frequency = {freq_query}, Power ={power_query}")
    
    # commands for spectrum analyzer
    if config.spectrum:  # spectrum commands for automation
        cf = frequency  # center frequency on measuring device in MHz
        spectrum_methods.set_reference_power(power + 5, spectrum_analyzer)#  step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)# step 2) set span frequency on spectrum
        spectrum_methods.get_centre_frequency(cf, spectrum_analyzer)# step 3) set center frequency on spectrum
        spectrum_methods.set_marker_at_peak(spectrum_analyzer)# step 4)  add a marker and set it to peak

        spectrum_methods.marker_to_center_frequency(spectrum_analyzer) #step 5) move marker to center frequency
        freq_out,power_max = spectrum_methods.set_marker(spectrum_analyzer)  # step 6) Read marker x (frequency) and y (power)

        error_value = abs(float(freq_out) - cf)  # Calculating difference between input and output frequency
        power_error = abs(float(power_max) - power)  # Calculating difference between input and output power
        frequency_th = 0.1  # frequency threshold in term of percentage of input frequency
        power_th = 1  # power threshold in dBm
        if (error_value < (frequency_th * cf)) and (power_error < power_th):  # Condition to conclude the test result
            print("Test pass for Frequency = {0} MHz".format(cf))
        else:
            print("Test fail  for Frequency = {0} MHz".format(cf))


    print(f"Keep Center frequency on Spectrum at Frequency = {freq_query}Hz with 200 Khz span (move accordingly) and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}")
    print("Press on the Peak search button on Spectrum analyzer and Note down the frequency and power of desired signal")
    print("Press enter for next power")
    input()
    
# disconnect instrument
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###

