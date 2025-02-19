"""
1) In this script we are using spectrum analyzer as a measuring device
"""
from functions_v1 import Lucid_functions,sweeps
from spectrum_analyser_functions import spectrum_methods
import time
from SourceFiles import config
handle = config.handle
Lucid_functions.reset(handle)
if config.spectrum:
    spectrum_address =config.spectrum  # Spectrum analyzer TCPIP  address
    spectrum_analyzer = spectrum_methods.connect_spectrum_via_lan(spectrum_address)
    status_sa = spectrum_methods.reset_and_clear_sa(spectrum_analyzer)  # reset and clear the measuring device spectrum analyzer
    if status_sa:
        print("Factory reset done Spectrum Analyzer")
    else:
        print("Error while reseting spectrum analyzer")
    spectrum_methods.set_reference_power(config.power_default + 5, spectrum_analyzer)

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
                    sweeps.power_sweep(start_power,stop_power,steps,direction,time_cmd)


Lucid_functions.send_scpi_command(':PRSW OFF', handle)
Lucid_functions.send_scpi_command(':OUTPut OFF', handle)
print("test completed")