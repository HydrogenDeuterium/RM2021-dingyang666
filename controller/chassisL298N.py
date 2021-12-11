"""底盘,此文件已废弃"""

import time

from typing import List

from drivers.motor import Motor


class Chassis:
    def __init__(self):
        """
        电机控制使用针脚
        按照顺序分别为左前右前左后右后
        """
        self.__motor1 = Motor(29, 31)
        self.__motor2 = Motor(32, 36)
        self.__motor3 = Motor(33, 35)
        self.__motor4 = Motor(38, 40)
        
        self.__motors: List[Motor] = [self.__motor1, self.__motor2, self.__motor3, self.__motor4]
    
    def go(self, distance_meter):
        secs_to_run_per_meter = 3
        time_to_run = distance_meter * secs_to_run_per_meter
        [motor.start_rotate() for motor in self.__motors]
        time.sleep(time_to_run)
        [motor.stop_rotate() for motor in self.__motors]
    
    def back(self, distance_meter):
        secs_to_run_per_meter = 3
        time_to_run = distance_meter * secs_to_run_per_meter
        [motor.start_rotate_reverse() for motor in self.__motors]
        time.sleep(time_to_run)
        [motor.stop_rotate() for motor in self.__motors]
    
    def left(self, angle_degree=90):
        sec_to_run_per_degree = 0.05
        
        self.__motor1.start_rotate_reverse()
        self.__motor3.start_rotate_reverse()
        self.__motor2.start_rotate()
        self.__motor4.start_rotate()
        
        time.sleep(angle_degree * sec_to_run_per_degree)
        
        [motor.stop_rotate() for motor in self.__motors]
    
    def right(self, degree=90):
        ms_to_run_per_meter = 0.05
        
        self.__motor1.start_rotate()
        self.__motor3.start_rotate()
        self.__motor2.start_rotate_reverse()
        self.__motor4.start_rotate_reverse()
        
        time.sleep(degree * ms_to_run_per_meter)
        
        [motor.stop_rotate() for motor in self.__motors]
