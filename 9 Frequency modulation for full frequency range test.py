print("<DESCRIPTION>Test description :-  This test run for Frequency modulation of a given different carrier signal, baseband frequency and deviation</DESCRIPTION>")
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration, FrequencyModulation
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
frequency_list = config.frequencies  # list of frequencies for testing
power = config.power_default  # power in dBm
fm_freq = config.fm_freq_default
deviation = config.fm_deviation_default


freq_query,power_query = SignalGeneration.continous_wave_generation(1000, 5)#initiating waveform
# Internal source commands for FM
fm_source_q,fm_freq_q,fm_dev_q,fm_status_q = FrequencyModulation.frequency_modulation_internal_on(fm_freq, deviation)
devicePrintCmd.msg_gui.set('FM Frequency={0}::p0.00::n0.00,Deviation={1}::p0.00::n0.00'.format(fm_freq_q, fm_dev_q))
devicePrintCmd.Print()

for freq_in in frequency_list:
    # continous wave generation
    freq_query,power_query = SignalGeneration.continous_wave_generation(freq_in, power)
    devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query, power_query))
    devicePrintCmd.Print()
    
# SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
    if config.spectrum:  # spectrum commands for automation
        cf = freq_in  # center frequency on measuring device
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
        
        freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
        # devicePrintCmd.msg_gui.set('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
        devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out, power_max))
        devicePrintResp.Print()
        
        # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
        error_value = abs(float(freq_out) - freq_in)  # Calculating difference between input and output frequency
        power_error = abs(float(power_max) - config.power_default)  # Calculating difference between input and output power
        frequency_th = 0.1  # frequency threshold in terms of percentage of input frequency
        power_th = 1  # power threshold in dBm
        # print(error_value < (frequency_th * freq_in)) # check frequency
        # print(power_error < power_th) # check power
        threshold = -60
        if (error_value<(frequency_th*freq_in)) and (power_max>threshold):  # Condition to conclude the test result
            spectrum_methods.set_span_freq(0.3, spectrum_analyzer)
            spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)
            freq_out_r, power_max_r = spectrum_methods.get_right_peak(cf,spectrum_analyzer)
            fm_freq_response = (freq_out_r- (cf))*1e6 #in MHz
            fm_error=fm_freq_response-(fm_freq)
            if(fm_error<(0.2*fm_freq)) and power_max_r>threshold:
                devicePrintCmd.msg_user.set('Test pass for Frequency = {0} Hz at Carrier frequency of {1} MHz'.format(fm_freq,freq_in))
                devicePrintCmd.Print()
            else:
                devicePrintCmd.msg_user.set('Test Fail for FM Frequency = {0} Hz at Carrier frequency of {1} MHz'.format(fm_freq,freq_in))
                devicePrintCmd.Print()
        else:
            devicePrintCmd.msg_user.set('Test Fail for Frequency = {0} MHz'.format(freq_in))
            devicePrintCmd.Print()
            
    devicePrintCmd.msg_user.set('Press enter for next frequency test')
    devicePrintCmd.Print()
    
    input()
# SECTION 5 - Closing the instruments
FrequencyModulation.frequency_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###