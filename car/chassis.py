"""底盘"""

import time

from serial import Serial, SerialException


class Chassis(Serial):
    def __init__(self):
        """串口初始化"""
        try:
            Serial.__init__(self, '/dev/ttyACM0', 9600)
        except SerialException as e:
            print('你妈的串口没插')
            raise e
        print('串口初始化...')
        # 我猜时间和配置有关
        time.sleep(1.7)
    
    def __del__(self):
        try:
            self.close()
        except AttributeError:
            pass
    
    def stop(self):
        self.write(b' ')
    
    def _move(self, time_to_run, char: bytes):
        self.write(char)
        time.sleep(time_to_run)
        self.stop()
    
    def front(self, distance_meter=0.5, fast=True):
        secs_to_run_per_meter = 0.92 * (1 if fast else 4)
        if distance_meter > 0.5:
            distance_meter -= 0.5
            self.front(distance_meter)
        time_to_run = distance_meter * secs_to_run_per_meter
        self._move(time_to_run, b'W' if fast else b'w')
        time.sleep(1)
    
    def back(self, distance_meter=0.5, fast=True):
        secs_to_run_per_meter = 0.9 * (1 if fast else 4)
        if distance_meter > 0.5:
            distance_meter -= 0.5
            self.back(distance_meter)
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


if __name__ == '__main__':
    chassis = Chassis()
    # chassis.front(1)
    print('初始化完成，等待输入')
    while True:
        key = input()
        if key == 'W':
            chassis.front(0.5)
        elif key == 'w':
            chassis.front(0.15, fast=False)
        elif key == 'A':
            chassis.left(90)
        elif key == 'a':
            chassis.left(20, fast=False)
        elif key == 'S':
            chassis.back(0.5)
        elif key == 's':
            chassis.back(0.15, fast=False)
        elif key == 'D':
            chassis.right(90)
        elif key == 'd':
            chassis.right(20, fast=False)
        elif key == 'q':
            break
        time.sleep(1)
