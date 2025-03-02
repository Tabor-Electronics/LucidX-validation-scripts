print("Test description :-  This test run for Amplitude modulation of a given different carrier signal , baseband frequnecy and depth ")
print("The resultant signal can be seen on spectrum analyzer ")

from functions_v1 import Lucid_functions,SignalGeneration, AmplitudeModulation
from spectrum_analyser_functions import spectrum_methods
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
frequency= config.frequency_default
power = config.power_default
am_ext_frequencies = config.am_ext_frequencies

freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, power)
print(f"Frequency = {freq_query}, Power ={power_query}")

AmplitudeModulation.amplitude_modulation_external_on()

for ext_freq in am_ext_frequencies:
    # extranal source commands for AM
    print(f"Generate external signal with Frequency = {ext_freq}Hz using a signal generator to AM external input of Lucid desktop")
    print("Press on the Peak search button on Spectrum analyzer and a delta marker on the left/right on the peak and Note down the frequency and power of desired modulated signal")
    print("Press enter for next frequency test")
    input()
    
    error = Lucid_functions.get_lucid_error(handle)

# commands for spectrum analyzer
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