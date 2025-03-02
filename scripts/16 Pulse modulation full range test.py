print("Test description :- This script will generate a signal with pulse modulation for different carrier frequencies")
print("An oscilloscope is a better way to see the output of pulse modulation (make sure it supports higher frequency range)")

###########################
###START OF SCRIPT###
#Run this script on debug mode, keeping the debugger on line number 28 for better results

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles import config

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

print("Start Oscilloscope")

#Global Parameters
frequency_list = config.frequencies
power = config.power_default
pulse_rr = 2
width =100e-3

for frequency in frequency_list:
    # continous wave generation
    freq_query, power_query = SignalGeneration.continous_wave_generation(frequency,power)  # continous signal generation
    print(f"Frequency = {freq_query}, Power ={power_query}")
    
    #Pulse modulation
    pulse_rr_q,width_q,status = PulseModulation.pulse_modulation_internal_on(pulse_rr,width)
    print(f"Pulse repitition rate {pulse_rr_q}")
    print(f"and Pulse width = {width_q}")
    print("Adjust the timescale of the signal to see the pulse modulated signal")
    print("Press enter for next frequency test")
    # input()
  
# disconnect
PulseModulation.pulse_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###