print("<DESCRIPTION> Test description :- This script will generate a signal with pulse modulation for different acrrier frequencies.\nAn oscilloscope is a better equipmet to see th eoutput of pulse modulation (make sure it supports higher frequency range<DESCRIPTION>")
###########################
###START OF SCRIPT###
#Run this script on debug mode, keeping the debugger on line number 30 for better results

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles import config
from SourceFiles.oscilloscope_functions import FetchResults
from SourceFiles.for_the_gui import DevicePrint

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

devicePrintCmd.msg_user.set('Connecting to the Oscilloscope')
devicePrintCmd.Print()
if config.scope:
    # Set the oscilloscope's VISA address
    scope_address = "TCPIP0::192.168.0.92::INSTR"  # Update with actual VISA address
    # Create an object of FetchResults
    oscilloscope = FetchResults(scope_address)
    # print("Start Oscilloscope")
    oscilloscope.connect(scope_address)

#Global Parameters
frequency = config.frequency_default
power = config.power_default
ext_pulse_rr_list =config.ext_pulse_rr_list

# continous wave generation
freq_query, power_query = SignalGeneration.continous_wave_generation(frequency,power)  # continous signal generation
# print(f"Frequency = {freq_query}, Power ={power_query}")
# devicePrintCmd.msg_gui.set(f'freq={freq_query}::p0.00::n0.00,pow={power_query}::p0.00::n0.00')
devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query,power_query))
devicePrintCmd.Print()

devicePrintCmd.msg_user.set('set some pulse signal width 10%, and frequency 1 Hz from external signal source and continue the test')
devicePrintCmd.Print()
# print('set some pulse signal width 10%, and frequency 1 Hz from external signal source and continue the test')
# print("Press enter")
devicePrintCmd.msg_user.set('Press enter for next frequency test')
devicePrintCmd.Print()
input()
for ext_freq in ext_pulse_rr_list:
	PulseModulation.pulse_modulation_external_on()
	devicePrintCmd.msg_user.set('Change the external source frequnecy and Note the signal on Oscilloscope')
	devicePrintCmd.Print()
	# SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
	if config.scope:
		time_scale = (1 / ext_freq) / 2  # 0.1/pulse_rr ## 500ns for prr =1us
		frequency, burst_period, burst_width, burst_interval = oscilloscope.get_pulse_mod_parameters(1, time_scale)
		# print(f"Pulse Modulation Parameters:")
		# print(f"Frequency: {frequency} Hz")
		# print(f"Burst Period: {burst_period} sec")
		# print(f"Burst Width: {burst_width} sec")
		# print(f"Burst Interval: {burst_interval} sec")
		
		# SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
		error = abs(float(1 / burst_period) - float(ext_freq))
		threshold = float(0.01 * ext_freq)
		results = error < threshold
		print(results)
		if results:
			print(f'Test pass for Pulserepitition rate of {ext_freq} ')
			# print(f'Test pass for Frequency = {freq_in} MHz')
			devicePrintCmd.msg_user.set(f'Test pass for Pulserepitition rate of {ext_freq} ')
			devicePrintCmd.Print()
		else:
			print(f'Test fail for Pulse repitition rate of {ext_freq} ')
			devicePrintCmd.msg_user.set(f'Test Fail for Pulse repitition rate of {ext_freq} ')
			devicePrintCmd.Print()
	
	# SECTION 5 - Closing the instruments
	PulseModulation.pulse_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
oscilloscope.disconnect()  # Disconnect the oscilloscope
###END OF SCRIPT###


# disconnect
PulseModulation.pulse_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
