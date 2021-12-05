import time

from RPi import GPIO as GPIO


class Gun:
    # 水弹枪控制针脚
    __gun_pin = 7
    
    def auto_shoot(self, secs):
        GPIO.output(self.__gun_pin, GPIO.HIGH)
        time.sleep(secs)
        GPIO.output(self.__gun_pin, GPIO.LOW)