
"""
Test description :- This test gives out the value frequency and  power
and compare the given threshold to conclude the result for Accuracy with given frequency
1) In this script we are using spectrum analyzer as a measuring device
"""


###START OF SCRIPT###

from SourceFiles.functions_v1 import Lucid_functions
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.lucid_cmd import  LucidCmd

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)
if config.spectrum:
    device_address = 'TCPIP::{0}::{1}::SOCKET'.format(config.spectrum_ip_address_india, config.port)  # Spectrum analyzer TCPIP  address
    spectrum_analyzer,status = spectrum_methods.reset(device_address)
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)  # step 1) set reference power level on spectrum
    spectrum_methods.set_span_freq(200,spectrum_analyzer)




# continous wave generation
frequency = 2e3 # frequency in MHz
power_list= [-70,-65,-58,-43,-39,-18,-5,0,1,2,3,4,5,6,7,8,9,10,12,15,18,20]

for power in power_list:
    Lucid_functions.send_scpi_command(':FREQuency {0}e6'.format(frequency), handle) # SCPI command for frequency
    Lucid_functions.send_scpi_command(':POWer {0}'.format(power), handle) # SCPI command for power
    freq_query = Lucid_functions.send_scpi_query(':FREQuency?', handle) # SCPI query to frequency
    power_query = Lucid_functions.send_scpi_query(':POWer?', handle) # SCPI query to power
    Lucid_functions.send_scpi_command(':OUTPut ON', handle) #Channel OUTPUT ON scpi command
    outp_query = Lucid_functions.send_scpi_query(LucidCmd.OUTP_Q, handle) #Channel OUTPUT ON scpi query
    error = Lucid_functions.get_lucid_error(handle) #Error SCPI query


    # Internal source commands for AM
    cf = frequency#center frequency on measuring device in MHz
    span_freq = 500 # span on measuring device in MHz
    if config.spectrum:  # spectrum commands for automation
        spectrum_methods.set_reference_power(power + 5, spectrum_analyzer)#  step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(span_freq, spectrum_analyzer)# step 2) set span frequency on spectrum
        spectrum_methods.get_centre_frequency(cf, spectrum_analyzer)# step 3) set center frequency on spectrum
        spectrum_methods.set_marker_at_peak(spectrum_analyzer)# step 4)  add a marker and set it to peak

        spectrum_methods.marker_to_center_frequency(spectrum_analyzer) #step 5) move marker to center frequency
        freq_out,power_max = spectrum_methods.set_marker(spectrum_analyzer)  # step 6) Read marker x (frequency) and y (power)

        error_value = abs(float(freq_out) - cf)  # Calculating difference between input and output frequency
        power_error = abs(float(power_max) - power)  # Calculating difference between input and output power
        frequency_th = 0.1  # frequency threshold in term of percentage of input frequency
        power_th = 1  # power threshold in dBm
        if (error_value < (frequency_th * cf)) and (power_error < power_th):  # Condition to conclude the test result
            print("Test pass for Frequency = {0} MHz".format(cf))
        else:
            print("Test fail  for Frequency = {0} MHz".format(cf))


Lucid_functions.disconnect_lucid(config.handle)# disconnect instrument
###END OF SCRIPT###x

