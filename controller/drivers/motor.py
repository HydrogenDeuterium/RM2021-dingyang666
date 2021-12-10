"""此文件已经废弃"""
from RPi import GPIO


class Motor:
    def __init__(self, pin1, pin2, ratio_duty=100):
        """正转针脚，倒转针脚，pwm修正率(%)"""
        GPIO.setup(pin2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)
        self.pin1 = pin1
        self.pin2 = pin2
    
    def start_rotate(self):
        """设置正车"""
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.LOW)
    
    def start_rotate_reverse(self):
        """设置倒车"""
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.HIGH)
    
    def stop_rotate(self):
        """设置停车"""
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
