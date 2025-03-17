print("<DESCRIPTION> Test description :- This test gives out the value frequency and  power and compare the given threshold to conclude the result for accuracy with given frequency\nSteps:- \n1) In this script we are using spectrum analyzer as a measuring device.\n2) We will set a center  frequency and  span to verify the signal frequency</DESCRIPTION>")
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.for_the_gui import DevicePrint

# SECTION 1- Connect LUCIDX, create object of Device print, connect to measuring device
handle = config.handle
Lucid_functions.reset(handle)  # Establishing connection with LUCIDX

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

devicePrintCmd.msg_user.set('Connecting to the spectrum analyzer')
devicePrintCmd.Print()
# commands for spectrum analyzer
if config.spectrum:
	spectrum_analyzer, status = spectrum_methods.reset(config)
	if status:
		spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
		spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz

# SECTION 2- Defining parameters and generate signal form LUCIDX
# Global Parameters
frequencies = config.frequencies  # list of frequencies for testing
power = config.power_default  # power in dBm

for freq_in in frequencies:
	# continous wave generation
	freq_query, power_query = SignalGeneration.continous_wave_generation(freq_in, power)  # continous signal generation
	devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query,power_query))
	devicePrintCmd.Print()
	# 	# print(f"Frequency = {freq_query}, Power ={power_query}")
	#     # Print_function.print_freq_pow_to_gui(freq=freq_query,pow=power_query)
	# devicePrintCmd.msg_user.set(f'Keep Center frequency on Spectrum at Frequency = {freq_query}Hz with 200Mhz span and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}dBm')
	# devicePrintCmd.Print()
	# # Print_function.print_to_user(f"Keep Center frequency on Spectrum at Frequency = {freq_query}Hz with 200Mhz span and verify the signal on the screen for Frequency = {freq_query}, Power ={power_query}dBm")
	# devicePrintCmd.msg_user.set('Press on the Peak search button on Spectrum analyzer and Note down the frequency and power of desired signal')
	# devicePrintCmd.Print()
	
	# SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
	if config.spectrum:  # spectrum commands for automation
		cf = freq_in  # center frequency on measuring device
		spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
		freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
		
		# devicePrintCmd.msg_gui.set('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
		devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out,power_max))
		devicePrintResp.Print()
		
		# SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
		error_value = abs(float(freq_out) - freq_in)  # Calculating difference between input and output frequency
		power_error = abs(float(power_max) - config.power_default)  # Calculating difference between input and output power
		frequency_th = 0.1  # frequency threshold in terms of percentage of input frequency
		power_th = 1  # power threshold in dBm
		# if (error_value < (frequency_th * freq_in)) and (power_error < power_th):  # Condition to conclude the test result
		if (error_value < (frequency_th * freq_in)):
			# print(f'Test pass for Frequency = {freq_in} MHz')
			devicePrintCmd.msg_user.set(f'Test pass for Frequency = {freq_in} MHz')
			devicePrintCmd.Print()
		else:
			#print(f'Test Fail for Frequency = {freq_in} MHz')
			devicePrintCmd.msg_user.set(f'Test Fail for Frequency = {freq_in} MHz')
			devicePrintCmd.Print()
	
	devicePrintCmd.msg_user.set('Press enter for next frequency test')
	devicePrintCmd.Print()
	input()

# SECTION 5 - Closing the instruments
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
