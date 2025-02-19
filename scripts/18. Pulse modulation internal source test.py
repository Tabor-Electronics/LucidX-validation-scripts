"""
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.
"""
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd

#Establishing connection with LUCIDX
Lucid_functions.reset(config.handle)

frequency = config.frequency_default
power = config.power_default
pulse_rr = 2
width =100e-3

internal_source = config.frequencies
for frequency in internal_source:
    SignalGeneration.continous_wave_generation(frequency, config.power_default)
    pulse_rr_q,width_q,status = PulseModulation.pulse_modulation_internal_on(pulse_rr,width)
    print(f"frequency = {frequency}MHz")
    print(f"Pulse repitition rate {pulse_rr_q}")
    print(f"and Pulse width = {width_q}")
  
# disconnect
PulseModulation.pulse_modulation_off()