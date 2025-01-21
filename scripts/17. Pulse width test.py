"""
1) In this script we are using spectrum analyzer as a measuring device
"""

###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import  LucidCmd

#Establishing connection with LUCIDX
handle = 'TCPIP::{0}::{1}::SOCKET'.format(config.lucid_ip_address,config.port)  #Lucid TCPIP address
Lucid_functions.reset(handle)


frequency = config.frequency_default
power = config.power_default
SignalGeneration.continous_wave_generation(frequency, config.power_default)

for pulse_width in config.pulse_width_list:
    rep_rate = 1e-6#config.pulse_repetition_rate_default
    rep_period = 1/rep_rate
    # pulse_width = 3.2e-6

    PulseModulation.pulse_modulation_internal_on(rep_rate,pulse_width)



# disconnect
# PulseModulation.pulse_modulation_off()
# Lucid_functions.disconnect_lucid(handle)

