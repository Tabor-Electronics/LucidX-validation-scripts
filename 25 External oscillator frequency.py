print("<DESCRIPTION> Test description :- Script tests the external source frequency fro the ref out of the Lucid module\nSteps:\n1) Connect an external source to the Ref in (input port) of the lucid module.\n2) Provide a signal of 10MHz and 100Mhz\n3) Connect the RF out and REF out (output ports) to the measuring device</DESCRIPTION>")
# print("Note: It may be tested on Spectrum Analyzer or Oscilloscope")
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration
from SourceFiles.spectrum_analyser_functions import spectrum_methods
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
        spectrum_methods.set_reference_power(config.power_default + 7,spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz
devicePrintCmd.msg_user.set('Connect the ref out to spectrum and ref in from external signal generator\nConnect external signal sin wave having 10MHz')
devicePrintCmd.Print()
input()
rosc_query = Lucid_functions.send_scpi_query(":ROSC:SOUR?",handle)

if "EXT" in rosc_query:
    ext_freq = 10 #in MHz
    # Lucid_functions.send_scpi_command(":ROSC:SOUR:FREQ 10e6",handle)
    # Lucid_functions.send_scpi_command(":POW 5",handle)
    #rosc_freq = Lucid_functions.send_scpi_query(":ROSC:SOUR:FREQ?", handle)
    spectrum_methods.set_centre_frequency(ext_freq, spectrum_analyzer)  # set center frequency on spectrum
    spectrum_methods.set_start_freq(0, spectrum_analyzer)
    freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
    devicePrintCmd.msg_user.set('External source detected')
    devicePrintCmd.Print()
    devicePrintResp.msg_gui.set(f'freq={freq_out}::p0.00::n0.00,pow={power_max}::p0.00::n0.00')
    devicePrintResp.Print()
    devicePrintCmd.msg_user.set(f'Test pass for External reference oscillatorMHz')
    devicePrintCmd.Print()
    devicePrintCmd.msg_user.set('Press enter for next test')
    devicePrintCmd.Print()
    input()
else:
    devicePrintCmd.msg_user.set('External source NOT detected')
    devicePrintCmd.Print()

# disconnect instrument
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###