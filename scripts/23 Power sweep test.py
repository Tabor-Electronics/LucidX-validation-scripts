print("Test description :- This script will generate a sweep of freuencies ")
print("There are variable parameters defined in the form of list such as, start,stop,step, delay and direction. You can make them user input value to make the test more flexible.")

from functions_v1 import Lucid_functions,sweeps
from spectrum_analyser_functions import spectrum_methods
import time
from SourceFiles import config
handle = config.handle
Lucid_functions.reset(handle)

print("Start spectrum analyzer")

# commands for spectrum analyzer
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
                    start_power_query,stop_power_query,step_query,time_query,direction_query = sweeps.power_sweep(start_power,stop_power,steps,direction,time_cmd)
                    print(f'Start power = {start_power_query}, Stop power ={stop_power_query}, steps= {step_query}, time delay= {time_query}, direction= {direction_query}')
                    print("Look for power sweep on the measuring device")
                    print("Press input to stop the Sweep")
                    input()

# disconnect instrument
Lucid_functions.send_scpi_command(':PRSW OFF', handle)
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###
