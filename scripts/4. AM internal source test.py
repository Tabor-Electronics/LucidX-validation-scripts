"""
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.
"""
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,AmplitudeModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import  LucidCmd

#Establishing connection with LUCIDX
Lucid_functions.reset(config.handle)

if config.spectrum:
    device_address = 'TCPIP::{0}::{1}::SOCKET'.format(config.spectrum_ip_address_india,config.port)  # Spectrum analyzer TCPIP  address
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(200,spectrum_analyzer)
    spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
    threshold = -40
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)

power = config.power_default
am_freq = config.am_freq_default
internal_source = config.frequencies
for frequency in internal_source:
    SignalGeneration.continous_wave_generation(frequency, power)
    AmplitudeModulation.amplitude_modulation_internal_on(am_freq, config.am_depth_default)
    if config.spectrum:
        cf = frequency
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
        span_freq = float(4*am_freq)/1e6
        spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)
        spectrum_methods.set_marker_at_peak(spectrum_analyzer)
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
        spectrum_methods.get_delta_left_peak(spectrum_analyzer)

# disconnect
AmplitudeModulation.amplitude_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)# disconnect instrument
###END OF SCRIPT###