"""底盘"""

import time
import keyboard

from serial import Serial, SerialException


class Chassis:
    def __init__(self):
        """串口初始化"""
        try:
            self.serial = Serial('/dev/ttyACM0', 9600)
        except SerialException:
            self.serial = None
            print('你妈的串口没插')
            exit(-1)
        print('串口初始化...')
        # 我猜时间和配置有关
        time.sleep(1.7)
    
    def __del__(self):
        if self.serial is not None:
            self.stop()
            self.serial.close()
    
    def _move(self, time_to_run, char: bytes):
        self.serial.write(char)
        time.sleep(time_to_run)
        self.serial.write(b' ')
        pass
    
    def front(self, distance_meter=0.5, fast=True):
        print(f'往前{distance_meter}米')
        secs_to_run_per_meter = 0.92 * (1 if fast else 4)
        time_to_run = distance_meter * secs_to_run_per_meter
        if distance_meter > 0.5:
            self.front(distance_meter - 0.5)
        self._move(time_to_run, b'W' if fast else b'w')
        time.sleep(1)
    
    def back(self, distance_meter=0.5, fast=True):
        secs_to_run_per_meter = 0.9 * (1 if fast else 4)
        if distance_meter > 0.5:
            # self.left(4)
            self.back(distance_meter - 0.5)
        
        # self.left(5 * distance_meter)
        time_to_run = distance_meter * secs_to_run_per_meter
        self._move(time_to_run, b'S' if fast else b's')
        time.sleep(1)
    
    def left(self, angle_degree=90., fast=True):
        sec_to_run_per_degree = 0.0046 * (1 if fast else 4)
        time_to_run = angle_degree * sec_to_run_per_degree
        self._move(time_to_run, b'A' if fast else b'a')
    
    def right(self, angle_degree=90., fast=True):
        sec_to_run_per_degree = 0.0048 * (1 if fast else 4)
        time_to_run = angle_degree * sec_to_run_per_degree
        self._move(time_to_run, b'D' if fast else b'd')
    
    def stop(self):
        self.serial.write(b' ')


if __name__ == '__main__':
    chassis = Chassis()
    time.sleep(2)
    # chassis.front(1)
    print('等待输入')
    while True:
        key = input()
        
        if key == 'w':
            print('w')
            chassis.front(0.2, fast=False)
        elif key == 'a':
            print('a')
            chassis.left(10, fast=False)
        elif key == 's':
            print('s')
            chassis.back(0.2, fast=False)
        elif key == 'd':
            print('d')
            chassis.right(10, fast=False)
        elif key == 'q':
            print('q')
            break
        time.sleep(1)
