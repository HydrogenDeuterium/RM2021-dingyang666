"""底盘"""

import time

from typing import List

from drivers import Motor


class Chassis:
    def __init__(self):
        """
        电机控制使用 35-38 针脚
        按照顺序分别为左前右前左后右后
        """
        # TODO 电机要两根针脚控制
        self.__motor1 = Motor(35)
        self.__motor2 = Motor(36)
        self.__motor3 = Motor(37)
        self.__motor4 = Motor(38)
        
        self.__motors: List[Motor] = [self.__motor1, self.__motor2, self.__motor3, self.__motor4]
    
    def go(self, distance):
        ms_to_run_per_meter = 1000
        [motor.start_rotate() for motor in self.__motors]
        time.sleep(distance * ms_to_run_per_meter)
        [motor.stop_rotate() for motor in self.__motors]
    
    def back(self, distance):
        ms_to_run_per_meter = 1000
        [motor.start_rotate_reverse() for motor in self.__motors]
        time.sleep(distance * ms_to_run_per_meter)
        [motor.stop_rotate() for motor in self.__motors]
        pass
    
    def left(self, degree=90):
        ms_to_run_per_meter = 10
        
        self.__motor1.start_rotate_reverse()
        self.__motor2.start_rotate()
        self.__motor3.start_rotate_reverse()
        self.__motor4.start_rotate()
        
        time.sleep(degree * ms_to_run_per_meter)
        
        [motor.stop_rotate() for motor in self.__motors]
        pass
    
    def right(self, degree=90):
        ms_to_run_per_meter = 10
        
        self.__motor1.start_rotate()
        self.__motor2.start_rotate_reverse()
        self.__motor3.start_rotate()
        self.__motor4.start_rotate_reverse()
        
        time.sleep(degree * ms_to_run_per_meter)
        
        [motor.stop_rotate() for motor in self.__motors]
        pass
    
    pass
