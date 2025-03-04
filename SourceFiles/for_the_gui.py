import pyvisa as visa
import time

from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd
class Print_function(object):
    def __init__(self,handle):
        handle = self.handle
        
    def print_freq_pow_to_gui(freq=1e9,freq__dev_p=0.000,freq_dev_n=0.000,pow=5,power_dev_p=0.000,power_dev_n=0.000):
        print("<TOGUI>freq={0}::p{1}::n{2},pow={3}::p{4}::n{5}</TOGUI>".format(freq,freq__dev_p,freq_dev_n,pow,power_dev_p,power_dev_n))
        
    def print_to_user(msg= 'Hi User'):
	    print("<TOUSER>"+msg+"</TOUSER>")