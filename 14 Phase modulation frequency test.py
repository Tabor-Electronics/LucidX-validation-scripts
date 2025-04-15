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

devicePrintCmd.msg_user.set('Connection to the spectrum analyzer is required, this test has to be done manual testing method')
devicePrintCmd.Print()

#SECTION 2- Defining parameters and generate signal form LUCIDX
frequency = config.frequency_default
power = config.power_default
pm_freq_list = config.pm_frequencies
deviation = config.pm_deviation_default

# continous wave generation
freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, power)
# devicePrintCmd.msg_gui.set(f'freq={freq_query}::p0.00::n0.00,pow={power_query}::p0.00::n0.00')
devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query,power_query))
devicePrintCmd.Print()

for pm_freq in pm_freq_list:
    pm_freq_q, pm_dev_q, pm_status_q = PhaseModulation.phase_modulation_internal_on(pm_freq, deviation)
    devicePrintCmd.msg_gui.set("PM frequency={0}::p0.00::n0.00,PM deviation={1}::p0.00::n0.00".format(pm_freq_q, pm_dev_q))
    devicePrintCmd.msg_user.set('Check the phase modulated frequency of the signal, Given phase modulation frequency is {0}'.format(pm_freq))
    devicePrintCmd.Print()
    devicePrintCmd.msg_user.set('Press enter for next phase modulation test')
    devicePrintCmd.Print()
    input()

# disconnect instrument
PhaseModulation.phase_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
