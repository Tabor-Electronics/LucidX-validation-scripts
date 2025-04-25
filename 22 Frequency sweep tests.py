print("<DESCRIPTION> Test description :- This script will generate a sweep of freuencies </DESCRIPTION>")
# print("There are variable parameters defined in the form of list such as, start,stop,step, delay and direction. You can make them user input value to make the test more flexible.")

###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from functions_v1 import Lucid_functions,sweeps
from spectrum_analyser_functions import spectrum_methods
import time
import numpy as np
from SourceFiles import config
from SourceFiles.for_the_gui import DevicePrint

# SECTION 1- Connect LUCIDX, create object of Device print, connect to measuring device
handle = config.handle
Lucid_functions.reset(handle)  # Establishing connection with LUCIDX

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

devicePrintCmd.msg_user.set('Connecting to the spectrum analyzer')
devicePrintCmd.Print()

if config.spectrum: # commands for spectrum analyzer
    spectrum_analyzer, status = spectrum_methods.reset(config)
    if status:
        spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
        
# SECTION 2- Defining parameters and generate signal form LUCIDX
# Global Parameters
frsw_start = [500]
frsw_stop = [1000]
frsw_step = [3, 12]
frsw_time = [0.5]
direction_list = ["UPD"]

for time_cmd in frsw_time:
    for direction in direction_list:
        for start_freq in frsw_start:
            for stop_freq in frsw_stop:
                for steps in frsw_step:
                    start_freq_query,stop_freq_query,step_query,time_query,direction_query =sweeps.frequency_sweep(start_freq,stop_freq,steps,direction,time_cmd)
                    devicePrintCmd.msg_gui.set('frequency power={0}::p0.00::n0.00,stop power={1}::p0.00::n0.00,step={2}::p0.00::n0.00,time={3}::p0.00::n0.00,direction={4}::p0.00::n0.00'.format(start_freq_query, start_freq_query, step_query, time_query, direction_query))
                    devicePrintCmd.Print()
                    
                    # SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
                    if config.spectrum:
                        threshold = config.power_default -15
                        # spectrum_methods.set_start_freq(start_freq_sa,spectrum_analyzer)
                        # spectrum_methods.set_start_freq(stop_freq_sa, spectrum_analyzer)
                        # spectrum_methods.sweep_test_frequency(spectrum_analyzer)
                        # frequencies,power = spectrum_methods.sweep_test_sa(start_freq_sa,stop_freq_sa,steps,threshold,spectrum_analyzer)
                        # print(frequencies,power)
                        # freq_val = list(np.linspace(start_freq,stop_freq,steps))
                        # for i in range(len(frequencies)):
                        #     freq_error = abs(frequencies[i] - freq_val[i])
                        #     fr_th = 0.1*freq_val[i]
                        #     power_error = abs(power[i]-config.power_default)
                        #     pr_th = 1
                        #     if freq_error < fr_th and power_error < pr_th :
                        #         devicePrintCmd.msg_user.set('Test pass for Reference oscillation frequency of {0} Hz'.format(rosc_freq))
                        #         devicePrintCmd.Print()
                        #     else:
                        #         devicePrintCmd.msg_user.set('Test Fail for Reference oscillation frequency of {0} Hz'.format(rosc_freq))
                        #         devicePrintCmd.Print()
                        # start_freq = 1000
                        # stop_freq = 2000
                        # steps = 5
                        if config.spectrum:
                            spectrum_analyzer, status = spectrum_methods.reset(config)
                            spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
                            start_freq_sa = start_freq - (0.5 * start_freq)
                            stop_freq_sa = stop_freq + (0.5 * start_freq)
                            threshold = config.power_default - 15
                            frequencies, power = spectrum_methods.sweep_test_sa(start_freq_sa, stop_freq_sa, steps,threshold, spectrum_analyzer)
                            print(frequencies, power)
                            freq_val = list(np.linspace(start_freq, stop_freq, steps))
                            for i in range(len(frequencies)):
                                freq_error = abs(frequencies[i] - freq_val[i])
                                fr_th = 0.1 * freq_val[i]
                                power_error = abs(power[i] - config.power_default)
                                pr_th = 1
                                # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
                                if freq_error < fr_th and power_error < pr_th:
                                    devicePrintCmd.msg_user.set('Test pass for frequency of {0} Hz'.format(freq_val[i]))
                                    devicePrintCmd.Print()
                                else:
                                    devicePrintCmd.msg_user.set('Test fail for frequency of {0} Hz'.format(freq_val[i]))
                                    devicePrintCmd.Print()
                                devicePrintCmd.msg_user.set('Press enter for next frequency test')
                                devicePrintCmd.Print()
                                input()
                                # disconnect instrument
                                Lucid_functions.send_scpi_command(':FRSW OFF', handle)
                                # SECTION 5 - Closing the instruments
                                Lucid_functions.disconnect_lucid(config.handle)
                                ###END OF SCRIPT###