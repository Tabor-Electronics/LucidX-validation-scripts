Version = '1.1.2'
#LUCID device
lucid_ip_address = '192.168.7.1' #LSX ip address
port = "5025" #port number
handle = 'TCPIP::{0}::{1}::SOCKET'.format(lucid_ip_address,port)  #Lucid TCPIP address
##Spectrum analyzer parameters
spectrum = True
spectrum_ip_address_israel = '192.168.0.103'
spectrum_ip_address_india = '192.90.70.36'
spectrum_tcpip = 'TCPIP::{0}::{1}::SOCKET'.format(spectrum_ip_address_israel,port)  # Spectrum analyzer TCPIP  address
default_cf =1e3 #in Mhz
default_span = 200
default_start = 500
default_stop = 5000
## Continuous wave parameter
frequency_default = 1e3
frequencies = [1e3,2e3, 3e3, 4e3,5e3,6e3,7e3,8e3]#,9e3,10e3,11e3,12e3,13e3,14e3,15e3,16e3,17e3,18e3,19e3, 20e3] #Frequency in Mhz
frequency_resolution = 0.001 #1KHz
power_default = 5
power_resolution =0.01 #0.01 dBm
power_list = [-30,-10,5,10,20]
##AM parameters
am_freq_default = 10e3
am_frequencies_list =  [100, 1000, 2000, 30000, 70000,100000]
am_depth_default = 50
am_depth_list = [0,10,20,30,40,50,60,70,80,90,100]
am_ext_frequencies = [100e3, 200e3, 300e3]
##FM parameters
fm_freq_default= 100e3
fm_frequencies_list = [10, 100, 1000, 10000, 100000, 1000000]
fm_deviation_default = 1e6
fm_deviation_list = [1e6,2e6,3e6,4e6,5e6]
fm_ext_frequencies = [100e3, 200e3, 300e3]
##PM parameters
pm_freq_min = 1
pm_freq_max = 1e6
pm_freq_default= 1e6
pm_deviation_default = 80
pm_frequencies = [1000, 10000, 100000, 1000000]
pm_deviation_list = [0,30,45,90,125,180]
##Pulse parameters
pulse_repetition_rate_default = 1e6
pulse_repetition_rate =[1e6,2e6,3e6,4e6,5e6,6e6,7e6,8e6,9e6,10e6]
pulse_width_default = 32e-9
pulse_width_list = [32e-9,32e-8,32e-7,32e-6,32e-5,32e-3,250e-3,100e-3]
