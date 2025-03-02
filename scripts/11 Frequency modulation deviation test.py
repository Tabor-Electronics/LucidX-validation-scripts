print("Test description :-  This test run for Frequency modulation of a given carrier signal ,baseband frequnecy and different deviation")
print("The resultant signal can be seen on spectrum analyzer ")

###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,FrequencyModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.calculations import ErrorCalculation
from SourceFiles.lucid_cmd import  LucidCmd
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
        threshold = -40
        spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)

#Global parameters
frequency = config.frequency_default
power = config.power_default
fm_freq = config.fm_freq_default
deviations = config.fm_deviation_list

SignalGeneration.continous_wave_generation(frequency, config.power_default)
# # keep the scope time resolution around 50 us/
for deviation in deviations:
    # Internal source commands for FM
    fm_source_q, fm_freq_q, fm_dev_q = FrequencyModulation.frequency_modulation_internal_on(fm_freq, deviation)
    print(f"FM Frequency = {fm_freq_q}, Deviation={fm_dev_q} \n Change the span to {5 * fm_dev_q}Hz")
    print(" Press on the Peak search button on Spectrum analyzer and a delta marker on the left/right on the peak and Note down the deviation for desired FM signal")
    print("Press enter for next frequency test")
    input()
    
# commands for spectrum analyzer
if config.spectrum:
        cf = frequency
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
