import time

from RPi import GPIO

GPIO.setmode(GPIO.BOARD)


class Gun:
    # 水弹枪控制针脚
    __gun_pin = 7
    
    def __init__(self):
        GPIO.setup(self.__gun_pin, GPIO.OUT)
    
    def auto_shoot(self, secs):
        GPIO.output(self.__gun_pin, GPIO.HIGH)
        time.sleep(secs)
        GPIO.output(self.__gun_pin, GPIO.LOW)


if __name__ == '__main__':
    print('开始射')
    Gun().auto_shoot(3)
    print('射完了')
