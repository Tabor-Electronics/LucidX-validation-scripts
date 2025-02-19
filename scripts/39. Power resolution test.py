
"""
Test description :- This test gives out the value frequency and  power
and compare the given threshold to conclude the result for Accuracy with given frequency
1) In this script we are using spectrum analyzer as a measuring device
"""


###START OF SCRIPT###
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods

import config
from  lucid_cmd import  LucidCmd
#Establishing connection with LUCIDX
handle = 'TCPIP0::{0}::{1}::SOCKET'.format(config.lucid_ip_address,config.port)  #Lucid TCPIP address
Lucid_functions.lsx_connection(handle)
status_lsx = Lucid_functions.reset_and_clear(handle) # reset and clear the lucid x desktop
if status_lsx: # checking the reset status
    print("Factory reset done LSX")
else:
    print("Error while reseting the LucidX module")
#Establishing connection with spectrum analyzer as a measuring device
spectrum = True #NOTE- Please keep it false if spectrum analyzer is not connected to same LAN network and run the script on debug mode
if spectrum:
    spectrum_address = 'TCPIP::192.90.70.36::5025::SOCKET' # Spectrum analyzer TCPIP  address
    spectrum_analyzer = spectrum_methods.connect_spectrum_via_lan(spectrum_address)
    status_sa = spectrum_methods.reset_and_clear_sa(spectrum_analyzer) # reset and clear the measuring device spectrum analyzer
    if status_sa: # checking the reset status
        print("Factory reset done Spectrum Analyzer")
    else:
        print("Error while reseting spectrum aanlyzer")



# continous wave generation
frequency = 2e3 # frequency in MHz
x= 5
resolution =0.01
power_list= [x, x+resolution, x-resolution]

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
    if spectrum:  # spectrum commands for automation
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
###END OF SCRIPT###

