###Description - This script creates and define multiple pattern
# manual testing for desired pattern
# desired number of repetition, ontime and offtime
#
from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config,create_pattern_data
from SourceFiles.lucid_cmd import LucidCmd

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

if config.spectrum:
    device_address =config.spectrum_tcpip
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(config.default_span,spectrum_analyzer)
    spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
    threshold = -40
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)

Patternsetup = create_pattern_data.PatternData()
# Pattren 1
frequency = config.frequency_default
power = config.power_default
no_of_reps = [1,2]
ontime = [100,200]
offtime= [100,800]

for i in range(len(no_of_reps)):
    pattern_row = create_pattern_data.PatternRow(no_of_repetition=no_of_reps[i], offtime=offtime[i] * 10**3, ontime=ontime[i] * 10**3)
    Patternsetup.add_pattern_row(pattern_row)
response = Patternsetup.send_scpi_command_byte(handle)
SignalGeneration.continous_wave_generation(frequency,power)
Lucid_functions.send_scpi_command(LucidCmd.PATTERN_ON, handle)
for i in range(len(no_of_reps)):
    pattern_number = i+1
    patt_def = Lucid_functions.send_scpi_query(LucidCmd.PATTERN_DEF_Q.format(pattern_number), handle)
    print(patt_def)


# Lucid_functions.send_scpi_command(LucidCmd.PATTERN_OFF, handle)
# Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('OFF'), handle)

