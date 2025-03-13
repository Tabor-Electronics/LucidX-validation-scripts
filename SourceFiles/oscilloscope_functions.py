import pyvisa as visa
import time

class ScopeMethods:
    """
    A class to interface with an oscilloscope using PyVISA.
    Provides methods for connection, configuration, and measurements.
    """
    def __init__(self, scope_address):
        """
        Initialize the scope with the given VISA address.
        """
        self.scope_address = scope_address
        self.resource_manager = visa.ResourceManager()
        self.scope = self.connect(scope_address)  # Connect during initialization

    def connect(self, scope_address):
        """
        Establish a connection to the oscilloscope.
        Returns the oscilloscope's VISA resource or None if connection fails.
        """
        try:
            # Open the oscilloscope resource
            oscilloscope = self.resource_manager.open_resource(scope_address)

            # Query oscilloscope identity
            idn = oscilloscope.query("*IDN?")
            print(f"Oscilloscope ID: {idn}")

            # Perform some initial setup (e.g., reset the oscilloscope)
            oscilloscope.write("*RST")
            print("Oscilloscope reset.")

            return oscilloscope  # Return the connected oscilloscope object
        except Exception as e:
            print(f"Error: Could not connect to the oscilloscope. Details: {e}")
            return None  # Return None if connection fails

    def disconnect(self):
        """Close the connection to the oscilloscope."""
        if self.scope:
            self.scope.close()
            print("Oscilloscope connection closed.")

    def reset(self):
        """Reset all oscilloscope settings and clear measurements."""
        if self.scope:
            self.scope.write('*RST')  # Reset the oscilloscope
            time.sleep(2)  # Wait for reset to complete
            self.scope.write('*OPC')  # Operation complete flag
            self.scope.write(':MEASure:CLEar')  # Clear all measurements
            resp = self.scope.query(':SYST:ERR?')
            print(f"System Error: {resp}")
            print("Oscilloscope reset completed.")

    def autoscale(self):
        """Automatically adjust oscilloscope settings for optimal display."""
        if self.scope:
            self.scope.write('*CLS')  # Clear status
            resp = self.scope.query(':SYST:ERR?')
            print(f"System Error: {resp}")
            self.scope.write(':SYSTem:HEADer OFF')
            resp = self.scope.query(':SYST:ERR?')
            print(f"System Error: {resp}")
            self.scope.write('CDIS')  # Disable display of errors
            resp = self.scope.query(':SYST:ERR?')
            print(f"System Error: {resp}")
            print("Autoscale applied.")

    def run_acquisition(self):
        """Starts the oscilloscope acquisition."""
        if self.scope:
            try:
                self.scope.write(":RUN")
                print("Oscilloscope acquisition started.")
            except Exception as e:
                print(f"Error running oscilloscope acquisition: {e}")

    def stop_acquisition(self):
        """Stops the oscilloscope acquisition."""
        if self.scope:
            try:
                self.scope.write(":STOP")
                print("Oscilloscope acquisition stopped.")
            except Exception as e:
                print(f"Error stopping oscilloscope acquisition: {e}")

    def display_channel(self, channel_number):
        """Enable display for a specific channel."""
        if self.scope:
            self.scope.write(f':CHAN{channel_number}:DISP ON')
            print(f"Channel {channel_number} display enabled.")

    def disable_channel(self, channel_number):
        """Disable display for a specific channel."""
        if self.scope:
            self.scope.write(f':CHAN{channel_number}:DISP OFF')
            print(f"Channel {channel_number} display disabled.")

    def set_horizontal_scale(self, time_per_division):
        """Set the horizontal time scale of the oscilloscope."""
        if self.scope:
            self.scope.write(f':TIMebase:SCALe {time_per_division}')
            print(f"Horizontal time scale set to {time_per_division} sec/div.")

    def set_vertical_scale(self, channel_number, volts_per_division):
        """Set the vertical scale for a specific channel."""
        if self.scope:
            self.scope.write(f':CHAN{channel_number}:SCALe {volts_per_division}')
            self.scope.write(f':CHAN{channel_number}:INP DC50')  # Set input impedance to 50Ω
            print(f"Channel {channel_number} vertical scale set to {volts_per_division} V/div.")

    def measure_delay(self, ch1, ch2):
        """Measure the time delay between two channels."""
        if self.scope:
            try:
                self.scope.write(f':MEASure:DELTatime CHANnel{ch1},CHANnel{ch2}')
                time.sleep(5)
                self.scope.write(':MEASure:RESults?')
                result = self.scope.read()
                delay_time = float(result.split(',')[2])  # Extract delay value
                print(f"Measured delay: {delay_time} sec")
                return delay_time
            except (IndexError, ValueError):
                print("Error: Could not read delay measurement.")
                return None

    def measure_frequency(self, channel_number):
        """Measure the frequency of the signal on a given channel."""
        if self.scope:
            try:
                self.scope.write(f':MEASure:FREQuency CHAN{channel_number}')
                time.sleep(1)
                self.scope.write(':MEASure:RESults?')
                result = self.scope.read()
                frequency = float(result.split(',')[1])  # Extract frequency value
                print(f"Measured frequency on Channel {channel_number}: {frequency} Hz")
                return frequency
            except (IndexError, ValueError):
                print(f"Error: Could not read frequency measurement from Channel {channel_number}.")
                return None

    def measure_burst_period(self, channel_number):
        """Measure the burst period of the signal on a given channel."""
        if self.scope:
            try:
                self.scope.write(f':MEASure:BPERiod CHANnel{channel_number}, 1E-9')
                time.sleep(1)
                self.scope.write(':MEASure:RESults?')
                result = self.scope.read()
                period = float(result.split(',')[1])  # Extract period value
                print(f"Measured burst period on Channel {channel_number}: {period} sec")
                return period
            except (IndexError, ValueError):
                print(f"Error: Could not read burst period measurement from Channel {channel_number}.")
                return None

    def measure_burst_width(self, channel_number):
        """Measure the burst width of the signal on a given channel."""
        if self.scope:
            try:
                self.scope.write(f':MEASure:BWIDTh CHANnel{channel_number}, 1E-9')
                time.sleep(1)
                self.scope.write(':MEASure:RESults?')
                result = self.scope.read()
                width = float(result.split(',')[1])  # Extract width value
                print(f"Measured burst width on Channel {channel_number}: {width} sec")
                return width
            except (IndexError, ValueError):
                print(f"Error: Could not read burst width measurement from Channel {channel_number}.")
                return None

    def measure_burst_interval(self, channel_number):
        """Measure the burst interval of the signal on a given channel."""
        if self.scope:
            try:
                self.scope.write(f':MEASure:BINTerval CHANnel{channel_number}, 1E-9')
                time.sleep(1)
                self.scope.write(':MEASure:RESults?')
                result = self.scope.read()
                interval = float(result.split(',')[1])  # Extract interval value
                print(f"Measured burst interval on Channel {channel_number}: {interval} sec")
                return interval
            except (IndexError, ValueError):
                print(f"Error: Could not read burst interval measurement from Channel {channel_number}.")
                return None


