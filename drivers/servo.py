import time

from RPi import GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Servo:
    angle_now: int
    
    def __init__(self, pin, min_degree=0, min_ratio=0.05, max_degree=180, max_ratio=0.1):
        self.__pin = pin
        GPIO.setup(self.__pin, GPIO.OUT)
        
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
        print('开始pwm')
        pwm.start(duty_ratio)
        time.sleep(1)
        pwm.stop()
        print('结束pwm')
        self.angle_now = angle
        return angle
    
    def get(self):
        return self.angle_now


if __name__ == '__main__':
    servo_v = Servo(12, min_ratio=2, max_ratio=12.5)
    
    for i in range(0, 182, 5):
        print(f'Set to {i}')
        servo_v.set(i)
        time.sleep(1)
    
    print('Done')
