print("<DESCRIPTION> Test description :- This script will generate a signal with pulse modulation for different pulse width\nAn oscilloscope is a better way to see output of pulse modulation (make sure it supports higher frequency range)</DESCRIPTION>")
###########################
###START OF SCRIPT###
# SECTION 0 - Import the required libraries
from SourceFiles.functions_v1 import Lucid_functions,SignalGeneration,PulseModulation
from SourceFiles import config
# from SourceFiles.oscilloscope_functions import scope_methods
from SourceFiles.oscilloscope_functions import FetchResults
from SourceFiles.for_the_gui import DevicePrint

# SECTION 1- Connect LUCIDX, create object of Device print, connect to measuring device
handle = config.handle
Lucid_functions.reset(handle)  # Establishing connection with LUCIDX

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

devicePrintCmd.msg_user.set('Connecting to the Oscilloscope')
devicePrintCmd.Print()
if config.scope:
    
    # Set the oscilloscope's VISA address
    scope_address ="TCPIP0::192.168.0.92::INSTR"  # Update with actual VISA address
    # Create an object of FetchResults
    oscilloscope = FetchResults(scope_address)
    # print("Start Oscilloscope")
    oscilloscope.connect(scope_address)

# SECTION 2- Defining parameters and generate signal form LUCIDX
# Global Parameters
frequency = config.frequency_default
power = config.power_default
pulse_rr = 1e6#config.pulse_repetition_rate_default
width_list =config.pulse_width_list

for width in width_list:
    # # continous wave generation
    freq_query, power_query = SignalGeneration.continous_wave_generation(frequency,power)  # continous signal generation
    # devicePrintCmd.msg_gui.set(f'freq={freq_query}::p0.00::n0.00,pow={power_query}::p0.00::n0.00')
    devicePrintCmd.msg_gui.set('freq={0}::p0.00::n0.00,pow={1}::p0.00::n0.00'.format(freq_query, power_query))
    devicePrintCmd.Print()
    # rep_rate = 1/(width)
    # pulse_rr = rep_rate/2
    # Pulse modulation
    pulse_rr_q, width_q, status = PulseModulation.pulse_modulation_internal_on(pulse_rr, width)
    devicePrintCmd.msg_gui.set(f'Pulse rep rate ={pulse_rr_q}::p0.00::n0.00,pulse width={width_q}::p0.00::n0.00')
    devicePrintCmd.Print()

    
    # SECTION 3 - Get the value from measuring device (Spectrum Analyzer)
    if config.scope:
        time_scale = width_q * 10  # 0.1/pulse_rr ## 500ns for prr =1us
        frequency, burst_period, burst_width, burst_interval = oscilloscope.get_pulse_mod_parameters(1,time_scale)
        # print(f"Pulse Modulation Parameters:")
        # print(f"Frequency: {frequency} Hz")
        # print(f"Burst Period: {burst_period} sec")
        # print(f"Burst Width: {burst_width} sec")
        # print(f"Burst Interval: {burst_interval} sec")
        
        # SECTION 4 - Comparing the results from measuring device (Spectrum Analyzer) with provided input to LUCIDX and Conclude if the result is pass or fail, giving the threshold of 0.1 percentange (TBC in datasheets)
        error = abs(float(burst_width)-float(width))
        threshold = float(0.1*width)
        results =float(burst_width)-float(width)<threshold
        print(results)
        if results:
            print(f'Test pass for Pulse width = {width} ')
            # print(f'Test pass for Frequency = {freq_in} MHz')
            devicePrintCmd.msg_user.set(f'Test pass for Pulse width = {width} ')
            devicePrintCmd.Print()
        else:
            print(f'Test Fail for Pulse width = {width} ')
            devicePrintCmd.msg_user.set(f'Test Fail for Pulse width = {width} ')
            devicePrintCmd.Print()
    
    
    
# SECTION 5 - Closing the instruments
    PulseModulation.pulse_modulation_off()
Lucid_functions.disconnect_lucid(config.handle)
oscilloscope.disconnect()# Disconnect the oscilloscope
###END OF SCRIPT###
