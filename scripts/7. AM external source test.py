


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
handle = config.handle
Lucid_functions.reset(handle)
if config.spectrum:
    device_address = 'TCPIP::{0}::{1}::SOCKET'.format(config.spectrum_ip_address_india,config.port)  # Spectrum analyzer TCPIP  address
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(200,spectrum_analyzer)
    spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
    threshold = -40
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)

frequency = config.frequency_default

power = config.power_default
SignalGeneration.continous_wave_generation(frequency, config.power_default)
# Internal source commands for AM
am_frequencies = [100e3,200e3,300e3]
# keep the scope time resolution around 50 us/
for ext_freq in am_frequencies:
    print(f'Connect external source with frequency {ext_freq}Hz ')
    AmplitudeModulation.amplitude_modulation_external_on()
    error = Lucid_functions.get_lucid_error(handle)
    if config.spectrum:
        cf = frequency
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
        span_freq = 1
        spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)
        spectrum_methods.set_marker_at_peak(spectrum_analyzer)
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
        spectrum_methods.get_delta_left_peak(spectrum_analyzer)

# disconnect
AmplitudeModulation.amplitude_modulation_off()