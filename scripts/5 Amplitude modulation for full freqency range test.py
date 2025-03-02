print("Test description :-  This test run for Amplitude modulation of a given different carrier signal , baseband frequnecy and depth ")
print("The resultant signal can be seen on spectrum analyzer ")

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration, AmplitudeModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

print("Start spectrum analyzer")
# commands for spectrum analyzer
if config.spectrum:
    spectrum_analyzer,status = spectrum_methods.reset(config)
    if status:
        spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200,spectrum_analyzer)

#Global parameters
frequency_list = config.frequencies
power = config.power_default
am_freq = config.am_freq_default
depth = config.am_depth_default

for freq in frequency_list:
    # continous wave generation
    freq_query,power_query =SignalGeneration.continous_wave_generation(freq,power)
    print(f"Frequency = {freq_query}, Power ={power_query}")
    print(f"Keep Center frequency on Spectrum at Frequency = {freq_query}Hz with 200Mhz span and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}dBm")

    # Internal source commands for AM
    am_source_q,am_freq_q,am_depth_q = AmplitudeModulation.amplitude_modulation_internal_on(am_freq,depth)
    print(f"AM Frequency = {am_freq_q}, Depth ={am_depth_q} \n Change the span to {5*am_freq_q}Hz")
    print(" Press on the Peak search button on Spectrum analyzer and a delta marker on the left/right on the peak and Note down the frequency and power of desired modulated signal")
    print("Press enter for next frequency test")
    input()
    if config.spectrum:
        cf = freq
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

# disconnect instrument
AmplitudeModulation.amplitude_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###