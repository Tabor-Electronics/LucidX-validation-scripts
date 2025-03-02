import pyvisa as visa
import time

from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd
class Lucid_functions(object):
    def __init__(self,handle):
        handle = self.handle

    def lsx_connection(handle):
       try:
            idn_response = Lucid_functions.send_scpi_query('*IDN?', handle)
            print("LucidX IDN Response: {}".format(idn_response))
       except Exception as e:
             print('[!] Exception: ' + str(e))
    def reset(handle):
        try:
            Lucid_functions.lsx_connection(handle)
            Lucid_functions.send_scpi_command("*RST", handle)
            time.sleep(10)
            error = Lucid_functions.get_lucid_error(handle)  # Error SCPI query
        except Exception as e:
            print('[!] Exception: ' + str(e))
    def clear(handle):
        try:
            Lucid_functions.send_scpi_command("*CLS", handle)
        except Exception as e:
            print('[!] Exception: ' + str(e))

    def send_scpi_query(query, handle):
        try:
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(handle)
            # Need to define the termination string
            session.write_termination = '\n'
            session.read_termination = '\n'
            response = str(session.query(query))
            session.close()
            return response

        except Exception as e:
            print('[!] Exception: ' + str(e))
    def send_scpi_command(scpi_command,handle):
        try:
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(handle)

            # Need to define the termination string
            session.write_termination = '\n'
            session.read_termination = '\n'

            session.write(scpi_command)
            session.close()
        except Exception as e:
            print('[!] Exception: ' + str(e))

    def send_scpi_command_byte(self,command_in_byte, handle):
        response = ""

        try:
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(handle)
            # Need to define the termination string
            session.write_termination = '\n'
            session.read_termination = '\n'
            session.write_raw(command_in_byte)

            response = session.read()
            session.close()
        except Exception as e:
            print('[!] Exception: ' + str(e))
        return response
    def reset_and_clear(handle):
        Lucid_functions.send_scpi_command("*CLS",handle)
        Lucid_functions.send_scpi_command("*RST", handle)
        time.sleep(10)
        status = True
        return status
    def get_lucid_error(handle):
        error= Lucid_functions.send_scpi_query(':SYST:ERR?', handle)
        #print("ERRor:{0}".format(error))
        return error


    def freq_pow_out(power,frequency,handle):
        Lucid_functions.send_scpi_command(frequency, handle)
        Lucid_functions.send_scpi_command(power, handle)
        Lucid_functions.send_scpi_command(":OUTP ON", handle)
        print(frequency,power)

    def disconnect_lucid(handle):
        Lucid_functions.send_scpi_command(LucidCmd.OUTP.format("OFF"), handle)
        print("Test completed")

class SignalGeneration():

    def continous_wave_generation(frequency,power):
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'# Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.FREQ.format(frequency*1e6), handle)  # SCPI command for frequency
        Lucid_functions.send_scpi_command(LucidCmd.POW.format(power), handle)  # SCPI command for power
        freq_query = Lucid_functions.send_scpi_query(LucidCmd.FREQ_Q, handle)  # SCPI query to frequency
        power_query = Lucid_functions.send_scpi_query(LucidCmd.POW_Q, handle)  # SCPI query to power
        Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('ON'), handle)  # Channel OUTPUT ON scpi command
        outp_query = Lucid_functions.send_scpi_query(LucidCmd.OUTP_Q, handle)  # Channel OUTPUT ON scpi query
        error = Lucid_functions.get_lucid_error(handle)  # Error SCPI query
        return freq_query,power_query

