print("Test description :- This script will generate a signal with pulse modulation for different acrrier frequencies")
print("An oscilloscope is a better equipmet to see th eoutput of pulse modulation (make sure it supports higher frequency range)")

###########################
###START OF SCRIPT###
#Run this script on debug mode, keeping the debugger on line number 30 for better results

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles import config

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

print("Start Oscilloscope")

#Global Parameters
frequency = config.frequency_default
power = config.power_default

# continous wave generation
freq_query, power_query = SignalGeneration.continous_wave_generation(frequency,power)  # continous signal generation
print(f"Frequency = {freq_query}, Power ={power_query}")

print('set some pulse signal width 10%, and frequency 1 Hz from external signal source and continue the test')
print("Press enter")
input()
PulseModulation.pulse_modulation_external_on()
print("Change the external source  frequnecy and Note the signal on Oscilloscope")


# disconnect
PulseModulation.pulse_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
