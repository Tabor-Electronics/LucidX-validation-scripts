print("<DESCRIPTION> Test description :-In this script we have done amplitude modulation on a signal and then used trigger with mentioned timer and once count.</DESCRIPTION>")
# SECTION 1 - Connect LUCIDX, create object of DevicePrint, connect to measuring device
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration, AmplitudeModulation, Triggers
from SourceFiles.spectrum_analyser_functions import spectrum_methods
from SourceFiles import config, create_list_data
from SourceFiles.lucid_cmd import LucidCmd
from SourceFiles.for_the_gui import DevicePrint
from SourceFiles.calculations import SweepCalculations
import time
import numpy as np
import statistics


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
        spectrum_methods.set_centre_frequency(1000, spectrum_analyzer)
        spectrum_methods.set_span_freq(200, spectrum_analyzer)

# SECTION 2 - Define parameters and generate signal from LUCIDX
frequency = config.frequency_default
power = config.power_default
am_freq = 10e3
am_depth = 90
timer = 1 # Timer in seconds
ext_freq = 1/timer
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
    sweep_time = max(10 * timer, 10 * (once_count / am_freq))

    spectrum_methods.set_centre_frequency(cf, spectrum_analyzer)
    freq_out, power_max = spectrum_methods.set_marker(spectrum_analyzer)
    devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out, power_max))
    # devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out_r, power_max_r))
    
    devicePrintResp.Print()

    spectrum_methods.set_span_freq(span, spectrum_analyzer)
    spectrum_methods.set_peak_threshold(threshold, spectrum_analyzer)
    freq_out_r, power_max_r = spectrum_methods.get_right(spectrum_analyzer)
    # print(abs(freq_out_r - freq_out))
    while abs(freq_out_r -freq_out)<0.01 :
        freq_out_r, power_max_r = spectrum_methods.get_right(spectrum_analyzer)
    devicePrintResp.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_out, power_max))
    devicePrintResp.Print()
    

    Lucid_functions.send_scpi_command(':INIT:CONT ON', handle)
    # fr, pow = spectrum_methods.get_right_peak(cf, spectrum_analyzer)
    # spectrum_methods.set_marker_at_fr(freq_out_r, spectrum_analyzer)
    spectrum_methods.marker_to_center_frequency(spectrum_analyzer)
    spectrum_methods.set_span_freq(0, spectrum_analyzer)
    devicePrintCmd.msg_user.set('Apply external trigger of {0} Hz to trigger input port of Lucid X device and press enter to continue'.format(ext_freq))
    devicePrintCmd.Print()
    input()
    Triggers.external_trigger_once(once_count)
    spectrum_methods.set_sweep_time(sweep_time, spectrum_analyzer)
    spectrum_methods.set_single_mode(spectrum_analyzer)

    time.sleep(sweep_time)
    sweep_pts = int(spectrum_analyzer.query(":SWE:POIN?"))
    data_raw = spectrum_analyzer.query(":TRAC? TRACE1")
    x=[]
    trace = np.array([float(x) for x in data_raw.strip().split(',')])
    
    
    time_step = sweep_time / sweep_pts
    
    rising_edges, falling_edges = SweepCalculations.get_edges(trace, threshold)
    # if rising_edges.size > 0 and falling_edges.size > 0:
    t_on, t_off = SweepCalculations.get_averaged_on_off(rising_edges, falling_edges, sweep_time, sweep_pts)
    devicePrintResp.msg_gui.set('Ontime={0}::p0.00::n0.00,Offtime={1}::p0.00::n0.00'.format(t_on, t_off))
    devicePrintResp.Print()
    # Reference times in milliseconds
    ref_on = (once_count / am_freq) * 1000
    ref_off = timer * 1000
    
    # Define tolerance map for thresholds
    tolerance_thresholds = [
        (500, 0.04),
        (1000, 0.04),
        (2000, 0.04),
    ]
    default_tolerance = 0.05
    
    # Determine tolerance for ON time
    tolerance_on = next((tol for limit, tol in tolerance_thresholds if ref_on <= limit), default_tolerance)
    # Determine tolerance for OFF time
    tolerance_off = next((tol for limit, tol in tolerance_thresholds if ref_off <= limit), default_tolerance)
    
    # Calculate bounds
    on_min, on_max = ref_on * (1 - tolerance_on), ref_on * (1 + tolerance_on)
    off_min, off_max = ref_off * (1 - tolerance_off), ref_off * (1 + tolerance_off)
    
    # Evaluate result
    if on_min <= t_on <= on_max and off_min <= t_off <= off_max:
        devicePrintCmd.msg_user.set('Test Pass for Trigger Timer')
        devicePrintCmd.Print()
    else:
        devicePrintCmd.msg_user.set(' Test Fail for Trigger Timer')
        devicePrintCmd.Print()
    
# SECTION 4 - Wrap-up
devicePrintCmd.msg_user.set('Press enter to finish testing')
devicePrintCmd.Print()
input()

# SECTION 5 - Closing the instruments
AmplitudeModulation.amplitude_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)

### END OF SCRIPT ###
