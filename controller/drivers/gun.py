import time

from RPi import GPIO

GPIO.setmode(GPIO.BOARD)


class Gun:
    # 水弹枪控制针脚
    __gun_pin = 7
    
    def __init__(self):
        self.pwm = None
        GPIO.setup(self.__gun_pin, GPIO.OUT)
    
    def auto_shoot(self, secs):
        # GPIO.output(self.__gun_pin, GPIO.HIGH)
        pwm = GPIO.PWM(self.__gun_pin, 50)
        pwm.start(65)
        time.sleep(secs)
        # GPIO.output(self.__gun_pin, GPIO.LOW)
        pwm.stop()
    
    def start_shoot(self):
        self.pwm = GPIO.PWM(self.__gun_pin, 50)
        self.pwm.start(90)
    
    def stop_shoot(self):
        self.pwm.stop()


if __name__ == '__main__':
    print('开始射')
    Gun().auto_shoot(2.5)
    print('射完了')
