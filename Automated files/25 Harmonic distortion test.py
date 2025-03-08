print('<DESCRIPTION> This script generates a waveform with certain  frequency and  power,\nUser needs to test the harmonic frequencies of the signal and note down the power of the signal based on the given frequency and power </DESCRIPTION>')
###START OF SCRIPT###
import numpy as np
import time
from functions_v1 import Lucid_functions,SignalGeneration
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config

#Establishing connection with LUCIDX
handle = config.handle #Lucid TCPIP address
#Establishing connection with LUCIDX
Lucid_functions.reset(config.handle)


print("Start spectrum analyzer")

# Input Parameters (madify this for 40G accordingly)
frequency_list =config.frequencies#(np.arange(10,1000,100))+list(np.arange(1100,8000,1000))+list(np.arange(8100,12000,1000)) #+list(np.arange(20000,40000,100)
power_list= [-15,0,15]


for i in range(len(frequency_list)):
    center_frequency = frequency_list[i]
    for power_in_dBm in power_list:
        SignalGeneration.continous_wave_generation(center_frequency,power_in_dBm)
        print(f'Frequency = {center_frequency}MHz, Power = {power_in_dBm}dBm')
        print("Press enter for next frequency test")
        input()
#
