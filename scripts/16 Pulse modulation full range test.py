print("Test description :- This script will generate a signal with pulse modulation for different carrier frequencies")
print("An oscilloscope is a better way to see the output of pulse modulation (make sure it supports higher frequency range)")
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles import config
# from SourceFiles.oscilloscope_functions import scope_methods
from SourceFiles.oscilloscope_functions import FetchResults
from SourceFiles.for_the_gui import DevicePrint

# SECTION 1- Connect LUCIDX, create object of Device print, connect to measuring device
handle = config.handle

Lucid_functions.reset(handle)  # Establishing connection with LUCIDX

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

devicePrintCmd.msg_user.set('Connecting to the Oscilloscope')
devicePrintCmd.Print()

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