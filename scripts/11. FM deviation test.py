"""
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.
"""


###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,FrequencyModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.calculations import ErrorCalculation
from SourceFiles.lucid_cmd import  LucidCmd

#Establishing connection with LUCIDX
handle = 'TCPIP::{0}::{1}::SOCKET'.format(config.lucid_ip_address,config.port)  #Lucid TCPIP address
Lucid_functions.reset(handle)

if config.spectrum:
    device_address = 'TCPIP::{0}::{1}::SOCKET'.format(config.spectrum_ip_address_india,config.port)  # Spectrum analyzer TCPIP  address
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(200,spectrum_analyzer)
    spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
    threshold = -40
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)

frequency = 1000
cf = frequency
SignalGeneration.continous_wave_generation(frequency, config.power_default)
# # keep the scope time resolution around 50 us/
for deviation in config.fm_deviation_list:

    FrequencyModulation.frequency_modulation_internal_on(config.fm_freq_default, deviation)

    if config.spectrum:
        span_freq =3*deviation/1e6
        spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)

        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
        spectrum_methods.set_marker_at_peak(spectrum_analyzer)

        freq_fm =spectrum_methods.get_marker_frequency(spectrum_analyzer)

        dev = abs(freq_fm-cf)
        deviation_err = ErrorCalculation.percent_error(dev, deviation)
        print(deviation_err)
        #spectrum_methods.get_delta_left_peak(spectrum_analyzer)

# disconnect
FrequencyModulation.frequency_modulation_off()
