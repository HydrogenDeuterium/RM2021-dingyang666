"""
预赛脚本
"""
from controller import Car

tag_seq = [1, 2, 3, 4]

if __name__ == "__main__":
    car = Car()
    car.front(0.5)
    car.back(0.5)
    car.left(90)
    car.right(90)
    car.pan.h_servo.set(60)
    car.pan.h_servo.set(120)
    car.pan.v_servo.set(60)
    car.pan.v_servo.set(120)
    car.auto_shoot()
    print('done')
