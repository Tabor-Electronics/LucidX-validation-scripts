print("<DESCRIPTION> Test description :-In this script we have done amplitude modulation on a signal and then used trigger with mentioned timer and once count using bus trigger.</DESCRIPTION>")

# SECTION 1 - Connect LUCIDX, create object of DevicePrint, connect to measuring device
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration, AmplitudeModulation, Triggers
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config, create_list_data
from SourceFiles.lucid_cmd import LucidCmd
from SourceFiles.for_the_gui import DevicePrint
from SourceFiles.calculations import SweepCalculations
import time
import numpy as np

handle = config.handle
Lucid_functions.reset(handle)

# SECTION 1 - Device print setup
devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

# SECTION 1 - Connecting to the spectrum analyzer
devicePrintCmd.msg_user.set('Connecting to the spectrum analyzer')
devicePrintCmd.Print()

if config.spectrum:
    spectrum_analyzer, status = spectrum_methods.reset(config)
    if status:
        spectrum_methods.set_reference_power(config.power_default + 10, spectrum_analyzer)
        spectrum_methods.set_span_freq(200, spectrum_analyzer)

# SECTION 2 - Define parameters and generate signal from LUCIDX
frequency = config.frequency_default
power = config.power_default
am_freq = 10e3
am_depth = 90
timer = 2  # Timer in seconds
once_count = 20000

freq_query, power_query = SignalGeneration.continous_wave_generation(frequency, power)
devicePrintCmd.msg_gui.set("freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00".format(freq_query, power_query))
devicePrintCmd.Print()

am_source_q, am_freq_q, am_depth_q, am_status_q = AmplitudeModulation.amplitude_modulation_internal_on(am_freq, am_depth)
devicePrintCmd.msg_gui.set('AM Frequency={0}::p0.00::n0.00,Depth={1}::p0.00::n0.00'.format(am_freq_q, am_depth_q))
devicePrintCmd.Print()

# SECTION 3 - Spectrum measurement and processing
if config.spectrum:
    cf = frequency
    span = 5 * am_freq / 1e6
    threshold = -30
    sweep_time = 20 * timer
    spectrum_analyzer, status = spectrum_methods.reset(config)
    spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
    spectrum_methods.set_reference_power(15, spectrum_analyzer)
    freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)
    devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out, power_max))
    devicePrintResp.Print()
    spectrum_methods.set_span_freq(span, spectrum_analyzer)
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)
    no_of_triggers = 10
    for trg in range(int(no_of_triggers)):
        Lucid_functions.send_scpi_command('*TRG', handle)
        print("trigger applied")
    Lucid_functions.send_scpi_command(':INIT:CONT OFF', handle)
    freq_out_r, power_max_r = spectrum_methods.get_right(spectrum_analyzer)
    time.sleep(2)
    devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out, power_max))
    devicePrintResp.Print()
    
    spectrum_methods.marker_to_center_frequency(spectrum_analyzer)
    
    spectrum_methods.set_span_freq(0, spectrum_analyzer)
    Triggers.bus_trigger_once(once_count)
    spectrum_methods.set_sweep_time(int(sweep_time), spectrum_analyzer)
    # time.sleep(sweep_time/2)
    for trg in range(int(no_of_triggers)):
        Lucid_functions.send_scpi_command('*TRG', handle)
        print("trigger applied")
    spectrum_methods.set_single_mode()
    
    # no_of_triggers = 10
    # for trg in range(int(no_of_triggers)):
    #     Lucid_functions.send_scpi_command('*TRG', handle)
    #     print("trigger applied")

    spectrum_methods.set_single_mode(spectrum_analyzer)

    time.sleep(sweep_time)
    sweep_pts = int(spectrum_analyzer.query(":SWE:POIN?"))
    data_raw = spectrum_analyzer.query(":TRAC? TRACE1")
    trace = np.array([float(x) for x in data_raw.strip().split(',')])
    time_step = sweep_time / sweep_pts

    rising_edges, falling_edges = SweepCalculations.get_edges(trace, threshold)
    avg_on, avg_off = SweepCalculations.get_averaged_on_off(rising_edges, falling_edges, sweep_time, sweep_pts)

    trigger_time = timer * 1000
    err = abs(avg_on - trigger_time)

    if err < 0.1 * trigger_time:
        devicePrintCmd.msg_user.set('Test pass for trigger timer {}'.format(trigger_time))
        devicePrintCmd.Print()
    else:
        devicePrintCmd.msg_user.set(f'Test Fail for trigger timer {trigger_time}')
        devicePrintCmd.Print()

# SECTION 4 - Wrap-up
devicePrintCmd.msg_user.set('Press enter to finish testing')
devicePrintCmd.Print()
input()

# SECTION 5 - Closing the instruments
AmplitudeModulation.amplitude_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)

### END OF SCRIPT ###