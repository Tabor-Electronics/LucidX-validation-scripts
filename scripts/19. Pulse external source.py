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
power = config.power_default
SignalGeneration.continous_wave_generation(frequency, power)
print('set some pulse signal width 10%, and frequency 1 Hz from external signal source and continue the test')
PulseModulation.pulse_modulation_external_on()

if config.spectrum:
    span_freq = 3 * config.fm_deviation_default / 1e6
    spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)
    spectrum_methods.set_marker_at_peak(spectrum_analyzer)
    spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
    spectrum_methods.get_delta_left_peak(spectrum_analyzer)

# disconnect
# PulseModulation.pulse_modulation_off()
