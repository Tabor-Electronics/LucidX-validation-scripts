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

# if config.spectrum:
#     device_address = 'TCPIP::{0}::{1}::SOCKET'.format(config.spectrum_ip_address_india,config.port)  # Spectrum analyzer TCPIP  address
#     spectrum_analyzer,status = spectrum_methods.reset(device_address)
#     spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
#     spectrum_methods.set_span_freq(200,spectrum_analyzer)
#     spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
#     threshold = -40
#     spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)

frequency = config.frequency_default
power = config.power_default
SignalGeneration.continous_wave_generation(frequency, config.power_default)

for rep_rate in config.pulse_repetition_rate:
    rep_period = 1/rep_rate
    pulse_width = config.pulse_width_default

    PulseModulation.pulse_modulation_internal_on(rep_rate,pulse_width)

    # if config.spectrum:
    #     cf = frequency
    #     span_freq =3*rep_rate/1e6
    #     spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)
    #     spectrum_methods.set_marker_at_peak(spectrum_analyzer)
    #     spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
    #     spectrum_methods.get_delta_left_peak(spectrum_analyzer)

# disconnect
# PulseModulation.pulse_modulation_off()
# Lucid_functions.disconnect_lucid(handle)

