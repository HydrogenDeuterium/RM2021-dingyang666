"""
预赛脚本
"""
import time

from controller import Car

tag_seq = [1, 2, 3, 4]

if __name__ == "__main__":
    car = Car()
    print('电机测试')
    car.front(0.5)
    car.back(0.5)
    car.left(90)
    car.right(90)
    time.sleep(1)
    print('舵机测试')
    car.pan.h_servo.set(60)
    car.pan.h_servo.set(120)
    car.pan.v_servo.set(60)
    car.pan.v_servo.set(120)
    car.pan.v_servo.set(90)
    car.auto_shoot()
    car.pan.scan_shoot()
    print('done')