class AmplitudeModulation():

    def amplitude_modulation_internal_on(am_freq,depth):
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.AM_SOURCE.format('INT'), handle)
        Lucid_functions.send_scpi_command(LucidCmd.AM_FREQ.format(am_freq), handle)
        Lucid_functions.send_scpi_command(LucidCmd.AM_DEPTH.format(depth), handle)
        Lucid_functions.send_scpi_command(LucidCmd.AM.format('ON'), handle)
        am_source_q=Lucid_functions.send_scpi_query(LucidCmd.AM_SOURCE_Q, handle)
        am_status_q = Lucid_functions.send_scpi_query(LucidCmd.AM_Q, handle)
        am_freq_q= Lucid_functions.send_scpi_query(LucidCmd.AM_FREQ_Q, handle)
        am_depth_q= Lucid_functions.send_scpi_query(LucidCmd.AM_DEPTH_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return am_source_q,am_freq_q,am_depth_q,am_status_q
    def amplitude_modulation_external_on():
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.AM_SOURCE.format('EXT'), handle)
        Lucid_functions.send_scpi_command(LucidCmd.AM.format('ON'), handle)
        am_source_q = Lucid_functions.send_scpi_query(LucidCmd.AM_SOURCE_Q, handle)
        am_status_q = Lucid_functions.send_scpi_query(LucidCmd.AM_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return am_source_q,am_status_q
    def amplitude_modulation_off():
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.AM.format('OFF'), handle)
        am_status_q = Lucid_functions.send_scpi_query(LucidCmd.AM_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return am_status_q

class FrequencyModulation():

    def frequency_modulation_internal_on(fm_freq,deviation):
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.FM_SOURCE.format('INT'), handle)
        Lucid_functions.send_scpi_command(LucidCmd.FM_FREQ.format(fm_freq), handle)
        Lucid_functions.send_scpi_command(LucidCmd.FM_DEV.format(deviation), handle)
        Lucid_functions.send_scpi_command(LucidCmd.FM.format('ON'), handle)
        fm_source_q=Lucid_functions.send_scpi_query(LucidCmd.FM_SOURCE_Q, handle)
        fm_status_q = Lucid_functions.send_scpi_query(LucidCmd.FM_Q, handle)
        fm_freq_q= Lucid_functions.send_scpi_query(LucidCmd.FM_FREQ_Q, handle)
        fm_dev_q= Lucid_functions.send_scpi_query(LucidCmd.FM_DEV_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return fm_source_q,fm_freq_q,fm_dev_q,fm_status_q
    def frequency_modulation_external_on(deviation):
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.FM_DEV.format(deviation), handle)
        fm_dev_q = Lucid_functions.send_scpi_query(LucidCmd.FM_DEV_Q, handle)
        Lucid_functions.send_scpi_command(LucidCmd.FM_SOURCE.format('EXT'), handle)
        Lucid_functions.send_scpi_command(LucidCmd.FM.format('ON'), handle)
        fm_source_q = Lucid_functions.send_scpi_query(LucidCmd.FM_SOURCE_Q, handle)
        fm_status_q = Lucid_functions.send_scpi_query(LucidCmd.FM_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return fm_dev_q,fm_source_q,fm_status_q
    def frequency_modulation_off():
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.FM.format('OFF'), handle)
        fm_status_q = Lucid_functions.send_scpi_query(LucidCmd.FM_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return fm_status_q
class PhaseModulation():

    def phase_modulation_internal_on(pm_freq,deviation):
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.PM_FREQ.format(pm_freq), handle)
        Lucid_functions.send_scpi_command(LucidCmd.PM_DEV.format(deviation), handle)
        Lucid_functions.send_scpi_command(LucidCmd.PM.format('ON'), handle)
        pm_status_q = Lucid_functions.send_scpi_query(LucidCmd.PM_Q, handle)
        pm_freq_q= Lucid_functions.send_scpi_query(LucidCmd.PM_FREQ_Q, handle)
        pm_dev_q= Lucid_functions.send_scpi_query(LucidCmd.PM_DEV_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return pm_freq_q,pm_dev_q,pm_status_q
    def phase_modulation_off():
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.PM.format('OFF'), handle)
        pm_status_q = Lucid_functions.send_scpi_query(LucidCmd.PM_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return pm_status_q
class PulseModulation():
    def pulse_modulation_internal_on(pulse_rep_rate,pulse_width):
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(':OUTPut ON', handle)
        # Lucid_functions.send_scpi_command(LucidCmd.PULSE_SOURCE.format('INT'), handle)
        Lucid_functions.send_scpi_command(LucidCmd.PULSE_FREQ.format(pulse_rep_rate), handle)
        Lucid_functions.send_scpi_command(LucidCmd.PULSE_WIDT.format(pulse_width), handle)
        Lucid_functions.send_scpi_command(LucidCmd.PULSE.format('ON'), handle)
        error = Lucid_functions.get_lucid_error(handle)
        # pulse_source_q = Lucid_functions.send_scpi_query(LucidCmd.PULSE_SOURCE_Q, handle)
        pulse_status_q = Lucid_functions.send_scpi_query(LucidCmd.PULSE_Q, handle)
        pulse_rep_rate_q = Lucid_functions.send_scpi_query(LucidCmd.PULSE_FREQ_Q, handle)
        pulse_width_q = Lucid_functions.send_scpi_query(LucidCmd.PULSE_WIDT_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return pulse_rep_rate_q,pulse_width_q, pulse_status_q

    def pulse_modulation_external_on():
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.PULSE_SOURCE.format('EXT'), handle)
        Lucid_functions.send_scpi_command(LucidCmd.PULSE.format('ON'), handle)
        pulse_source_q = Lucid_functions.send_scpi_query(LucidCmd.PULSE_SOURCE_Q, handle)
        pulse_status_q = Lucid_functions.send_scpi_query(LucidCmd.PULSE_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return pulse_source_q, pulse_status_q

    def pulse_modulation_off():
        handle = 'TCPIP::192.168.7.1::5025::SOCKET'  # Lucid TCPIP address
        Lucid_functions.send_scpi_command(LucidCmd.PULSE.format('OFF'), handle)
        pulse_status_q = Lucid_functions.send_scpi_query(LucidCmd.PULSE_Q, handle)
        error = Lucid_functions.get_lucid_error(handle)
        return pulse_status_q
class sweeps():
    def frequency_sweep(start_freq, stop_freq, steps, direction, time_cmd):
        handle = config.handle
        Lucid_functions.send_scpi_command(':OUTPut ON', handle)
        Lucid_functions.send_scpi_command(':FRSW:STAR {0}e6'.format(start_freq), handle)
        Lucid_functions.send_scpi_command(':FRSW:STOP {0}e6'.format(stop_freq), handle)
        Lucid_functions.send_scpi_command(':FRSW:DIR {0}'.format(direction), handle)
        Lucid_functions.send_scpi_command(':FRSW:STEP {0}'.format(steps), handle)
        Lucid_functions.send_scpi_command(':FRSW:TIME {0}'.format(time_cmd), handle)
        start_freq_query = Lucid_functions.send_scpi_query(':FRSW:STAR?', handle)
        stop_freq_query = Lucid_functions.send_scpi_query(':FRSW:STOP?', handle)
        step_query = Lucid_functions.send_scpi_query(':FRSW:STEP?', handle)
        direction_query = Lucid_functions.send_scpi_query(':FRSW:DIR?', handle)
        step_query = Lucid_functions.send_scpi_query(':FRSW:STEP?', handle)
        
        time_query = Lucid_functions.send_scpi_query(':FRSW:TIME?', handle)
        
        Lucid_functions.send_scpi_command(':FRSW ON', handle)
        return  start_freq_query,stop_freq_query,step_query,time_query,direction_query
        
    
    def power_sweep(start_power, stop_power, steps, direction, time_cmd):
        handle = config.handle
        Lucid_functions.send_scpi_command(':OUTPut ON', handle)
        Lucid_functions.send_scpi_command(':PRSW ON', handle)
        Lucid_functions.send_scpi_command(':PRSW:STAR {0}'.format(start_power), handle)
        Lucid_functions.send_scpi_command(':PRSW:STOP {0}'.format(stop_power), handle)
        Lucid_functions.send_scpi_command(':PRSW:DIR {0}'.format(direction), handle)
        Lucid_functions.send_scpi_command(':PRSW:STEP {0}'.format(steps), handle)
        Lucid_functions.send_scpi_command(':PRSW:TIME {0}'.format(time_cmd), handle)
        start_power_query = Lucid_functions.send_scpi_query(':PRSW:STAR?', handle)
        stop_power_query = Lucid_functions.send_scpi_query(':PRSW:STOP?', handle)
        step_query = Lucid_functions.send_scpi_query(':PRSW:STEP?', handle)
        direction_query = Lucid_functions.send_scpi_query(':PRSW:DIR?', handle)
        step_query = Lucid_functions.send_scpi_query(':PRSW:STEP?', handle)
        time_query = Lucid_functions.send_scpi_query(':PRSW:TIME?', handle)
        return start_power_query,stop_power_query,step_query,time_query,direction_query
    
