"""底盘"""

import time

from serial import Serial


class Chassis:
    def __init__(self):
        """串口初始化"""
        self.serial = Serial('/dev/serial0', 9600)
    
    def go(self, distance_meter):
        secs_to_run_per_meter = 3
        time_to_run = distance_meter * secs_to_run_per_meter
        self.serial.write('F')
        time.sleep(time_to_run)
        self.serial.write('S')
    
    def back(self, distance_meter):
        secs_to_run_per_meter = 3
        time_to_run = distance_meter * secs_to_run_per_meter
        self.serial.write('B')
        time.sleep(time_to_run)
        self.serial.write('S')
    
    def left(self, angle_degree=90):
        sec_to_run_per_degree = 0.05
        time_to_run = angle_degree * sec_to_run_per_degree
        
        self.serial.write('L')
        time.sleep(time_to_run)
        self.serial.write('S')
    
    def right(self, angle_degree=90):
        sec_to_run_per_degree = 0.05
        time_to_run = angle_degree * sec_to_run_per_degree
        
        self.serial.write('R')
        time.sleep(time_to_run)
        self.serial.write('S')


if __name__ == '__main__':
    pass
