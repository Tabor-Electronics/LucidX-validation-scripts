"""
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.
"""
from functions_v1 import Lucid_functions,AmplitudeModulation
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config

handle = config.handle
#Establishing connection with LUCIDX
Lucid_functions.reset(handle)
if config.spectrum:
    spectrum_address = 'TCPIP::192.90.70.36::5025::SOCKET'  # Spectrum analyzer TCPIP  address
    spectrum_analyzer = spectrum_methods.connect_spectrum_via_lan(spectrum_address)
    status_sa = spectrum_methods.reset_and_clear_sa(
        spectrum_analyzer)  # reset and clear the measuring device spectrum analyzer
    if status_sa:
        print("Factory reset done Spectrum Analyzer")
    else:
        print("Error while reseting spectrum analyzer")

frequency_list = [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]
power = 5
for freq in frequency_list:
    cf = freq
    Lucid_functions.send_scpi_command(':FREQuency {0}e6'.format(freq), handle)
    Lucid_functions.send_scpi_command(':POWer {0}'.format(power), handle)
    freq_query = Lucid_functions.send_scpi_query(':FREQuency?', handle)
    power_query = Lucid_functions.send_scpi_query(':POWer?', handle)
    Lucid_functions.send_scpi_command(':OUTPut ON', handle)
    outp_query = Lucid_functions.send_scpi_query(':OUTP?', handle)
    error = Lucid_functions.get_lucid_error(handle)

    # Internal source commands for AM
    am_frequencies = [100, 1000, 2000, 30000, 100000]
    # keep the scope time resolution around 50 us/
    for am_freq in am_frequencies:

        Lucid_functions.send_scpi_command(':AM:SOUR INT', handle)
        Lucid_functions.send_scpi_command(':AM:INT:FREQ {0}'.format(am_freq), handle)
        Lucid_functions.send_scpi_command(':AM:DEPT 50', handle)
        Lucid_functions.send_scpi_command(':AM ON', handle)

        error = Lucid_functions.get_lucid_error(handle)
        if spectrum:
            span_freq = 200
            threshold = -40
            spectrum_methods.set_reference_power(power + 7, spectrum_analyzer)

            spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)
            spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
            spectrum_methods.set_marker(spectrum_analyzer)
            span_freq = float(4 * am_freq) / 1e6
            spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)
            spectrum_methods.set_marker_at_peak(spectrum_analyzer)
            spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)
            spectrum_methods.get_delta_left_peak(spectrum_analyzer)

AmplitudeModulation.amplitude_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)# disconnect instrument
###END OF SCRIPT###