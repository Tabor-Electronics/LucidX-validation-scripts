print("<DESCRIPTION> Test description :- This script will generate a sweep of different power levels </DESCRIPTION>")
#print("There are variable parameters defined in the form of list such as, start,stop,step, delay and direction. You can make them user input value to make the test more flexible.")

###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from functions_v1 import Lucid_functions,sweeps
from spectrum_analyser_functions import spectrum_methods
import time
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
        spectrum_methods.set_reference_power(config.power_default + 10,spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_centre_frequency(1000, spectrum_analyzer)
        spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz

# SECTION 2- Defining parameters and generate signal form LUCIDX
# Parameters for power sweep
prsw_start = [-10]  # np.linspace(-100, 20,10)
prsw_stop = [10]  # np.linspace(-100, 20,10)
prsw_step = [5]  # np.linspace(2,16777215,10)
prsw_time = [10, 1, 0.5, 0.2, 2]  # np.linspace(100e-6, 8976,10)
direction_list = ["UPD"]  # ["NORM","UPD"]

for time_cmd in prsw_time:
    for direction in direction_list:
        for start_power in prsw_start:
            for stop_power in prsw_stop:
                
                for steps in prsw_step:
                    start_power_query,stop_power_query,step_query,time_query,direction_query = sweeps.power_sweep(start_power,stop_power,steps,direction,time_cmd)
                    devicePrintCmd.msg_gui.set('start power={0}::p0.00::n0.00,stop power={1}::p0.00::n0.00,step={2}::p0.00::n0.00,time={3}::p0.00::n0.00,direction={4}::p0.00::n0.00'.format(start_power_query,start_power_query,step_query,time_query,direction_query))
                    devicePrintCmd.Print()
                    
                    # SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
                    if config.spectrum:
                        freq_in = 1000
                        cf =freq_in # freq_in  # center frequency on measuring device
                        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
                        spectrum_methods.set_reference_power(stop_power+5,spectrum_analyzer)
                        step_size = (stop_power - start_power) / (steps - 1)
                        power_list = [stop_power - i * step_size for i in range(steps)]
                        n = len(power_list)
                        spectrum_methods.set_span_freq(0,spectrum_analyzer)
                        sweep_time = 7*time_cmd
                        spectrum_methods.set_sweep_time(sweep_time, spectrum_analyzer)
                        time.sleep(sweep_time)
                        time_out, power_max = spectrum_methods.set_marker_t(spectrum_analyzer)  # Read marker x (frequency) and y (power)
                        power_list_sa = [power_max]
                        # power_list_sa.append(power_max)
                        for i in range(n-1):
                            target_time = time_out - (time_cmd)
                            time_out, power_max = spectrum_methods.get_time_at_marker(target_time,spectrum_analyzer) # Read marker x (time) and y (power)
                            power_list_sa.append(power_max)
                        print(power_list,power_list_sa)
                        for i in range(n):
                    #     # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
                            power_error = abs(power_list_sa[i]-power_list[i])   # Calculating difference between input and output power
                            power_th = 2  # power threshold in dBm
                            if (power_error < power_th):  # Condition to conclude the test result
                                devicePrintCmd.msg_user.set('Test pass for Power = {0}'.format(power_list[i]))
                                devicePrintCmd.Print()
                            else:
                                devicePrintCmd.msg_user.set('Test Fail for Power = {0}'.format(power_list[i]))
                                devicePrintCmd.Print()
    devicePrintCmd.msg_user.set('Test done for sweep time {0} s'.format(time_cmd))
    devicePrintCmd.Print()
    devicePrintCmd.msg_user.set('Press enter for next frequency test')
    devicePrintCmd.Print()
    input()

# disconnect instrument
Lucid_functions.send_scpi_command(':PRSW OFF', handle)
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###