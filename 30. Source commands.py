print("<DESCRIPTION>Test name :- Source commands test. \nTest description :-This script tests the commands used to save setup configurations and verifies whether the parameters are correctly retained. No additional connections are required to run this test.")
      ###START OF SCRIPT###
import numpy as np
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config
from SourceFiles.for_the_gui import DevicePrint

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)
#Clear all the setups
no_of_setup = 5
for i in range(5):

    Lucid_functions.send_scpi_command(':SYST:SET:CLEar {0}'.format(i+1), handle)
    error = Lucid_functions.get_lucid_error(handle) #Error SCPI query
    
while "0, no errors" not in error:
    error = Lucid_functions.get_lucid_error(handle)
    print(error)
error = Lucid_functions.get_lucid_error(handle)

devicePrintCmd.msg_user.set('Previous stored setup cleared')
devicePrintCmd.Print()
##parameters
frequency_list = [20e6,3e9,8e8,250e3,123e6]#np.linspace(50e3, 55e3,5)#unit MHz
power_list = np.linspace(-10, 10,5) #unit dBm
print(frequency_list,power_list)
# Set some frequency and power and then store 5 different setup to the internal target
for i in range(no_of_setup):
    Lucid_functions.send_scpi_command(':FREQuency {0}'.format(frequency_list[i]), handle)
    Lucid_functions.send_scpi_command(':POW {0}'.format(power_list[i]), handle)
    # Lucid_functions.send_scpi_command(':OUTPut ON', handle)
    # outp_query = Lucid_functions.send_scpi_query(':OUTP?', handle)
    Lucid_functions.send_scpi_command(':SYST:SET:STOR {0}'.format(i + 1), handle)
    #
    error = Lucid_functions.get_lucid_error(handle)
    # frequency_query = Lucid_functions.send_scpi_query(':FREQuency?', handle)
    # power_query = Lucid_functions.send_scpi_query(':POWer?', handle
    # print("Power level", power_query)
    # print("Frequency in MHz", frequency_query)

#Recall those set up using loop store 5 setup to the internal target
for i in range(no_of_setup):
    Lucid_functions.send_scpi_command(':SYST:SET:REC {0}'.format(i+1), handle)
    frequency_query = Lucid_functions.send_scpi_query(':FREQuency?', handle)
    power_query = Lucid_functions.send_scpi_query(':POWer?', handle)
    freq_err = abs(frequency_list[i] - float(frequency_query))
    power_err = abs(power_list[i] - float(power_query))
    freq_threshold = config.tolerance * frequency_list[i]
    
    pow_th = config.power_tolerance
    if freq_err < freq_threshold:
        # print('fail')
        if (power_err < pow_th):
            devicePrintCmd.msg_user.set('Test pass for Frequency {0} Hz, power {1} dBm'.format(frequency_query,power_query))
            devicePrintCmd.Print()
    else:
        # print(f'Test Fail for Frequency = {freq_in} MHz')
        devicePrintCmd.msg_user.set(f'Test Fail for Frequency ')
        devicePrintCmd.Print()
    if i == no_of_setup - 1:
        devicePrintCmd.msg_user.set('Press enter to finish test')
        devicePrintCmd.Print()
    else:
        devicePrintCmd.msg_user.set('Press enter for next frequency test')
        devicePrintCmd.Print()
    input()
error = Lucid_functions.get_lucid_error(handle)
Lucid_functions.send_scpi_command(':OUTP OFF', handle)
devicePrintCmd.msg_user.set('Test completed ')
devicePrintCmd.Print()
##################End of script#############