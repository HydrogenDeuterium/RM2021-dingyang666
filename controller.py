import time

import RPi.GPIO as GPIO
from typing import List

from drivers.camera import Camera
from drivers.gun import Gun
from drivers.Motor import Motor
from drivers.servo import Servo

GPIO.setmode(GPIO.BOARD)

print('import finisheds')


# 底盘
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


# 云台
class Pan(Gun, Camera):
    def __init__(self):
        # 水平和垂直方向的舵机
        super().__init__()
        self.__h_servo: Servo = Servo(12, min_ratio=2, max_ratio=12.5)
        self.__v_servo: Servo = Servo(11, min_ratio=5, max_ratio=15)
    
    # 默认射击
    def __shoot(self, tags):
        for i in tags:
            self.__pid_aim(i)
            self.auto_shoot(5)
    
    # 水平方向角度调整
    def __horizontal(self, angle=None):
        if angle:
            return self.__h_servo.set(angle)
        return self.__h_servo.get()
    
    # 水平方向角度
    def __vertical(self, angle=None):
        if angle:
            return self.__v_servo.set(angle)
        return self.__v_servo.get()
    
    # 搜索目标
    def __scan_target(self, target_id):
        for l_angle in range(-90, 90, 30):
            location_map = self.__anal_photo()
            if target_id in location_map:
                return
    
    def __pid_aim(self, tag_id):
        self.__scan_target(tag_id)
        integrate = 0., 0.
        last = 0., 0.
        kp, ki, kd = 0.7, 0.01, 0.01
        
        # 瞄准范围
        eps = 25
        
        bias = self.__anal_photo()[tag_id]
        # 到达瞄准范围后则不再瞄准
        while bias[0] < eps and bias[1] < eps:
            # 计算积分常量
            integrate[0] += bias[0]
            integrate[1] += bias[1]
            # 计算调整值
            diff = (
                kp * bias[0] + ki * integrate[0] + (bias[0] - last[0]) * kd,
                kp * bias[1] + ki * integrate[1] + (bias[1] - last[1]) * kd
            )
            # 调整舵机
            self.__h_servo.set(self.__h_servo.get() + diff[0])
            self.__v_servo.set(self.__v_servo.get() + diff[1])
            # 保存微分常量
            last = bias
            # 获取调整后的结果
            bias = self.__anal_photo()[tag_id]


class Car(Chassis, Pan):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    print('Hello!')
    
    # Camera
    # t0=time.time_ns()
    # camera: Camera = Camera()
    # for i in range(100):
    #     print(camera._Camera__anal_photo())
    # t=time.time_ns()
    # print(f'100次识别总用时 {(t-t0)/1e9} 秒。\n识别速率：{100/(t-t0)*1e9} Hz')
    
