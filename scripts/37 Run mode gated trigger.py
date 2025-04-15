"""
1) In this script we are using spectrum analyzer as a measuring device
# if spectrum is not connected to LAN please chnage the variable on line 16 "spectrum = False" and run the script on debug.
"""
from functions_v1 import Lucid_functions
from spectrum_analyser_functions import spectrum_methods

handle = 'TCPIP0::192.168.7.1::5025::SOCKET'
Lucid_functions.lsx_connection(handle)
status_lsx = Lucid_functions.reset_and_clear(handle)  # reset and clear the lucid x desktop
if status_lsx:
    print("Factory reset done LSX")
else:
    print("Error while reseting the LucidX module")
#####################################################################

#insert some signal to be triggered
Lucid_functions.send_scpi_command(':INIT:CONT OFF',handle)
Lucid_functions.send_scpi_command(':INIT:GATE ON',handle)
Lucid_functions.send_scpi_command(':TRIG:SOUR EXT',handle)
