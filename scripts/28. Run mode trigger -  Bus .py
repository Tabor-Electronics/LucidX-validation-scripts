"""
In this script a pattern od desired ontime offtine is define and a bus (manual) trigger is activated using a command to seee the pattern on spectrum analyzer.

1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.

"""
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd

# Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

if config.spectrum:
    device_address = config.spectrum_tcpip
    spectrum_analyzer, status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5,
                                         spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(config.default_span, spectrum_analyzer)
    spectrum_methods.set_reference_power(config.power_default + 7, spectrum_analyzer)
    threshold = -40
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)

'''for each pattern, theer is different parameters
1) ontime /offtime in seconds
2) pattern number of repetition for each Pattern
3) last entry- if it sthe last enter for pattern list
4) Number of bus trigger applied.
'''
frequency = config.frequency_default
power = config.power_default
SignalGeneration.continous_wave_generation(frequency, power) # continous signal generation
ontime = [1,2]
offtime = [1,2]
repitition = [1,1]
last_entry = 0
no_of_triggers =5

for i in range(len(ontime)):
    step_number = i + 1
    if i == (len(ontime) - 1):
        last_entry = 1
    Lucid_functions.send_scpi_command(LucidCmd.PATTERN_DEF.format(i + 1, ontime[i], offtime[i], repitition[i], last_entry), handle)
    list_def = Lucid_functions.send_scpi_query(LucidCmd.PATTERN_DEF_Q.format(step_number), handle)
    print(list_def)
Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('ON'), handle)
Lucid_functions.send_scpi_command(LucidCmd.PATTERN_ON, handle)

Lucid_functions.send_scpi_command(':INIT:CONT OFF', handle)
temp= Lucid_functions.send_scpi_query(':INIT:CONT?', handle)
Lucid_functions.send_scpi_command(':TRIG:ADV STEP', handle)
temp= Lucid_functions.send_scpi_query(':TRIG:ADV?', handle)
Lucid_functions.send_scpi_command(':TRIG:SOUR BUS', handle)
temp= Lucid_functions.send_scpi_query(':TRIG:SOUR?', handle)
for trg in range(int(no_of_triggers)):
    
    Lucid_functions.send_scpi_command('*TRG', handle)
    print("trigger applied")

# Lucid_functions.send_scpi_command(LucidCmd.PATTERN_OFF, handle)
# Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('OFF'), handle)


