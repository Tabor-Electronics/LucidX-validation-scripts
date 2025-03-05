import pyvisa as visa
import time

from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd


class Print_function(object):
	def __init__(self, handle):
		handle = self.handle
	def print_freq_pow_to_gui(freq=1e9, freq__dev_p=0.000, freq_dev_n=0.000, pow=5, power_dev_p=0.000,
	                          power_dev_n=0.000):
		print("<TOGUI>freq={0}::p{1}::n{2},pow={3}::p{4}::n{5}</TOGUI>".format(freq, freq__dev_p, freq_dev_n, pow,power_dev_p, power_dev_n))
	
	def print_to_user(msg='Hi User'):
		print("<TOUSER>" + msg + "</TOUSER>")


class Description(object):
	def __init__(self, description_text):
		self.description_text = description_text
	
	def set_description(self, description_text):
		self.description_text = description_text
	
	def get_description(self):
		return self.description_text
	
	def clear_description(self):
		self.set_description('')
	
	def print_description(self):
		print(f'<DESCRIPTION>{self.get_description()}</DESCRIPTION>')


class _MessageToUser(object):
	def __init__(self, message_to_user):
		self.message_to_user = message_to_user
	
	def set(self, message_to_user):
		self.message_to_user = message_to_user
	
	def get(self):
		return self.message_to_user
	
	def clear(self):
		self.set('')
	
	def print(self):
		if self.get() != '':
			print(f'<TOUSER>{self.get()}</TOUSER>', end='')


class _MessageToGui(object):
	def __init__(self, message_to_gui):
		self.message_to_gui = message_to_gui
	
	def set(self, message_to_gui):
		self.message_to_gui = message_to_gui
	
	def get(self):
		return self.message_to_gui
	
	def clear(self):
		self.set('')
	
	def print(self):
		if self.get() != '':
			print(f'<TOGUI>{self.get()}</TOGUI>', end='')


class _Cmd(object):
	def __init(self, cmd_text):
		self.cmd_text = cmd_text
	
	def set(self, cmd_text):
		self.cmd_text = cmd_text
	
	def get(self):
		return self.cmd_text
	
	def clear(self):
		self.set('')
	
	def print(self):
		if self.get() != '':
			print(f'<CMD>{self.get()}</CMD>', end='')


class _Resp(object):
	def __init(self, resp_text):
		self.resp_text = resp_text
	
	def set(self, resp_text):
		self.resp_text = resp_text
	
	def get(self):
		return self.resp_text
	
	def clear(self):
		self.set('')
	
	def print(self):
		if self.get() != '':
			print(f'<RESPONSE>{self.get()}</RESPONSE>', end='')


class DevicePrint(object):
	def __init__(self, print_type=0, cmd_text='', response_text='', message_to_user='', message_to_gui=''):
		self.print_type = print_type
		self.cmd = _Cmd(cmd_text)
		self.resp = _Resp(response_text)
		self.msg_user = _MessageToUser(message_to_user)
		self.msg_gui = _MessageToGui(message_to_gui)
	
	def Print(self):
		if self.print_type == 0:
			print('<DEVICECMD>', end='')
			self.cmd.print()
			self.msg_user.print()
			self.msg_gui.print()
			print('</DEVICECMD>', end='')
		
		elif self.print_type == 1:
			print('<DEVICERESPONSE>', end='')
			self.resp.print()
			self.msg_user.print()
			self.msg_gui.print()
			print('</DEVICERESPONSE>', end='')
		
		self.cmd.clear()
		self.resp.clear()
		self.msg_gui.clear()
		self.msg_user.clear()
