'''
SCPI command format- :SOURCE:PATTERN:DATA {#< header><binary block>}
#Description:-
-This command will download pattern data to the Lucid unit. Pattern data is loaded to the Lucid unit using high-speed binary data transfer. High-speed binary data transfer allows any number of 8-bit bytes to be transmitted in a message.
-This command is particularly useful for sending large quantities of data.

#Example:-
-The command will download to the generator a block of pattern-related data of 40 entries:

        :SOURCE:PATTERN:DATA#3640<binary_block>

-This command causes the transfer of 640 bytes of data (32 pattern entries).
-The <header> is interpreted this way:
• The ASCII "#" ($23) designates the start of the binary data block.
• "3" designates the number of digits that follow representing the binary data block size in bytes.
• "800" is the number of bytes to follow.
-The <binary_block> represents pattern-related data.
Each entry in the pattern is represented by 20 bytes
#User information :-
- In order to download pattern to the LUCID X device, user is supposed to provide the paramer in following format

pattern_row<n> = PatternRow(no_of_repetition=25, offtime=35, ontime=15)
Patternsetup.add_pattern_row(pattern_row<n>)

#Note- This script will follow the sequence for step in the same order as they are defined here, and can download upto 2048 such Patterns

##Parameter Range

Repetition - 0 to 65535
Ontime - 3.2e-8 to 1.8e6 (dhould be in units of 1ns)
Offtime - 3.2e-8 to 1.8e6 (dhould be in units of 1ns)

'''

import pyvisa as visa
# from functions_v1 import Lucid_functions
from  lucid_cmd import LucidCmd
from functions_v1 import Lucid_functions
import config
class PatternRow:
    def __init__(self, no_of_repetition, offtime, ontime):
        self.step = 0
        self.no_of_repetition = no_of_repetition
        self.offtime = offtime
        self.ontime = ontime
        self.payload = bytearray(20)

    def byte_converter(self, param, number_of_bytes,
                       count):  # this function will do the conversion into bytes accoring to the sequence in manual
        mask = 255
        for i in range(number_of_bytes):  # loop to get parameter into required sequence and number of bytes
            self.payload[count] = ((param >> 8 * i) & mask)
            count = count + 1  # index for payload
        return self.payload, count

    def get_bytes(self):  # collecting all the paarmeter in 16 byte payload
        lastEntry_Advance = 0
        payload, count = self.byte_converter(self.step, 2, 0)
        payload, count = self.byte_converter(self.no_of_repetition, 2, count)
        payload, count = self.byte_converter(self.offtime, 8, count)
        payload, count = self.byte_converter(self.ontime, 8, count)
        return payload


class PatternData:
    def __init__(self):
        self.pattern_rows = []

    def add_pattern_row(self, pattern_row):  # add the patterns defined by user
        pattern_row.step = len(self.pattern_rows) + 1
        self.pattern_rows.append(pattern_row)

    def count_rows(self):  # count the number of pattern user has defined in main code
        return len(self.pattern_rows)

    def get_payload(self):  # concatenate the payload of all the patterns
        no_of_rows = self.count_rows()
        payload_all = bytes(0)
        for i in range(no_of_rows):
            payload_all = payload_all + (self.pattern_rows[i].get_bytes())
        return payload_all

    def get_header(self, payload_all):  # build a header according to the payload and number of patterns
        size_in_bytes = (len(payload_all))
        number_of_digits = len(str(size_in_bytes))
        header = "#" + str(number_of_digits) + str(size_in_bytes)
        header_bytes = bytes(header, 'ascii')
        return header_bytes

    def get_command(self):  # string command to bytes
        command_string = ":SOURCE:PATTERN:DATA "
        command_bytes = bytes(command_string, 'ascii')
        return command_bytes

    def get_end_string(self):  # end string to bytes
        end_string = "\n\r"
        end_bytes = bytes(end_string, 'ascii')
        return end_bytes

    def get_full_scpi_command(self):
        payload_all = self.get_payload()
        command = self.get_command()  # command string
        end_bytes = self.get_end_string()  # end string \r\n termination string
        header = self.get_header(payload_all)  # header for scpi command
        full_command = bytes(command) + bytes(header) + bytes(payload_all) + bytes(
            end_bytes)  # adding all of them to create full command
        return full_command

    def send_scpi_command_byte(self,handle):
        response = ""

        try:
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(handle)
            # Need to define the termination string
            session.write_termination = '\n'
            session.read_termination = '\n'
            full_command =self.get_full_scpi_command()
            print("Command", full_command)
            session.write_raw(full_command)

            response = session.read()
            session.close()
        except Exception as e:
            print('[!] Exception: ' + str(e))
        return response

if __name__ == "__main__":
    handle = config.handle
    Patternsetup = PatternData()
    pattern_row = PatternRow(no_of_repetition=1, offtime=100 * 10 ** 3,ontime=100 * 10 ** 3)
    Patternsetup.add_pattern_row(pattern_row)
    response = Patternsetup.send_scpi_command_byte(handle)
    Lucid_functions.send_scpi_command(LucidCmd.OUTP.format('ON'), handle)
    Lucid_functions.send_scpi_command(LucidCmd.PATTERN_ON, handle)
    patt_def = Lucid_functions.send_scpi_query(LucidCmd.PATTERN_DEF_Q.format(1), handle)
    print(patt_def)
