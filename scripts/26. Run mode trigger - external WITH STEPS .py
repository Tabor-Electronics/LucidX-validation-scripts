"""
In this script we have done amplitude modulation on a signal and then used trigger with mentioned timer and once count
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please comment spectrum related commands or make the "config.spectrum = False"
"""
############Start of script############

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,AmplitudeModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config,create_list_data
from SourceFiles.lucid_cmd import LucidCmd

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)
frequency =config.frequency_default
power = config.power_default
am_freq = 10e3
am_depth = 90

print("Start spectrum analyzer")
# commands for spectrum analyzer
if config.spectrum:
    device_address =config.spectrum_tcpip
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(config.default_span,spectrum_analyzer)
    spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
    threshold = -40
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)
    #####################################################################

# insert some signal to be triggered

SignalGeneration.continous_wave_generation(frequency,power)
AmplitudeModulation.amplitude_modulation_internal_on(am_freq,am_depth)

Lucid_functions.send_scpi_command(':INIT:CONT OFF',handle)
Lucid_functions.send_scpi_command(':TRIG:ADV STEP',handle)
Lucid_functions.send_scpi_command(':TRIG:SOUR EXT',handle)
