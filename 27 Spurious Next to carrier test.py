print("<DESCRIPTION> Test description- This test verifies, there is no spurious present near the carrier frequency (between start and stop frequency ie span ) of the carrier above the defined error limit ie -60dB</DESCRIPTION>")
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
import time
import numpy as np
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration
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

power_in_dBm = 5# power level required for the test in dBm

# commands for spectrum analyzer
if config.spectrum:
    spectrum_analyzer, status = spectrum_methods.reset(config)
    if status:
        spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz
        threshold = -60 + power_in_dBm
        spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)
        spectrum_methods.set_resolution_bandwidth(100000, spectrum_analyzer)

####################################################################
# Input Parameters
frequency_list =list(np.arange(20,110,10))#+list(np.arange(150,1000,50)))+list(np.arange(1000,3000,500))#list(np.arange(1000,12000,1000))#+list(np.arange(150,1050,50))+list(np.arange(1250,12250,250)) # list of frequencies to be tested
frequnecy_list = config.frequencies

for freq_in in frequency_list: # iterating over each frequency (main loop)
    # continous wave generation
    freq_query, power_query = SignalGeneration.continous_wave_generation(freq_in,power_in_dBm)  # continous signal generation
    devicePrintCmd.msg_gui.set(f'freq={freq_query}::p0.00::n0.00,pow={power_query}::p0.00::n0.00')
    devicePrintCmd.Print()
    
    # SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
    if config.spectrum:  # spectrum commands for automation
        cf = freq_in  # center frequency on measuring device
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
        freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
        # print(freq_out,power_max)
        # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
        error_value = abs(float(freq_out) - freq_in)  # Calculating difference between input and output frequency
        power_error = abs(float(power_max) - float(power_in_dBm))  # Calculating difference between input and output power
        frequency_th = 0.1  # frequency threshold in terms of percentage of input frequency
        power_th = 4  # power threshold in dBm
        a=error_value < (frequency_th * freq_in)
        b=power_error < power_th
        print(a,b)
        if (error_value < (frequency_th * freq_in)) and (power_error < power_th):
            if cf <= 20 or cf <= 100:
                step_size = 10
                span_sa = 20
            elif cf <= 150 or cf <= 1000:
                step_size = 50
                span_sa = 30
            elif cf <= 1250 or cf <= 12000:
                step_size = 50
                span_sa = 40
            else:
                continue
            spectrum_methods.set_span_freq(span_sa, spectrum_analyzer)  # step 2) set span to 200MHz
          
            freq_left, power_left = spectrum_methods.get_left_peak(cf, spectrum_analyzer)
            devicePrintResp.msg_gui.set(f'freq={freq_left}::p0.00::n0.00,pow={power_left}::p0.00::n0.00')
            devicePrintResp.Print()
            freq_right, power_right = spectrum_methods.get_right_peak(cf, spectrum_analyzer)
            devicePrintResp.msg_gui.set(f'freq={freq_right}::p0.00::n0.00,pow={power_right}::p0.00::n0.00')
            devicePrintResp.Print()
            if freq_left == freq_right:
                devicePrintCmd.msg_user.set(f'Spurious test pass for Frequency = {freq_in} MHz')
                devicePrintCmd.Print()
            else:
                devicePrintCmd.msg_user.set(f'Spurious test Fail for Frequency = {freq_in} MHz')
                devicePrintCmd.Print()
        else:
            devicePrintCmd.msg_user.set(f'Test Fail for Frequency = {freq_out} MHz with power ={power_max}')
            devicePrintCmd.Print()
        
        devicePrintCmd.msg_user.set('Press enter to test the spurious for next frequency')
        devicePrintCmd.Print()
        input()
        
# SECTION 5 - Closing the instruments
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###

