print("<DESCRIPTION> Test description :- This test gives out the value frequency and  power and compare the given threshold to conclude the result for Accuracy with given frequency\nSteps:- \n1) In this script we are using spectrum analyzer as a measuring device.\n2) We will set a center  frequency and  span to verify the signal frequency</DESCRIPTION>")
###########################
###START OF SCRIPT###
#Run this script on debug mode, keeping the debugger on line number 30 for better results

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.for_the_gui import Print_function

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

Print_function.print_to_user("Start spectrum analyzer")

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
    Print_function.print_freq_pow_to_gui(freq=freq_query,pow=power_query)
    # print(f"Frequency = {freq_query}, Power ={power_query}")
    
    Print_function.print_to_user(f"Keep Center frequency on Spectrum at Frequency = {freq_query}Hz with 200Mhz span and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}dBm")
    Print_function.print_to_user("Press on the Peak search button on Spectrum analyzer and Note down the frequency and power of desired signal")
    Print_function.print_to_user("Press enter for next frequency test")
    input()
    
# disconnect instrument
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
