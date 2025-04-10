print("<DESCRIPTION>Test description :-  Script tests the Internal source frequency for the ref out of the Lucid module</DESCRIPTION>")
###START OF SCRIPT###
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import  config
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

rosc_query = Lucid_functions.send_scpi_query(":ROSC:SOUR?", handle)
print('Rosc source', rosc_query)
for r_freq in [10e6,100e6]:
    Lucid_functions.send_scpi_command(":ROSC:SOUR INT",handle)
    Lucid_functions.send_scpi_command(':ROSC:OUTP:FREQ {0}'.format(r_freq), handle)
    rosc_freq = Lucid_functions.send_scpi_query(":ROSC:OUTP:FREQ?", handle)
    devicePrintCmd.msg_gui.set('Oscillation freq={0}::p0.00::n0.00'.format(rosc_freq))
    devicePrintCmd.Print()
    
    # SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
    if config.spectrum:  # spectrum commands for automation
        cf = r_freq/1e6  # center frequency on measuring device
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)
        freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
        # devicePrintCmd.msg_gui.set('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
        devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out, power_max))
        devicePrintResp.Print()
        
        # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
        error_value = abs(float(freq_out) - r_freq/1e6)  # Calculating difference between input and output frequency
        power_error = abs(float(power_max) - config.power_default)  # Calculating difference between input and output power
        frequency_th = 0.01  # frequency threshold in terms of percentage of input frequency
        power_th = 1  # power threshold in dBm
        # print(error_value < (frequency_th * freq_in)) # check frequency
        # print(power_error < power_th) # check power
        threshold = -60
        if (error_value < (frequency_th * r_freq)) and (power_max > threshold):  # Condition to conclude the test result
            # spectrum_methods.set_span_freq(0.03, spectrum_analyzer)
            # spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)
            # freq_out_r, power_max_r = spectrum_methods.get_right_peak(cf, spectrum_analyzer)
            # fm_freq_response = (freq_out_r - (cf)) * 1e6  # in MHz
            # fm_error = fm_freq_response - (am_freq)
            # if (fm_error < (0.2 * am_freq)) and power_max_r > threshold:
            devicePrintCmd.msg_user.set('Test pass for Reference oscillation frequency of {0} Hz'.format(r_freq))
            devicePrintCmd.Print()
        else:
            devicePrintCmd.msg_user.set('Test Fail for Reference oscillation frequency of {0} Hz'.format(r_freq))
            devicePrintCmd.Print()
    devicePrintCmd.msg_user.set('Press enter for next frequency test')
    devicePrintCmd.Print()
    
    input()
# SECTION 5 - Closing the instruments
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT##