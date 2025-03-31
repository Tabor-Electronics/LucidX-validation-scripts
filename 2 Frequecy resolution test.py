print("<DESCRIPTION> Test description :- This test gives out the value frequency and  power and compare the given threshold to conclude the result for resolution of frequency with given frequency\nSteps:- \n1) In this script we are using spectrum analyzer as a measuring device.\n2) We will set a center  frequency and  span to verify the signal frequency</DESCRIPTION>")
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
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
# commands for spectrum analyzer
if config.spectrum:
    spectrum_analyzer, status = spectrum_methods.reset(config)
    if status:
        spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz

# SECTION 2- Defining parameters and generate signal form LUCIDX
        
#Global Parameters
x=config.frequency_default # frequency to be tetsted
resolution =config.frequency_resolution # frequency resolution
frequencies = [x, x+resolution, x-resolution]
power = config.power_default

for frequency in frequencies:
    # continous wave generation
    freq_query,power_query = SignalGeneration.continous_wave_generation(frequency, power)
    devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query, power_query))
    devicePrintCmd.Print()

        # BW = 15
        # spectrum_methods.set_centre_frequency(cf, spectrum_analyzer) # step 2) set center frequency on spectrum
        # spectrum_methods.set_marker_at_peak(spectrum_analyzer)# step 3)  add a marker and set it to peak
        # spectrum_methods.marker_to_center_frequency(spectrum_analyzer)  #step 4) move marker to center frequency
        # freq_out,power_max = spectrum_methods.set_marker(spectrum_analyzer) # step 5) Read marker x (frequency) and y (power)
        # error_value=abs(float(freq_out) - cf)  # Calculating difference between input and output frequency
        # power_error = abs(float(power_max)-power)  # Calculating difference between input and output power
        # frequency_th = 0.1 #  frequency threshold in term of percentage of input frequency
        # power_th = 1  #  power threshold in dBm
        # if (error_value <( frequency_th*cf)) and (power_error <1): # Condition to conclude the test result



# SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
    if config.spectrum:  # spectrum commands for automation
        cf = frequency  # center frequency on measuring device
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
        freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
        
        # devicePrintCmd.msg_gui.set('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
        devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out, power_max))
        devicePrintResp.Print()
        
        # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
        error_value = abs(float(freq_out) - cf)  # Calculating difference between input and output frequency
        power_error = abs(float(power_max) - config.power_default)  # Calculating difference between input and output power
        frequency_th = 0.1  # frequency threshold in terms of percentage of input frequency
        power_th = 1  # power threshold in dBm
        # if (error_value < (frequency_th * freq_in)) and (power_error < power_th):  # Condition to conclude the test result
        if (error_value < (frequency_th * cf)) and (power_error <1):
            # print(f'Test pass for Frequency = {freq_in} MHz')
            devicePrintCmd.msg_user.set(f'Test pass for Frequency = {cf} MHz')
            devicePrintCmd.Print()
        else:
            # print(f'Test Fail for Frequency = {freq_in} MHz')
            devicePrintCmd.msg_user.set(f'Test Fail for Frequency = {cf} MHz')
            devicePrintCmd.Print()
    
    devicePrintCmd.msg_user.set('Press enter for next frequency test')
    devicePrintCmd.Print()
    input()
    
# SECTION 5 - Closing the instruments
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###`