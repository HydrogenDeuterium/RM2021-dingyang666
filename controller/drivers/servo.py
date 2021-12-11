import contextlib
import time

from RPi import GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Servo:
    
    def __init__(self, pin, range_=(0, 15)):
        self.pin = pin
        self.range = range_
        
        GPIO.setup(self.pin, GPIO.OUT)
        # 舵机位置初始化
        self.angle = 90
        self.set_to(90)
    
    def __del__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)
    
    @contextlib.contextmanager
    def set(self, angle: int):
        assert self.range[0] < self.range[1]
        target = 3 + angle * 0.05
        # print('开始pwm')
        pwm = GPIO.PWM(self.pin, 50)
        pwm.start(target)
        yield
        
        self.angle = angle
        pwm.stop()
        return angle
    
    def set_to(self, angle):
        with self.set(angle):
            time.sleep(abs(angle - self.angle) / 250 + 0.1)
    
    @contextlib.contextmanager
    def i_set(self, diff_angle):
        with self.set(self.angle + diff_angle):
            yield
        return
    
    def get(self):
        return self.angle


if __name__ == '__main__':
    servo_v = Servo(11, range_=(1.75, 11.75))
    servo_h = Servo(12, range_=(1.75, 11.75))
    servo = servo_h
    with servo_v.set(90):
        time.sleep(0.5)
    with servo_h.set(90):
        time.sleep(0.5)
    
    # for i in range(75-45, 75+45, 3):
    #     print(f'Set to {i / 10}')
    #     with servo_v.setPWM(i / 10):
    #         time.sleep(1)
    #     # time.sleep(1)
    
    # with servo_h.setPWM(3):
    #     time.sleep(0.46)
    # with servo_h.setPWM(12):
    #     time.sleep(0.5)
    
    print('Done')
