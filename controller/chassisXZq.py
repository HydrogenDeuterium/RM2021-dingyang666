"""底盘"""

import time

from serial import Serial


class Chassis:
    def __init__(self):
        """串口初始化"""
        self.serial = Serial('/dev/ttyACM0', 9600)
        print('等待串口初始化')
        # 我猜时间和配置有关
        time.sleep(1.7)
        # print('等完了 开始跑')
    
    def __del__(self):
        self.serial.close()
    
    def move(self, time_to_run, char: bytes):
        self.serial.write(char)
        time.sleep(time_to_run)
        self.serial.write(b' ')
        pass

    def front(self, distance_meter):
        secs_to_run_per_meter = 3.6
        time_to_run = distance_meter * secs_to_run_per_meter
        while(time_to_run>secs_to_run_per_meter):
            self.left(5)
            self.move(secs_to_run_per_meter,b'S')
            time_to_run-=secs_to_run_per_meter

        self.left(3*distance_meter)
        self.move(time_to_run, b'S')
    
    def back(self, distance_meter):
        secs_to_run_per_meter = 3.5
        time_to_run = distance_meter * secs_to_run_per_meter
        self.move(time_to_run, b'W')
    
    def left(self, angle_degree=90):
        sec_to_run_per_degree = 0.03
        time_to_run = angle_degree * sec_to_run_per_degree
        self.move(time_to_run, b'A')
    
    def right(self, angle_degree=90):
        sec_to_run_per_degree = 0.028
        time_to_run = angle_degree * sec_to_run_per_degree
        self.move(time_to_run, b'D')

    def stop():
        self.serial.write(b' ')

if __name__ == '__main__':
    chassis = Chassis()
    # chassis.front(0.5)
    # chassis.left(90)
    chassis.right(90)
    print('跑完了')
