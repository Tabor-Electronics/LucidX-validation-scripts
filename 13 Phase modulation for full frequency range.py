print("<DESCRIPTION>Test description :-  This test run for Phase modulation of a given different carrier signal , baseband frequnecy and deviation</DESCRIPTION>")
# print("The resultant signal can be seen on spectrum analyzer ")

# NOT SURE HOW TO TEST!
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration,PhaseModulation
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

#SECTION 2- Defining parameters and generate signal form LUCIDX
#Global parameters
frequency = config.frequencies
power = config.power_default
pm_freq = config.pm_freq_default
deviation = config.pm_deviation_default
internal_source = config.frequencies

for frequency in frequency:
    # continous wave generation
    # continous wave generation
    freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, power)
    # devicePrintCmd.msg_gui.set(f'freq={freq_query}::p0.00::n0.00,pow={power_query}::p0.00::n0.00')
    devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query, power_query))
    devicePrintCmd.Print()
    
    pm_freq_q, pm_dev_q, pm_status_q = PhaseModulation.phase_modulation_internal_on(pm_freq, deviation)
    print("PM Frequency = {0}, Deviation={1}".format(pm_freq_q,pm_dev_q))
    print("Press enter for next frequency test")
    input()

# disconnect
PhaseModulation.phase_modulation_off()