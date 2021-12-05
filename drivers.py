import os
import time

import apriltag
import cv2
import RPi.GPIO as GPIO
from apriltag import Detector
from typing import List

GPIO.setmode(GPIO.BOARD)


# 电机
class Motor:
    def __init__(self, pin):
        self.ping = pin
    
    def start_rotate(self):
        """设置正车"""
        # TODO
        pass
    
    def start_rotate_reverse(self):
        """设置倒车"""
        pass
    
    def stop_rotate(self):
        """设置停车"""
        pass


# 舵机
class Servo:
    angle_now: int
    
    def __init__(self, pin, min_degree, min_ratio, max_degree, max_ratio):
        self.__pin = pin
        # 最小角度和此时 pwm 占空比时间
        self.__min_degree = min_degree
        self.__min_ratio = min_ratio
        # 最大角度和此时 pwm 占空比时间
        self.__max_degree = max_degree
        self.__max_ratio = max_ratio
        self.__degree_range = self.__max_degree - self.__min_degree
        self.__ratio_range = self.__max_ratio - self.__min_ratio
    
    def set(self, angle: int):
        pwm = GPIO.PWM(self.__pin, 50)
        
        duty_ratio = (angle - self.__min_degree) / self.__degree_range * self.__ratio_range + self.__min_ratio
        pwm.start(duty_ratio)
        time.sleep(1)
        pwm.stop()
        return angle
    
    def get(self):
        return self.angle_now


# 水弹枪
class Gun:
    # 水弹枪控制针脚
    __gun_pin = 7
    
    def auto_shoot(self, secs):
        GPIO.output(self.__gun_pin, GPIO.HIGH)
        time.sleep(secs)
        GPIO.output(self.__gun_pin, GPIO.LOW)


class Camera:
    def __init__(self):
        self.__detector = Detector()
    
    # 拍照
    @staticmethod
    def __get_photo():
        os.system('libcamera-jpeg -o tmp.jpg')
        return cv2.imread('tmp.jpg', cv2.IMREAD_GRAYSCALE)
    
    def __anal_photo(self) -> dict:
        img = self.__get_photo()
        result: List[apriltag.Detection] = self.__detector.detect(img=img)
        
        if result:
            img_center = (i / 2 for i in img.shape)
            return {i.tag_id: (res - img for img, res in zip(img_center, i.center))
                    for i in result}
        return {}


# 底盘
class Chassis:
    def __init__(self):
        """
        电机控制使用 35-38 针脚
        按照顺序分别为左前右前左后右后
        """
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
    def __init__(self, horizontal_servo, vertical_servo):
        # 水平和垂直方向的舵机
        super().__init__()
        self.__h_servo: Servo = horizontal_servo
        self.__v_servo: Servo = vertical_servo
    
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
