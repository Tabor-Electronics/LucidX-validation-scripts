"""
1) In this script we are using spectrum analyzer as a measuring device
"""
from functions_v1 import Lucid_functions,PulseModulation,SignalGeneration
from spectrum_analyser_functions import spectrum_methods
from SourceFiles import config

handle = config.handle
Lucid_functions.reset(handle)

# continous wave generation
frequency = config.frequency_default
power = 5
SignalGeneration.continous_wave_generation(frequency,power)

# Internal source commands for AM
pulse_frequencies = [10, 100, 1000, 10000, 100000, 1000000]  # 1 to 1E6
# keep the scope time resolution around 50 us/
for pulse_freq in pulse_frequencies:
    pulse_rr_q,width_q,status = PulseModulation.pulse_modulation_internal_on(pulse_freq,322e-9)
    print(f"frequency = {frequency}MHz")
    print(f"Pulse repitition rate {pulse_rr_q}")
    print(f"and Pulse width = {width_q}")
    
    # Lucid_functions.send_scpi_command(':PULS:SOUR INT', handle)
    # Lucid_functions.send_scpi_command(':PULS:INT:FREQ {0}'.format(pulse_freq), handle)
    # Lucid_functions.send_scpi_command(':PULS:WIDT 322e-9', handle)
    # Lucid_functions.send_scpi_command(':PULS ON', handle)
    # error = Lucid_functions.get_lucid_error(handle)
#######################################################
# disconnect
Lucid_functions.send_scpi_command(':PULS OFF', handle)
Lucid_functions.send_scpi_command(':OUTPut OFF', handle)
error = Lucid_functions.get_lucid_error(handle)
print("test completed")