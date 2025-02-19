"""
1) In this script we are using spectrum analyzer as a measuring device
"""
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

if config.spectrum:
    device_address = 'TCPIP::{0}::{1}::SOCKET'.format(config.spectrum_ip_address_india, config.port)  # Spectrum analyzer TCPIP  address
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(200,spectrum_analyzer)
    spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
    threshold = -40
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)



frequency = config.frequency_default
cf = frequency
power = 5
# rep_rate =config.pulse_repetition_rate_default
SignalGeneration.continous_wave_generation(frequency, config.power_default)

for pulse_width in config.pulse_width_list:

    rep_rate = 1/(pulse_width)
    PulseModulation.pulse_modulation_internal_on(rep_rate,pulse_width)

 
# disconnect
PulseModulation.pulse_modulation_off()
