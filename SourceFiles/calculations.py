import pyvisa as visa
import time
import config
from SourceFiles.lucid_cmd import LucidCmd
class ErrorCalculation(object):
    def __init__(self,handle):
        handle = self.handle

    def abs_error_difference(output,reference):
        error_value = abs(output-reference)
        return error_value
    def percent_error(output,reference):
        error_value = ErrorCalculation.abs_error_difference(output,reference)
        error_in_percent = error_value/reference
        return error_in_percent

    def final_result(error,threshold):
        test_result = "pass"
        if error<= threshold:
            test_result = "Pass"
            print(test_result)
        else:
            test_result = "Fail"
            print(test_result)

