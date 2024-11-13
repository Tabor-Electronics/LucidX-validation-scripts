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
power = 5
SignalGeneration.continous_wave_generation(frequency, config.power_default)

for rep_rate in config.pulse_repetition_rate:

    PulseModulation.pulse_modulation_internal_on(rep_rate, config.pulse_width_default)

    if config.spectrum:
        span_freq =3*rep_rate/1e6
        spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)
        spectrum_methods.set_marker_at_peak(spectrum_analyzer)
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
        spectrum_methods.get_delta_left_peak(spectrum_analyzer)

# disconnect
PulseModulation.pulse_modulation_off()

#
# handle = 'TCPIP0::192.168.7.1::5025::SOCKET'
# Lucid_functions.lsx_connection(handle)
# status_lsx = Lucid_functions.reset_and_clear(handle) # reset and clear the lucid x desktop
# if status_lsx:
#     print("Factory reset done LSX")
# else:
#     print("Error while reseting the LucidX module")
#
# # spectrum = True
# # if spectrum:
# #     spectrum_address = 'TCPIP::192.168.0.57::5025::SOCKET' # Spectrum analyzer TCPIP  address
# #     spectrum_analyzer = spectrum_methods.connect_spectrum_via_lan(spectrum_address)
# #     status_sa = spectrum_methods.reset_and_clear_sa(spectrum_analyzer) # reset and clear the measuring device spectrum analyzer
# #     if status_sa:
# #         print("Factory reset done Spectrum Analyzer")
# #     else:
# #         print("Error while reseting spectrum analyzer")
#
# # continous wave generation
# frequency = 1000e6
# power = 5
# Lucid_functions.send_scpi_command(':FREQuency {0}'.format(frequency), handle)
# Lucid_functions.send_scpi_command(':POWer {0}'.format(power), handle)
# freq_query = Lucid_functions.send_scpi_query(':FREQuency?', handle)
# power_query = Lucid_functions.send_scpi_query(':POWer?', handle)
# Lucid_functions.send_scpi_command(':OUTPut ON', handle)
# outp_query = Lucid_functions.send_scpi_query(':OUTP?', handle)
# error = Lucid_functions.get_lucid_error(handle) #Error SCPI query
# # Internal source commands for AM
#   # 1 to 1E6
# # keep the scope time resolution around 50 us/
# for pulse_freq in pulse_frequencies:
#     Lucid_functions.send_scpi_command(':PULS:SOUR INT', handle)
#     Lucid_functions.send_scpi_command(':PULS:INT:FREQ {0}'.format(pulse_freq), handle)
#     Lucid_functions.send_scpi_command(':PULS:WIDT 322e-9', handle)
#     Lucid_functions.send_scpi_command(':PULS ON', handle)
#     error = Lucid_functions.get_lucid_error(handle)
# #######################################################
# # disconnect
# Lucid_functions.send_scpi_command(':PULS OFF', handle)
# Lucid_functions.send_scpi_command(':OUTPut OFF', handle)
# error = Lucid_functions.get_lucid_error(handle)
# print("test completed")