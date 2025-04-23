print("<DESCRIPTION> Test Ddescription - This script creates and define multiple patterns with given parameters")
# print("There are variable parameters defined for, number of repetition, ontime and offtime. U can make them user input to make the test more flexible")
#
from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config,create_pattern_data,calculations
from SourceFiles.lucid_cmd import LucidCmd
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
        spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz

# SECTION 2- Defining parameters and generate signal form LUCIDX
# #Global Parameters
frequency = config.frequency_default
power = config.power_default
no_of_reps = [1,2]
ontime = [100000,200000] #in useconds
offtime= [100000,800000] #in useconds

# continous wave generation
freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, power)
devicePrintCmd.msg_gui.set("freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00".format(freq_query, power_query))
devicePrintCmd.Print()

#Creating an object for patter generation
Patternsetup = create_pattern_data.PatternData()

for i in range(len(no_of_reps)):
    pattern_row = create_pattern_data.PatternRow(no_of_repetition=no_of_reps[i], offtime=offtime[i] * 10**3, ontime=ontime[i] * 10**3)
    Patternsetup.add_pattern_row(pattern_row)
response = Patternsetup.send_scpi_command_byte(handle)
Lucid_functions.send_scpi_command(LucidCmd.PATTERN_ON, handle)
for i in range(len(no_of_reps)):
    pattern_number = i+1
    patt_def = Lucid_functions.send_scpi_query(LucidCmd.PATTERN_DEF_Q.format(pattern_number), handle)
    # print("Pattern :-",patt_def)
    # SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
    if config.spectrum:  # spectrum commands for automation
        cf = frequency  # center frequency on measuring device
        sweep_time =(sum(ontime)+sum(offtime))*max(no_of_reps)
        sweep_points =2001
        spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)  # set center frequency on spectrum
        freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
        devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out, power_max))
        devicePrintResp.Print()
        spectrum_methods.set_span_freq(0, spectrum_analyzer)
        swe_tim = spectrum_methods.set_sweep_time(0.002, spectrum_analyzer)
        swe_pts = spectrum_methods.set_sweep_pts(sweep_points,spectrum_analyzer)
        swe_pts = spectrum_methods.get_sweep_pts(sweep_points,spectrum_analyzer)
        
    devicePrintCmd.msg_user.set('Press enter for next frequency test')
    devicePrintCmd.Print()
    input()

# # disconnect instrument
# Lucid_functions.send_scpi_command(LucidCmd.PATTERN_OFF, handle)
# Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###

