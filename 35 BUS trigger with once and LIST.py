print("<DESCRIPTION>Test description:- In this script List functionality is implemented\nBus trigger will be applied to run the list and once the trigger is cliclked the list will run and stops at the last parameetr from frequency and power list, we will copmpare th eresult to it and conclude if test pass or failed.</DESCRIPTION>")

###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration, Triggers
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config, create_list_data
from SourceFiles.lucid_cmd import LucidCmd
from SourceFiles.for_the_gui import DevicePrint
import numpy as np
import time

# SECTION 1- Connect LUCIDX, create object of Device print, connect to measuring device
handle = config.handle
Lucid_functions.reset(handle)  # Establishing connection with LUCIDX

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

devicePrintCmd.msg_user.set('Connecting to the spectrum analyzer')
devicePrintCmd.Print()

if config.spectrum:  # commands for spectrum analyzer
	spectrum_analyzer, status = spectrum_methods.reset(config)
	if status:
		#spectrum_methods.set_centre_frequency(2000, spectrum_analyzer)
		spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
		#spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz

'''for each list, there is different parameters
1) frequencies for all the list in Hz
2) power for all list in dBm
3) dwell time in terms of seconds
4) advance is the run/wait option make it 0/1 as required
5) no need to modify last entry as it will be '1' fro th elast list otherwise 0
6) no need to add step number as well, it will work as order it is defined
'''
frequency_list = [1010e6, 1020e6, 1030e6]  # ,4e9,5e9] #frequency in Hz
power_list = [5, 5, 5, 5, 5]  # power in dBm
dwell_time = [1, 2, 2, 2, 2]  ##dwell time in seconds
adv = [0, 0, 0, 0, 0]
last_entry = 0
loop= 1
desired_freq = frequency_list[len(frequency_list)-1]/1e6
desired_power = power_list[len(frequency_list)-1]

for i in range(len(frequency_list)):
	if i == (len(frequency_list) - 1):
		last_entry = 1
	
	Lucid_functions.send_scpi_command(
		LucidCmd.LIST_DEF.format(i + 1, frequency_list[i], power_list[i], last_entry, adv[i], dwell_time[i]), handle)
Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('ON'), handle)
Lucid_functions.send_scpi_command(LucidCmd.LIST_ON, handle)

for i in range(len(frequency_list)):
	list_number = i + 1
	list_def = Lucid_functions.send_scpi_query(LucidCmd.LIST_DEF_Q.format(list_number), handle)
	print("List:- ", list_def)
Triggers.bus_trigger_once(loop)
print("You must see the list on measuring device")


start_freq = min(frequency_list)
stop_freq = max(frequency_list)
steps = len(frequency_list)
if config.spectrum:
	spectrum_analyzer, status = spectrum_methods.reset(config)
	spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
	
	threshold = config.power_default - 15
	spectrum_methods.set_centre_frequency(desired_freq, spectrum_analyzer)
	spectrum_methods.set_span_freq(30, spectrum_analyzer)
	print("Press input to apply trigger")
	input()
	Lucid_functions.send_scpi_command("*TRG", handle)
	time.sleep(sum(dwell_time))
	
	freq , po = spectrum_methods.set_marker(spectrum_analyzer)
	print(freq,po)
	
	freq_error = abs(desired_freq - freq)
	fr_th = 0.1 * desired_freq
	power_error = abs(desired_power-po)
	pr_th = 1
	# SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
	if freq_error < fr_th and power_error < pr_th:
		devicePrintCmd.msg_user.set('Test pass for list with Bus trigger')
		devicePrintCmd.Print()
	else:
		devicePrintCmd.msg_user.set('Test fail for list with Bus trigger')
		devicePrintCmd.Print()
	devicePrintCmd.msg_user.set('Press enter to finish this test for bus trigger with once count/loop = {}'.format(loop))
	devicePrintCmd.Print()
	input()
	# disconnect instrument
	Lucid_functions.send_scpi_command(LucidCmd.LIST_OFF, handle)
	Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###

