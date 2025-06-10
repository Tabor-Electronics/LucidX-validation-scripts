import pyvisa as visa
import time
import numpy as np
from SourceFiles import config
from SourceFiles.lucid_cmd import LucidCmd
from SourceFiles.for_the_gui import DevicePrint

devicePrintCmd = DevicePrint()
devicePrintResp = DevicePrint(print_type=1)

class ErrorCalculation(object):
    def __init__(self, handle):
        self.handle = handle

    @staticmethod
    def abs_error_difference(output, reference):
        return abs(output - reference)

    @staticmethod
    def percent_error(output, reference):
        error_value = ErrorCalculation.abs_error_difference(output, reference)
        return error_value / reference

    @staticmethod
    def final_result(error, threshold):
        test_result = "Pass" if error <= threshold else "Fail"
        #print(test_result)
        return test_result


class SweepCalculations:
    @staticmethod
    def get_edges(trace, threshold):
        try:
            
            is_on = trace > threshold
            transitions = np.diff(is_on.astype(int))
    
            # Detect rising and falling edges
            rising_edges = np.where(transitions == 1)[0]
            falling_edges = np.where(transitions == -1)[0]
    
            # Align edges
            if len(falling_edges) > 0 and falling_edges[0] < rising_edges[0]:
                falling_edges = falling_edges[1:]
            if len(rising_edges) > len(falling_edges):
                rising_edges = rising_edges[:len(falling_edges)]
    
            return rising_edges, falling_edges
        except Exception as e:
            rising_edges = 0
            falling_edges = 0
            devicePrintCmd.msg_user.set('Error in getting the on off time')
            devicePrintCmd.Print()
            return rising_edges, falling_edges

    @staticmethod
    def get_averaged_on_off(rising_edges, falling_edges, sweep_time, sweep_pts):
        max_ton=0
        max_toff=0
        try:
            from collections import Counter
            pulse_time_on = []
            pulse_time_off = []
            pulse_data= []
            time_axis = np.linspace(0, sweep_time, sweep_pts)
    
            for i in range(len(rising_edges)):
                ton_start = time_axis[rising_edges[i]]
                ton_end = time_axis[falling_edges[i]]
                ton = ton_end - ton_start
    
                if i < len(rising_edges) - 1:
                    toff = time_axis[rising_edges[i + 1]] - ton_end
                else:
                    toff = sweep_time - ton_end
                pulse_data.append((i + 1, ton * 1000, toff * 1000))  # in ms
                if ton > 1:
                    pulse_time_on.append(ton * 1000)  # Convert to ms
                if toff > 1:
                    pulse_time_off.append(toff * 1000)  # Convert to ms
    
            # Remove first/last edge if needed for alignment
            # if len(pulse_time_on) > 1:
            #     pulse_time_on = pulse_time_on[1:]
            # if len(pulse_time_off) > 1:
            #     pulse_time_off = pulse_time_off[:-1]
    
            # average_on = np.mean(pulse_time_on)
            # average_off = np.mean(pulse_time_off)
            # print("\n📊 Pulse Report (ms):")
            # print("Pulse#   Ton(ms)   Toff(ms)")
            # for p in pulse_data:
            #     print(f"{p[0]:>6}   {p[1]:>7.2f}   {p[2]:>8.2f}")
            # print('\nAverage On-Time (ms):', average_on)
            # print('Average Off-Time (ms):', average_off)
            # print()
            
            
            
            # Ignore first and last pulse data
            if len(pulse_data) > 2:
                filtered_pulse_data = pulse_data[1:-1]
            else:
                filtered_pulse_data = pulse_data
            
            # Find repeated values for Ton (p[1]) and Toff (p[2])
            ton_values = [p[1] for p in filtered_pulse_data]
            toff_values = [p[2] for p in filtered_pulse_data]
            
            # Count frequencies (rounded to 2 decimal places)
            ton_counts = Counter(round(ton, 2) for ton in ton_values)
            toff_counts = Counter(round(toff, 2) for toff in toff_values)
            
            # Filter repeated ones
            repeated_ton_values = {ton: count for ton, count in ton_counts.items() if count > 1}
            repeated_toff_values = {toff: count for toff, count in toff_counts.items() if count > 1}
            
            # If there are multiple repeated values, keep only the max one
            if repeated_ton_values:
                max_ton = max(repeated_ton_values)
                repeated_ton_values = {max_ton: repeated_ton_values[max_ton]}
            
            if repeated_toff_values:
                max_toff = max(repeated_toff_values)
                repeated_toff_values = {max_toff: repeated_toff_values[max_toff]}
                
                #print(f"Max Ton: {max_ton}")
                #print(f"Max Toff: {max_toff}")
        
            # Print filtered pulse data
            #print("\n📊 Filtered Pulse Report (ms):")
            #print("Pulse#   Ton(ms)   Toff(ms)")
            for p in filtered_pulse_data:
                print(f"{p[0]:>6}   {p[1]:>7.2f}   {p[2]:>8.2f}")
            #
            # # Print repeated Ton and Toff values
            # print("\n📊 Repeated Ton values:")
            # for ton, count in repeated_ton_values.items():
                #     print(f"Ton = {ton:.2f} ms, Repeated {count} times")
                #
                # print("\n📊 Repeated Toff values:")
                # for toff, count in repeated_toff_values.items():
                #     print(f"Toff = {toff:.2f} ms, Repeated {count} times")
            
        except Exception as e:
            devicePrintCmd.msg_user.set('Error in getting the on off time')
            devicePrintCmd.Print()
        return float(max_ton), float(max_toff)

    
