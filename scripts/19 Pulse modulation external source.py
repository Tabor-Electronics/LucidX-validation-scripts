print("<DESCRIPTION> Test description :- This script will generate a signal with pulse modulation for different acrrier frequencies.\nAn oscilloscope is a better equipmet to see th eoutput of pulse modulation (make sure it supports higher frequency range<DESCRIPTION>")
###########################
###START OF SCRIPT###
#Run this script on debug mode, keeping the debugger on line number 30 for better results

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles import config
from SourceFiles.for_the_gui import DevicePrint

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

# print("Start Oscilloscope")
devicePrintCmd.msg_user.set('Start Oscilloscope')
devicePrintCmd.Print()

#Global Parameters
frequency = config.frequency_default
power = config.power_default

# continous wave generation
freq_query, power_query = SignalGeneration.continous_wave_generation(frequency,power)  # continous signal generation
# print(f"Frequency = {freq_query}, Power ={power_query}")
devicePrintCmd.msg_gui.set(f'freq={freq_query}::p0.00::n0.00,pow={power_query}::p0.00::n0.00')
devicePrintCmd.Print()

devicePrintCmd.msg_user.set('set some pulse signal width 10%, and frequency 1 Hz from external signal source and continue the test')
devicePrintCmd.Print()
# print('set some pulse signal width 10%, and frequency 1 Hz from external signal source and continue the test')
# print("Press enter")
devicePrintCmd.msg_user.set('Press enter for next frequency test')
devicePrintCmd.Print()
input()

PulseModulation.pulse_modulation_external_on()
devicePrintCmd.msg_user.set('Change the external source  frequnecy and Note the signal on Oscilloscope')
devicePrintCmd.Print()


# disconnect
PulseModulation.pulse_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
