print("<DESCRIPTION> Test description :- This script generates signal with different frequency to test the Phase noise on each frequency, please check the parameter for error limit to compare the given threshold and conclude the result for  given frequency\n1) This script has to be tested  using SSA manually.\n2) Need to test  Phase noise for different frequencies according to the frequency_list\n3)You may change or modify the variable as required </DESCRIPTION>")
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd
from SourceFiles.for_the_gui import DevicePrint

# SECTION 1- Connect LUCIDX, create object of Device print, connect to measuring device
handle = config.handle
Lucid_functions.reset(handle)  # Establishing connection with LUCIDX

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

devicePrintCmd.msg_user.set('Connection to SSA is required, this test has to be done manual testing method')#SSA = signal source analyzer
devicePrintCmd.Print()
frequency_list = [100e6, 250e6, 500e6, 1000e6, 2000e6, 4000e6, 8000e6, 10000e6, 20000e6,40000e6]  # List of frequency to be tested for phase noise.
power = config.power_default  # Power level applied to LucidX
error_limit = [-155, -147, -141, -134, -128, -123, -116, -115, -109, -103]  # Error limit for phase noise
for i in range(len(frequency_list)):
    freq_in = frequency_list[i]
    freq_query, power_query = SignalGeneration.continous_wave_generation(freq_in, power)  # continous signal generation
    devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query, power_query))
    devicePrintCmd.Print()
    devicePrintCmd.msg_user.set('Check the phase noise of the signal,  test fails if its below {0} dBC'.format(error_limit[i]))
    devicePrintCmd.Print()
    devicePrintCmd.msg_user.set('Press enter for next frequency test')
    devicePrintCmd.Print()
    input()
    
# SECTION 5 - Closing the instruments
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###


