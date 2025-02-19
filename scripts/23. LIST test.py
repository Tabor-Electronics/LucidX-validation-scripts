
''' In this script List functionality is implemented
it requires follwoing paarmaeters
1) Frequencies (Hz): Specifies the frequency values for all lists in Hertz.
2) Power (dBm): Defines the power levels for all lists in decibels-milliwatts (dBm).
3) Dwell Time (s): Indicates the duration (in seconds) for each list entry.
4) Advance: Determines whether the sequence runs or waits:
        a) 0 for "Wait"
        b) 1 for "Run"
5) Ensure the last list entry always has value of 1, while the others remain 0.
5) Step Numbers: There's no need to define step numbers, as the sequence works based on the order in which lists are defined.'''
############Start of script############

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config,create_list_data
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

'''for each list, theer is different parameters
1) frequencies for all the list in Hz
2) power for all list in dBm
3) dwell time in terms of seconds
4) advance is the run/wait option make it 0/1 as required
5) no need to modify last entry as it will be '1' fro th elast list otherwise 0
6) no need to add step number as well, it will work as order it is defined
'''
frequency_list = [1e9,2e9,3e9]#,4e9,5e9] #frequency in Hz
power_list = [5,5,5,5,5] #power in dBm
dwell_time = [1,2,2,2,2] ##dwell time in seconds
adv = [0,0,0,0,0]
last_entry = 0


for i in range(len(frequency_list)):
    if i == (len(frequency_list)-1):
        last_entry =1
    
    Lucid_functions.send_scpi_command(LucidCmd.LIST_DEF.format(i+1, frequency_list[i], power_list[i], last_entry, adv[i],dwell_time[i]), handle)
    Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('ON'), handle)
    Lucid_functions.send_scpi_command(LucidCmd.LIST_ON, handle)
for i in range(len(frequency_list)):
    list_number = i+1
    list_def = Lucid_functions.send_scpi_query(LucidCmd.LIST_DEF_Q.format(list_number), handle)
    print(list_def)
    
Lucid_functions.send_scpi_command(LucidCmd.LIST_OFF, handle)
Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('OFF'), handle)
##################End of script#############

