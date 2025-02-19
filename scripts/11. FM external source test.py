


"""
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.
"""
"""
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.
"""


###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,FrequencyModulation
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
cf = frequency
SignalGeneration.continous_wave_generation(frequency, config.power_default)
# # keep the scope time resolution around 50 us/

deviation = 1e6
FrequencyModulation.frequency_modulation_external_on(deviation)

if config.spectrum:

    spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
    spectrum_methods.set_marker_at_peak(spectrum_analyzer)
    freq_fm =spectrum_methods.get_marker_frequency(spectrum_analyzer)
    dev = abs(freq_fm-cf)
    print(dev)
    #spectrum_methods.get_delta_left_peak(spectrum_analyzer)


FrequencyModulation.frequency_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)# disconnect instrument
###END OF SCRIPT###