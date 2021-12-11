import contextlib
import time

from RPi import GPIO

GPIO.setmode(GPIO.BOARD)


class Gun:
    # 水弹枪控制针脚
    __gun_pin = 7
    
    def __init__(self):
        GPIO.setup(self.__gun_pin, GPIO.OUT)
    
    def __del__(self):
        GPIO.setup(self.__gun_pin, GPIO.IN)
    
    @contextlib.contextmanager
    def shooting(self, power: int):
        assert 0 < power < 100
        pwm = GPIO.PWM(self.__gun_pin, 50)
        pwm.start(power)
        yield
        pwm.stop()
    
    def shoot(self, secs=2.0):
        with self.shooting(power=65):
            time.sleep(secs)


if __name__ == '__main__':
    print('开始射')
    Gun().shoot(10)
    print('射完了')
