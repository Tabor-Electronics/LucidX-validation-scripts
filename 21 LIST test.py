print("<DESCRIPTION>Test description:- In this script List functionality is implemented\nIt  will run a list of frequecny to test List feature</DESCRIPTION>")
# print("1) Frequencies (Hz): Specifies the frequency values for all lists in Hertz.")
# print("2) Power (dBm): Defines the power levels for all lists in decibels-milliwatts (dBm).")
# print("3) Dwell Time (s): Indicates the duration (in seconds) for each list entry.")
# print("4) Advance: Determines whether the sequence runs or waits:")
# print("\ta) 0 for 'Wait'")
# print("\tb) 1 for 'Run'")
# print("5) Ensure the last list entry always has value of 1, while the others remain 0.")
# print("6) Step Numbers: There's no need to define step numbers, as the sequence works based on the order in which lists are defined.''")
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config,create_list_data
from SourceFiles.lucid_cmd import LucidCmd
from SourceFiles.for_the_gui import DevicePrint
import numpy as np

# SECTION 1- Connect LUCIDX, create object of Device print, connect to measuring device
handle = config.handle
Lucid_functions.reset(handle)  # Establishing connection with LUCIDX

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

devicePrintCmd.msg_user.set('Connecting to the spectrum analyzer')
devicePrintCmd.Print()

if config.spectrum:# commands for spectrum analyzer
    spectrum_analyzer, status = spectrum_methods.reset(config)
    if status:
        spectrum_methods.set_centre_frequency(2000,spectrum_analyzer)
        spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz

'''for each list, there is different parameters
1) frequencies for all the list in Hz
2) power for all list in dBm
3) dwell time in terms of seconds
4) advance is the run/wait option make it 0/1 as required
5) no need to modify last entry as it will be '1' fro th elast list otherwise 0
6) no need to add step number as well, it will work as order it is defined
'''
frequency_list = [1010e6,1020e6,1030e6]#,4e9,5e9] #frequency in Hz
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
    devicePrintCmd.msg_user.set('List:- {0}'.format(list_def))
    devicePrintCmd.Print()
    # print("List:- ",list_def)

devicePrintCmd.msg_user.set('You must see the list on measuring device')
devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press input to stop the list')
devicePrintCmd.Print()
input()
start_freq = min(frequency_list)
stop_freq= max(frequency_list)
steps = len(frequency_list)
if config.spectrum:
    spectrum_analyzer, status = spectrum_methods.reset(config)
    spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
    start_freq_sa = start_freq - (0.5 * start_freq)
    stop_freq_sa = stop_freq + (0.5 * start_freq)
    threshold = config.power_default - 15
    frequencies, power = spectrum_methods.sweep_test_sa(start_freq_sa, stop_freq_sa, steps, threshold,spectrum_analyzer)
    # print(frequencies, power)
    freq_val = list(np.linspace(start_freq, stop_freq, steps))
    for i in range(len(frequencies)):
        freq_error = abs(frequencies[i] - freq_val[i])
        fr_th = 0.1 * freq_val[i]
        power_error = abs(power[i] - config.power_default)
        pr_th = 1
        # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
        if freq_error < fr_th and power_error < pr_th:
            devicePrintCmd.msg_user.set('Test pass for list frequency of {0} Hz'.format(freq_val[i]))
            devicePrintCmd.Print()
        else:
            devicePrintCmd.msg_user.set('Test fail for list frequency of {0} Hz'.format(freq_val[i]))
            devicePrintCmd.Print()
        devicePrintCmd.msg_user.set('Press enter for next frequency test')
        devicePrintCmd.Print()
        input()
    # disconnect instrument
    Lucid_functions.send_scpi_command(LucidCmd.LIST_OFF, handle)
    Lucid_functions.disconnect_lucid(config.handle)
    ###END OF SCRIPT###

