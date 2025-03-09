print("<DESCRIPTION> Test description :- This test gives out the value frequency and  power and tests for the harmonics and Verify the power at Harmonic frequency\nSteps:- \n1) In this script we are using spectrum analyzer as a measuring device.\n2) We will set a center  frequency first, verify the power \n3) Move to harmonic frequency and get the power of it\n4) Set span to verify the signal frequency</DESCRIPTION>")
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
# Global Parameters
frequency_list =config.frequencies#(np.arange(10,1000,100))+list(np.arange(1100,8000,1000))+list(np.arange(8100,12000,1000)) #+list(np.arange(20000,40000,100)
power_list= [-15,0,15]
for freq_in in frequency_list:
    for power_in_dBm in power_list:
        freq_query, power_query = SignalGeneration.continous_wave_generation(freq_in,power_in_dBm) # continous signal generation
        devicePrintCmd.msg_gui.set(f'freq={freq_query}::p0.00::n0.00,pow={power_query}::p0.00::n0.00')
        devicePrintCmd.Print()
        
        # SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
        if config.spectrum:  # spectrum commands for automation
            cf = freq_in # center frequency on measuring device
            spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
            freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
            # print(freq_out,power_max)
            
            # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
            error_value = abs(float(freq_out) - freq_in)  # Calculating difference between input and output frequency
            power_error = abs(float(power_max) - float(power_in_dBm)) # Calculating difference between input and output power
            frequency_th = 0.1 # frequency threshold in terms of percentage of input frequency
            power_th = 1  # power threshold in dBm
            # a=error_value < (frequency_th * freq_in)
            # b=power_error < power_th
            # print(a,b)
            
            if (error_value < (frequency_th * freq_in)) and (power_error < power_th):  # Condition to conclude the test result
                second_freq = 2 * cf
                spectrum_methods.set_centre_frequency(second_freq, spectrum_analyzer)  # set center frequency on spectrum
                # spectrum_methods.set_start_freq(cf/10,spectrum_analyzer)
                spectrum_methods.set_span_freq(cf*20,spectrum_analyzer)
                freq_out2, power_max2 = spectrum_methods.get_cf_marker(second_freq,spectrum_analyzer) # Read marker x (frequency) and y (power)
                devicePrintResp.msg_gui.set(f'freq={freq_out2}::p0.00::n0.00,pow={power_max2}::p0.00::n0.00')
                devicePrintResp.Print()
                
                threshold = -40 + power_in_dBm
                print(power_max2<threshold)
                if power_max2<threshold:
                    devicePrintCmd.msg_user.set(f'Test pass for Frequency = {freq_in} MHz')
                    devicePrintCmd.Print()
                else:
                    devicePrintCmd.msg_user.set(f'Test Fail for Frequency = {freq_in} MHz')
                    devicePrintCmd.Print()
            else:
                # print(f'Test Fail for Frequency = {freq_in} MHz')
                devicePrintCmd.msg_user.set(f'Test Fail for Frequency = {freq_in} MHz')
                devicePrintCmd.Print()
        
        devicePrintCmd.msg_user.set('Press enter for next Harmonic frequency test')
        devicePrintCmd.Print()
        input()
    
    # SECTION 5 - Closing the instruments
    Lucid_functions.disconnect_lucid(config.handle)
    ###END OF SCRIPT###
