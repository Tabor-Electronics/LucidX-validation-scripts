"""
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.
"""
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PhaseModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import  LucidCmd

#Establishing connection with LUCIDX
handle =config.handle
Lucid_functions.reset(config.handle)

frequency = config.frequency_default
power = config.power_default
pm_freq = config.pm_freq_default
deviation = config.pm_deviation_default
internal_source = config.frequencies
for frequency in internal_source:
    SignalGeneration.continous_wave_generation(frequency, config.power_default)
    PhaseModulation.phase_modulation_internal_on(pm_freq, deviation)
PhaseModulation.phase_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)# disconnect instrument
###END OF SCRIPT###