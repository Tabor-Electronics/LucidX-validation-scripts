print("Test description :-  This test run for Phase modulation of a given carrier signal , baseband frequnecy and  different  deviation")
# print("The resultant signal can be seen on spectrum analyzer ")

# NOT SURE HOW TO TEST!
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PhaseModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import  LucidCmd

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
    spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
    threshold = -40
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)

#Global parameters
frequency = config.frequency_default
power = config.power_default
pm_freq= config.pm_freq_default
deviation_list = config.pm_deviation_list
# continous wave generation
freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, power)
print(f"Frequency = {freq_query}, Power ={power_query}")
print(f"Keep Center frequency on Spectrum at Frequency = {freq_query}Hz with 200Mhz span and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}dBm")

for deviation in deviation_list:
    pm_freq_q, pm_dev_q, pm_status_q = PhaseModulation.phase_modulation_internal_on(pm_freq, deviation)
    print(f"PM Frequency = {pm_freq_q}, Deviation={pm_dev_q}")
    print("Press enter for next frequency test")
    input()
    
# disconnect
PhaseModulation.phase_modulation_off()
