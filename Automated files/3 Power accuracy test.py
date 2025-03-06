print("<DESCRIPTION>Test description :- This test gives out the value frequency and  power and compare the given threshold to conclude the result for accuracy of power  given frequency\nSteps:- \n1) In this script we are using spectrum analyzer as a measuring device.\n2) We will set a center  frequency and  span to verify the signal power in dBm</DESCRIPTION>")
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
        spectrum_methods.set_reference_power(config.power_default + 5,
                                             spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz

#SECTION 2- Defining parameters and generate signal form LUCIDX
frequency = config.frequency_default  # frequency in MHz
power = config.power_list  # list of power for testing

for powe in config.power_list:
    # continous wave generation
    freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, powe)  # continous signal generation
    # print(f"Frequency = {freq_query}, Power ={power_query}")
    devicePrintCmd.msg_gui.set(f'freq={freq_query}::p0.00::n0.00,pow={power_query}::p0.00::n0.00')
    devicePrintCmd.Print()
    
    #SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
    if config.spectrum:  # spectrum commands for automation
        cf = frequency  # center frequency on measuring device
        spectrum_methods.set_reference_power(powe + 5, spectrum_analyzer)
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
        freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
        
        #SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 1  dBm power  (TBC in datasheets)
        error_value = abs(float(freq_out) - cf)  # Calculating difference between input and output frequency
        power_error = abs(float(power_max) - float(powe))# Calculating difference between input and output power
        frequency_th = 0.1  # frequency threshold in terms of percentage of input frequency
        power_th = 1  # power threshold in dBm
        if (error_value < (frequency_th * cf)) and (abs(power_error) < power_th):  # Condition to conclude the test result
            devicePrintCmd.msg_user.set('Test pass for power level {0} dBm'.format(powe))
            devicePrintCmd.Print()
        else:
            print('Test Fail for power level {0} dBm'.format(powe))
            devicePrintCmd.msg_user.set('Test Fail for power level {0} dBm'.format(powe))
            devicePrintCmd.Print()

        devicePrintCmd.msg_user.set('Press enter for next power level test')
        devicePrintCmd.Print()
        input()

# SECTION 5 - Closing the instruments
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
