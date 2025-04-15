print("<DESCRIPTION> Test description - This script performs amplitude modulation on a signal and waits for a trigger detected by the instrument."
      "\nSteps:\n1) The instrument detects the trigger and generates a signal.\n2) The oscilloscope is used to measure the generated signal parameters.</DESCRIPTION>")

############ Start of Script ############
import time
import pyvisa as visa
from SourceFiles.functions_v1 import Lucid_functions, SignalGeneration, AmplitudeModulation
from SourceFiles.oscilloscope_functions import scope_methods  # Correct import of oscilloscope class from the correct file
from SourceFiles import config

# Establishing connection with LUCID device
handle = config.handle
Lucid_functions.reset(handle)

# Default configuration values
frequency = config.frequency_default
power = config.power_default
am_freq = 10e3  # AM frequency in Hz
am_depth = 90   # AM depth in percentage
timer = 2       # Trigger timer in seconds

rm = visa.ResourceManager()
print(rm.list_resources())
# Configure the instrument to detect the trigger
def configure_trigger(timer, handle):
    """
    Configures the instrument to wait for a trigger before generating the signal.
    """
    commands = [
        (':INIT:CONT OFF', "Disable continuous mode"),
        (':TRIG:ADV STEP', "Set trigger advance to STEP mode"),
        (':TRIG:SOUR TIM', "Set trigger source to TIMER"),
        (f':TRIG:TIM:TIME {timer}', f"Set trigger time to {timer} seconds")
    ]

    for cmd, desc in commands:
        Lucid_functions.send_scpi_command(cmd, handle)
        error = Lucid_functions.get_lucid_error(handle)
        if error:
            print(f"Error in {desc}: {error}")

# Apply trigger configuration
configure_trigger(timer, handle)

# Wait for trigger event in the instrument
print("Waiting for the instrument to detect a trigger event...")
while True:
    trigger_status = Lucid_functions.send_scpi_query(handle, ":TRIG:STATE?")
    if trigger_status == "1":
        print("Trigger detected in the instrument!")
        break
    time.sleep(0.1)  # Small delay to avoid excessive querying

# Generate the signal after the trigger is detected
SignalGeneration.continous_wave_generation(frequency, power)
AmplitudeModulation.amplitude_modulation_internal_on(am_freq, am_depth)

# Connect to the oscilloscope using the address from config
scope_address = config.oscilloscope_address  # Get oscilloscope address from config
oscilloscope = scope_methods(scope_address)  # Create an instance of the oscilloscope class
oscilloscope.scope_connection(scope_address)  # Establish connection


# Fetch and display oscilloscope measurements
measured_frequency = scope_methods.get_frequency(oscilloscope)
measured_burst_width = scope_methods.get_burst_width(oscilloscope)
print(f"Measured Frequency: {measured_frequency} Hz")
print(f"Measured Burst Width: {measured_burst_width} s")

# Verify trigger timer setting
temp = Lucid_functions.send_scpi_query(handle, ":TRIG:TIM:TIME?")
print(f"Trigger Timer set to: {temp} seconds")

# AmplitudeModulation.amplitude_modulation_off()  # Uncomment if needed
