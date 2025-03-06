import pyvisa as visa
import time
import config


class spectrum_methods(object):
    def __init__(self, device_address):
        # self.device_address = device_address
        self.spectrum_tcpip = config.spectrum_tcpip

    def connect_spectrum_via_lan(self):
        # device_address = 'TCPIP::192.90.70.36::5025::SOCKET'
        try:
            rm = visa.ResourceManager()
            spectrum_analyzer = rm.open_resource(self.spectrum_tcpip)
            spectrum_analyzer.timeout = 2000
            spectrum_analyzer.write_termination = '\n'
            spectrum_analyzer.read_termination = '\n'
            print(spectrum_analyzer)
            spectrum_analyzer.write('*IDN?')
            # spectrum_analyzer.timeout = 1000
            idn_response = spectrum_analyzer.read()
            # spectrum_analyzer.write('*RST')
            # spectrum_analyzer.write('*CLS')

            print("Spectrum Analyzer IDN Response: {}".format(idn_response))
        except visa.Error as e:
            print("Error reading IDN: {}".format(e))
        return spectrum_analyzer
    def resetX(self):
        try:
            device_address = 'TCPIP::192.90.70.103::5025::SOCKET'
            # device_address = self.device_address
            spectrum_analyzer=spectrum_methods.connect_spectrum_via_lan(device_address)
            spectrum_analyzer.write('*RST')
            spectrum_analyzer.write('*CLS')
            spectrum_analyzer.write(':INIT:REST')
            spectrum_methods.set_continous_mode(spectrum_analyzer)
            time.sleep(1)
            status = True
            return spectrum_analyzer,status
        except Exception as e:
            print('[!] Exception: ' + str(e))
            
    def reset(self):
        try:
            device_address = 'TCPIP::192.90.70.103::5025::SOCKET'
            spectrum_analyzer = spectrum_methods.connect_spectrum_via_lan(self)
            spectrum_analyzer.write('*RST')
            spectrum_analyzer.write('*CLS')
            spectrum_analyzer.write(':INIT:REST')
            spectrum_methods.set_continous_mode(spectrum_analyzer)
            time.sleep(1)
            return spectrum_analyzer, True
        except Exception as e:
            print('[!] Exception: ' + str(e))
            raise
    def reset_and_clear_sa(spectrum_analyzer):
        spectrum_analyzer.write('*RST')
        spectrum_analyzer.write('*CLS')
        spectrum_analyzer.write(':INIT:REST')
        spectrum_methods.set_continous_mode(spectrum_analyzer)
        time.sleep(1)
        status = True
        return status
    # def disconnect_spectrum(spectrum_analyzer):
    #     spectrum_analyzer.close()
    def set_continous_mode(spectrum_analyzer):
        spectrum_analyzer.write(':INIT:CONT 1')

    def set_centre_frequency(cf, spectrum_analyzer):
        spectrum_analyzer.write(':SENS:FREQ:CENT {0} MHz'.format(cf))
        time.sleep(2)

    def set_start_freq(start_freq, spectrum_analyzer):
        spectrum_analyzer.write(':SENS:FREQ:STAR {0} MHz'.format(start_freq))
        time.sleep(2)

    def set_stop_freq(stop_freq, spectrum_analyzer):
        spectrum_analyzer.write(':SENS:FREQ:STOP {0} MHz'.format(stop_freq))
        time.sleep(2)

    def set_span_freq(span_freq, spectrum_analyzer):
        spectrum_analyzer.write(':SENS:FREQ:SPAN {0} MHz'.format(span_freq))
        time.sleep(2)

    def set_reference_power(ref_level, spectrum_analyzer):
        spectrum_analyzer.write('DISP:WIND:TRAC:Y:RLEV {0} dbm'.format(ref_level))
        time.sleep(2)

    def set_peak_threshold(threshold, spectrum_analyzer):
        spectrum_analyzer.write(':CALC:MARK:PEAK:THR {0} dbm'.format(threshold))
        time.sleep(2)

    def set_resolution_bandwidth(BW, spectrum_analyzer):
        spectrum_analyzer.write(':SENS:BAND:RES {0}'.format(BW))
        time.sleep(2)

    def set_marker(spectrum_analyzer):
        spectrum_analyzer.write(':CALC:MARK1:STAT ON')
        spectrum_methods.set_marker_at_peak(spectrum_analyzer)
        # spectrum_methods.marker_to_center_frequency(spectrum_analyzer)
        freq_out = spectrum_methods.get_marker_frequency(spectrum_analyzer)
        power_max = spectrum_methods.get_marker_power(spectrum_analyzer)
        # print('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
        return freq_out, power_max

    def set_marker_at_peak(spectrum_analyzer):
        spectrum_analyzer.write(':CALC:MARK1:STAT ON')
        spectrum_analyzer.write(':CALC:MARK1:MAX')

    def get_marker_frequency(spectrum_analyzer):
        spectrum_analyzer.write('CALC:MARK1:X?')
        time.sleep(2)
        resp = spectrum_analyzer.read()
        freq_out = float(resp) / 1e6
        return freq_out

    def marker_to_center_frequency(spectrum_analyzer):
        spectrum_analyzer.write(':CALC:MARK1:STAT ON')
        spectrum_analyzer.write('CALC:MARK1:SET:CENT')
        time.sleep(2)

    def get_marker_power(spectrum_analyzer):
        spectrum_analyzer.write('CALC:MARK1:Y?')
        time.sleep(2)
        power_max = spectrum_analyzer.read()
        return power_max

    def get_delta_left_peak(spectrum_analyzer):
        # Enable the delta marker
        spectrum_analyzer.write(':CALC:MARK1:MODE DELTA')
        spectrum_analyzer.write(':CALCulate:MARKer1:MAXimum:LEFt')
        time.sleep(1)
        freq_out = spectrum_methods.get_marker_frequency(spectrum_analyzer)
        power_max = spectrum_methods.get_marker_power(spectrum_analyzer)
        print('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
        return freq_out, power_max

    def get_delta_right_peak(spectrum_analyzer):
        # Enable the delta marker
        spectrum_analyzer.write(':CALC:MARK1:MODE DELTA')
        spectrum_analyzer.write(':CALCulate:MARKer1:MAXimum:RIGHt')
        time.sleep(1)
        freq_out = spectrum_methods.get_marker_frequency(spectrum_analyzer)
        power_max = spectrum_methods.get_marker_power(spectrum_analyzer)
        print('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
        return freq_out, power_max

    def get_left_peak(spectrum_analyzer):
        spectrum_analyzer.write(':CALCulate:MARKer1:MAXimum:LEFt')
        time.sleep(1)
        freq_out = spectrum_methods.get_marker_frequency(spectrum_analyzer)
        power_max = spectrum_methods.get_marker_power(spectrum_analyzer)
        print('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
        return freq_out, power_max
    def get_right_peak(spectrum_analyzer):
        spectrum_analyzer.write(':CALCulate:MARKer1:MAXimum:RIGHt')
        time.sleep(1)
        freq_out = spectrum_methods.get_marker_frequency(spectrum_analyzer)
        power_max = spectrum_methods.get_marker_power(spectrum_analyzer)
        print('power ={1} dBm at frequency = {0} MHz'.format(freq_out, power_max))
        return freq_out, power_max
    def get_peak_table(spectrum_analyzer):
        spectrum_analyzer.write(':INIT:CONT 1')
        time.sleep(1)
        spectrum_analyzer.write(':CAl:MARK1:PEAK:TABLE:STAT 1')
        time.sleep(1)
        peak_table_data=spectrum_analyzer.write(':CAl:MARK1:PEAK:TABLE:DATA?')
        time.sleep(1)
        print(peak_table_data)
        # peak_table = peak_table_data.split(',')

        # # Print out the peaks
        # for i in range(0, len(peak_table), 2):
        #     frequency = peak_table[i]
        #     amplitude = peak_table[i + 1]
        #     print(f"Peak {i // 2 + 1}: Frequency = {frequency} Hz, Amplitude = {amplitude} dBm")






# spectrum_analyzer.write(':CALCulate:MARKer1:PEAK:EXCursion 0')
   # # Move the delta marker to the next peak to the left
        # spectrum_analyzer.write(':CALC:MARK1:DELTA:PEAK:LEFT')
        #
        # # Query the delta marker's frequency difference (relative to the reference marker)
        # delta_frequency = spectrum_analyzer.write(':CALC:MARK1:DELTA:X?')
        # resp = spectrum_analyzer.read()
        # print(f'Delta Marker Frequency Difference: {delta_frequency} Hz')
        #
        # # Query the delta marker's amplitude difference
        # delta_amplitude = spectrum_analyzer.write(':CALC:MARK1:DELTA:Y?')
        # resp = spectrum_analyzer.read()
        # print(f'Delta Marker Amplitude Difference: {delta_amplitude} dB')
