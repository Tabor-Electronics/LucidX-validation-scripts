"""
1) In this script we are using spectrum analyzer as a measuring device
"""
from functions_v1 import Lucid_functions,sweeps
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config

handle = config.handle
power = 5
Lucid_functions.reset(handle)
if config.spectrum:
    spectrum_address = config.spectrum_tcpip # Spectrum analyzer TCPIP  address
    spectrum_analyzer = spectrum_methods.connect_spectrum_via_lan(spectrum_address)
    status_sa = spectrum_methods.reset_and_clear_sa(
        spectrum_analyzer)  # reset and clear the measuring device spectrum analyzer
    if status_sa:
        print("Factory reset done Spectrum Analyzer")
    else:
        print("Error while reseting spectrum analyzer")
    spectrum_methods.set_reference_power(power + 5, spectrum_analyzer)

frsw_start = [500]  # trig_timer
frsw_stop = [1000]  # np.linspace(50e3, 40e9,10)
frsw_step = [3, 12]  # np.linspace(2, 65535,10)
frsw_time = [0.5]  # np.linspace(10e-6, 8976,10)
direction_list = ["UPD"]  # ,"UPD"]
Lucid_functions.send_scpi_command(':POWer {0}'.format(power), handle)
Lucid_functions.send_scpi_command(':OUTPut ON', handle)

for time_cmd in frsw_time:
    for direction in direction_list:
        for start_freq in frsw_start:
            for stop_freq in frsw_stop:
                for steps in frsw_step:
                    Lucid_functions.send_scpi_command(':OUTPut ON', handle)
                    sweeps.frequency_sweep(start_freq,stop_freq,steps,direction,time_cmd)
                    
                    if config.spectrum:
                        list1 = spectrum_methods.get_peak_table(spectrum_analyzer)

                    Lucid_functions.send_scpi_command(':FRSW OFF', handle)
Lucid_functions.send_scpi_command(':OUTPut OFF', handle)
print("test completed")