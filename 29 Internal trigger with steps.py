print(
	"<DESCRIPTION> Test description - This script performs amplitude modulation on a signal and waits for a trigger event detected by an oscilloscope."
	"\nSteps:\n1) The spectrum analyzer is used as a measuring device.\n2) The script waits for a trigger from the oscilloscope before proceeding.</DESCRIPTION>")
############Start of script############

from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,AmplitudeModulation
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config,create_list_data
from SourceFiles.lucid_cmd import LucidCmd

#Establishing connection with LUCIDX
handle = config.handle
Lucid_functions.reset(handle)
frequency =config.frequency_default
power = config.power_default
am_freq = 10e3
am_depth = 90

SignalGeneration.continous_wave_generation(frequency,power)
AmplitudeModulation.amplitude_modulation_internal_on(am_freq,am_depth)


#Internal trigger commands
timer = 2 # Timer in seconds
once_count = 10000
Lucid_functions.send_scpi_command(':INIT:CONT OFF',handle) # disabling continous as we go for internal trigger option
Lucid_functions.send_scpi_command(':TRIG:ADV ONC',handle)
Lucid_functions.send_scpi_command(':TRIG:COUN {}'.format(once_count),handle)
Lucid_functions.send_scpi_command(':TRIG:SOUR TIM',handle)
Lucid_functions.send_scpi_command(':TRIG:TIM:TIME {}'.format(timer),handle)

# AmplitudeModulation.amplitude_modulation_off()
