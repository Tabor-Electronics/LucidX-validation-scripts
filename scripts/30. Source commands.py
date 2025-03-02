###START OF SCRIPT###
import numpy as np
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)
#Clear all the setups
no_of_setup = 5
for i in range(5):

    Lucid_functions.send_scpi_command(':SYST:SET:CLEar {0}'.format(i+1), handle)

    error = Lucid_functions.get_lucid_error(handle) #Error SCPI query
while "0, no errors" not in error:
    error = Lucid_functions.get_lucid_error(handle)
    print(error)
error = Lucid_functions.get_lucid_error(handle)

print("Previous stored setup cleared")

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
    # error = Lucid_functions.get_lucid_error(handle)
    # frequency_query = Lucid_functions.send_scpi_query(':FREQuency?', handle)
    # power_query = Lucid_functions.send_scpi_query(':POWer?', handle)
    # print("Power level", power_query)
    # print("Frequency in MHz", frequency_query)

#Recall those set up using loop store 5 setup to the internal target
for i in range(no_of_setup):
    Lucid_functions.send_scpi_command(':SYST:SET:REC {0}'.format(i+1), handle)
    frequency_query = Lucid_functions.send_scpi_query(':FREQuency?', handle)
    power_query = Lucid_functions.send_scpi_query(':POWer?', handle)

    print(frequency_query)
    print(power_query)
error = Lucid_functions.get_lucid_error(handle)
Lucid_functions.send_scpi_command(':OUTP OFF', handle)
##################End of script#############