class FetchResults(ScopeMethods):
    """
    Inherits from ScopeMethods class and adds a specialized method to get pulse modulation parameters.
    """
    def __init__(self, scope_address):
        """
        Initialize the FetchResults class with the scope's VISA address.
        """
        super().__init__(scope_address)

    def get_pulse_mod_parameters(self, channel_number,time_scale):
        """Get pulse modulation parameters for the given channel."""
        if self.scope:
            try:
                # Reset and configure the scope
                self.reset()
                self.autoscale()

                # Set display and scales
                self.display_channel(1)
                #self.set_horizontal_scale(0.0000005)  # sec/div
                self.set_horizontal_scale(time_scale)  # sec/div
                self.set_vertical_scale(1, 0.200)  # V/div

                # Measure and return the parameters
                frequency = self.measure_frequency(1)
                burst_period = self.measure_burst_period(1)
                burst_width = self.measure_burst_width(1)
                burst_interval = self.measure_burst_interval(1)

                return frequency, burst_period, burst_width, burst_interval
            except (IndexError, ValueError):
                print(f"Error: Could not read parameters from Channel {channel_number}.")
                return None


# Example Usage
if __name__ == "__main__":
    scope_address = "TCPIP0::192.168.0.92::INSTR"  # Update with actual VISA address
    oscilloscope = FetchResults(scope_address)  # Connects automatically

    # Reset and configure the scope
    oscilloscope.reset()
    oscilloscope.autoscale()

    # Get pulse modulation parameters
    pulse_mod_params = oscilloscope.get_pulse_mod_parameters(1)
    if pulse_mod_params:
        print(f"Pulse Modulation Parameters: {pulse_mod_params}")

    # Disconnect from the oscilloscope
    oscilloscope.disconnect()
