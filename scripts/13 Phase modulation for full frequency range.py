print("Test description :-  This test run for Phase modulation of a given carrier signal ,  different  baseband frequnecy and deviation")
# print("The resultant signal can be seen on spectrum analyzer ")

# NOT SURE HOW TO TEST!

###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PhaseModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config


#Establishing connection with LUCIDX
handle =config.handle
Lucid_functions.reset(config.handle)
print("Start spectrum analyzer")

#Global parameters
frequency = config.frequencies
power = config.power_default
pm_freq = config.pm_freq_default
deviation = config.pm_deviation_default
internal_source = config.frequencies

for frequency in frequency:
    # continous wave generation
    freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, power)
    print(f"Frequency = {freq_query}, Power ={power_query}")
    print(
        f"Keep Center frequency on Spectrum at Frequency = {freq_query}Hz with 200Mhz span and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}dBm")
    pm_freq_q,pm_dev_q,pm_status_q =PhaseModulation.phase_modulation_internal_on(pm_freq, deviation)
    print(f"PM Frequency = {pm_freq_q}, Deviation={pm_dev_q}")
    # print(
    #     " Press on the Peak search button on Spectrum analyzer and a delta marker on the left/right on the peak and Note down the frequency and power of desired modulated signal")
    print("Press enter for next frequency test")
    input()

# disconnect instrument
PhaseModulation.phase_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###