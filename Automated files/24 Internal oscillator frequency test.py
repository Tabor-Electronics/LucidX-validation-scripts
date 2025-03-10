print("Script tests the Internal source frequency for the ref out of the Lucid module")
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
        spectrum_methods.set_reference_power(config.power_default + 5,spectrum_analyzer)  # step 1) set reference power level on spectrum
        spectrum_methods.set_span_freq(200, spectrum_analyzer)  # step 2) set span to 200MHz
        
Lucid_functions.send_scpi_command(":ROSC:SOUR INT",handle)
rosc_query = Lucid_functions.send_scpi_query(":ROSC:SOUR?", handle)
devicePrintCmd.msg_user.set('Connect the ref out to spectrum, Make sure no external source is connected to the ref in port')
devicePrintCmd.Print()
input()
if "INT" in rosc_query:
    r_freq=10
    devicePrintResp.msg_gui.set(f'freq={r_freq}::p0.00::n0.00,pow={config.power_default}::p0.00::n0.00')
    devicePrintResp.Print()
    Lucid_functions.send_scpi_command(':ROSC:OUTP:FREQ {0}e6'.format(r_freq), handle)
    rosc_sour = Lucid_functions.send_scpi_query(":ROSC:SOUR?", handle)
    rosc_freq = Lucid_functions.send_scpi_query(":ROSC:OUTP:FREQ?", handle)
    spectrum_methods.set_centre_frequency(r_freq, spectrum_analyzer)  # set center frequency on spectrum
    spectrum_methods.set_start_freq(0, spectrum_analyzer)
    freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)  # Read marker x (frequency) and y (power)
    devicePrintResp.msg_gui.set(f'freq={freq_out}::p0.00::n0.00,pow={power_max}::p0.00::n0.00')
    devicePrintResp.Print()
    if (freq_out==r_freq):
        devicePrintCmd.msg_user.set(f'Test pass for Internal reference oscillator frequency of {r_freq}')
        devicePrintCmd.Print()
    else:
        devicePrintCmd.msg_user.set(f'Test Fail for Internal reference oscillator frequency of {r_freq}')
        devicePrintCmd.Print()
devicePrintCmd.msg_user.set('Press enter for complete this test')
devicePrintCmd.Print()
input()


# SECTION 5 - Closing the instruments
Lucid_functions.disconnect_lucid(config.handle)
###END OF SCRIPT###