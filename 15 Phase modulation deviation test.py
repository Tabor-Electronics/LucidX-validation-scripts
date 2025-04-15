print("<DESCRIPTION>Test description :-  This test run for Phase modulation of a given carrier signal , baseband frequnecy and  different  deviation</DESCRIPTION>")
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

devicePrintCmd.msg_user.set('Connection to the spectrum analyzer is required, this test has to be done manual testing method')
devicePrintCmd.Print()

#SECTION 2- Defining parameters and generate signal form LUCIDX
#Global parameters
frequency = config.frequency_default
power = config.power_default
pm_freq= config.pm_freq_default
deviation_list = config.pm_deviation_list
# continous wave generation
freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, power)
devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query, power_query))
devicePrintCmd.Print()

for deviation in deviation_list:
    pm_freq_q, pm_dev_q, pm_status_q = PhaseModulation.phase_modulation_internal_on(pm_freq, deviation)
    devicePrintCmd.msg_gui.set("PM frequency={0}::p0.00::n0.00,PM deviation={1}::p0.00::n0.00".format(pm_freq_q, pm_dev_q))
    devicePrintCmd.msg_user.set('Check the phase modulated frequency of the signal, Given phase modulation deviation is {0}'.format(deviation))
    devicePrintCmd.Print()
    devicePrintCmd.msg_user.set('Press enter for next frequency test')
    devicePrintCmd.Print()
    input()
    
# disconnect
PhaseModulation.phase_modulation_off()
