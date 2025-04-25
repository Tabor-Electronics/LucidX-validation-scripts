'''
SCPI command format- :SOURCE:LIST:DATA {#< header><binary block>}
#Description:-
-This command will download list data to the Lucid unit. List data is loaded to the Lucid unit using highspeed binary data transfer. High-speed binary data transfer allows any number of 8-bit bytes to be transmitted in a message.
-This command is particularly useful for sending large quantities of data.
#Example:-
-The command will download to the generator a block of list-related data of 40 entries:

        :SOURCE:LIST:DATA #3640<binary_block>

-This command causes the transfer of 640 bytes of data (40 list entries).
The <header> is interpreted
this way:
• The ASCII "#" ($23) designates the start of the binary data block.
• "3" designates the number of digits that follow representing the binary data block size in bytes.
• "600" is the number of bytes to follow.
The <binary_block> represents list-related data.
Each entry in the list is represented by 16 bytes.
#User information :-
- In order to download/add List to the LUCID X device, user is supposed to provide the paramer in following format

list_row<n>=ListRow(frequency=100000, power=4000, last_entry=1, advance=1, dwell_time=100000)
Listsetup.add_list_row(list_row<n>)

#Note- This script will follow the sequence for step in the same order as they are defined here, and can download upto 4096 such Lists

Frequency in range(9e3 to 1.2e10) in units of 1 mHz
Power in range(-100 to 20) in units of 0.01 dBm
Dwell time in range(1e-4 to 4295) in units of 1 µsec
'''
import pyvisa as visa

import functions_v1
from SourceFiles.lucid_cmd import LucidCmd
from SourceFiles.functions_v1 import Lucid_functions
import config


class ListRow:
	def __init__(self, frequency, power, last_entry, advance, dwell_time):
		self.step = 0
		self.frequency = frequency
		self.power = power
		self.last_entry = last_entry
		self.advance = advance
		self.dwell_time = dwell_time
		self.payload = bytearray(16)
		#print(step, frequency, power, last_entry, advance, dwell_time)
		
	def byte_converter(self,param,number_of_bytes,count):  #this function will do the conversion into bytes accoring to the sequence in manual
		mask = 255
		for i in range(number_of_bytes): #loop to get parameter into required sequence and number of bytes
			self.payload[count] = ((param >> 8*i) & mask)
			count = count+1  # index for payload
		return self.payload,count
	def get_bytes(self): #collecting all the paarmeter in 16 byte payload
		lastEntry_Advance = 0
		payload, count = self.byte_converter(self.step, 2, 0)
		payload, count = self.byte_converter(self.frequency, 6, count)
		payload, count = self.byte_converter(self.power, 2, count)
		if self.last_entry == 1:
			lastEntry_Advance = lastEntry_Advance | 1
		if self.advance == 1:
			lastEntry_Advance = lastEntry_Advance | 2
		payload, count = self.byte_converter(lastEntry_Advance, 1, count)
		payload, count = self.byte_converter(self.dwell_time, 5, count)
		return payload


class ListData:
    def __init__(self):
        self.list_rows = []
    def add_list_row(self, list_row): #add the lists defined by user
        list_row.step = len(self.list_rows) + 1
        self.list_rows.append(list_row)
    def count_rows(self): #count the number of list user has defined in main code
        return len(self.list_rows)

    def get_payload(self): #concatenate the payload of all the lists
        no_of_rows = self.count_rows()
        payload_all = bytes(0)
        for i in range(no_of_rows):
            payload_all=payload_all+(self.list_rows[i].get_bytes())
        return payload_all
    def get_header(self,payload_all): # build a header according to the payload and number of lists
        size_in_bytes = (len(payload_all))
        number_of_digits = len(str(size_in_bytes))
        header = "#"+str(number_of_digits)+str(size_in_bytes)
        header_bytes = bytes(header, 'ascii')
        return header_bytes
    def get_command(self):  #string command to bytes
        command_string = ":SOURCE:LIST:DATA "
        command_bytes = bytes(command_string, 'ascii')
        return command_bytes
    def get_end_string(selfself): # end string to bytes
        end_string = "\r\n"
        end_bytes = bytes(end_string, 'ascii')
        return end_bytes

    def get_full_scpi_command(self):
        payload_all = self.get_payload()
        command = self.get_command()  # command string
        end_bytes = self.get_end_string()  # end string \r\n termination string
        header = self.get_header(payload_all)  # header for scpi command
        full_command = bytes(command) + bytes(header) + bytes(payload_all) + bytes(end_bytes)  # adding all of them to create full command
        return full_command
    
    def send_scpi_command_byte(self,handle):
        response = ""

        try:
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(handle)
            # Need to define the termination string
            session.write_termination = '\n'
            session.read_termination = '\n'
            full_command = self.get_full_scpi_command()
            print("Command",full_command)
            session.write_raw(full_command)

            response = session.read()
            session.close()
        except Exception as e:
            print('[!] Exception: ' + str(e))
        return response


if __name__ == "__main__":
	handle = config.handle
	Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('ON'), handle)
	Lucid_functions.send_scpi_command(LucidCmd.LIST_ON, handle)
	Listsetup = ListData()
	list_row1 = ListRow(frequency=200*10**9,power=5 * 100,last_entry=0,advance=0,dwell_time=2000)
	Listsetup.add_list_row(list_row1)
	list_row2 = ListRow(frequency=100* 10**9,power=5 * 100,last_entry=1,advance=0,dwell_time=2000)
	Listsetup.add_list_row(list_row2)
	# list_row3 = ListRow(frequency=300 * 10 ** 3, power=5 * 100, last_entry=1, advance=1, dwell_time=200 * 10 **6)
	# Listsetup.add_list_row(list_row3)
	response = Listsetup.send_scpi_command_byte(config.handle)
	err=Lucid_functions.send_scpi_query(":SYST:ERR?", handle)
	print(err)
	for i in range(2):
		list_def = Lucid_functions.send_scpi_query(LucidCmd.LIST_DEF_Q.format(i+1), config.handle)
		print(list_def)
		Lucid_functions.send_scpi_command(LucidCmd.LIST_OFF, handle)
	Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('OFF'), handle)
	