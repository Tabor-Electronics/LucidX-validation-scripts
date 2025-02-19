"""
Test description :- This script generates signal with different frequency to test the Phase noise on each frequency,
 please check the parameter for error limit to compare the given threshold and conclude the result for  given frequency
1) This script has to be tested  using SSA manually.
2) Need to test  Phase noise for different frequencies according to the frequency_list
3)You may change or modify the variable as required.
"""
###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)
frequency_list = [100e6, 250e6, 500e6, 1000e6, 2000e6, 4000e6, 8000e6, 10000e6, 20000e6,40000e6]  # List of frequency to be tested for phase noise.
power = config.power_default  # Power level applied to LucidX
error_limit = [-155, -147, -141, -134, -128, -123, -116, -115, -109, -103]  # Error limit for phase noise
for frequency in frequency_list:
    print(f"Frequency = {frequency}")
    SignalGeneration.continous_wave_generation(frequency, power) # continous signal generation
Lucid_functions.disconnect_lucid(handle)# disconnect instrument
###END OF SCRIPT###