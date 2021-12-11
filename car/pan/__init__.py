import time
from typing import Sequence

from car.pan.camera import Camera
from car.pan.gun import Gun
from car.pan.servo import Servo


class TagNotFoundError(Exception):
    pass


#
# class Pan():
#     def __del__(self):
#         pass


class Pan(Camera, Gun):
    def __init__(self):
        Camera.__init__(self)
        # Gun.__init__(self)
        self.v_servo: Servo = Servo(11)
        self.h_servo: Servo = Servo(12)
    
    def scan_tag(self, tag_id: int):
        if tag_id in self.auto_anal():
            return True
        for angle in range(30, 151, 30):
            self.h_servo.set_to(angle)
            result = self.auto_anal()
            if tag_id in result:
                return True
        raise TagNotFoundError
    
    def p_aim(self, tag_id: int):
        kp = -0.035
        try:
            bias = self.auto_anal()[tag_id]
        except KeyError:
            raise TagNotFoundError
        
        diff = kp * bias[0], kp * bias[1]
        return diff
    
    def aim(self, tag_id: int):
        self.scan_tag(tag_id)
        eps = 1, 1
        diff = 1000, 1000
        while diff[0] > eps[0] or diff[1] > eps[1]:
            diff = self.p_aim(tag_id)
            with self.h_servo.i_set(diff[0]),\
                    self.v_servo.i_set(diff[1]):
                time.sleep(0.5)
    
    def 摇摇乐(self):
        now = self.v_servo.angle
        for i in range(3):
            with self.v_servo.set(30):
                time.sleep(0.15)
            with self.v_servo.set(75):
                time.sleep(0.15)
        self.v_servo.set_to(now)
    
    # @staticmethod
    # def shooting(*args):
    #     return Gun().shooting(*args)
    #
    # @staticmethod
    # def shoot(*args):
    #     return Gun().shoot(*args)
    
    def brutal_shoot(self):
        """扫射"""
        self.摇摇乐()
        with self.shooting(65), self.v_servo.set(90):
            for i in range(60, 120, 5):
                self.h_servo.set_to(i)
            for i in range(120, 60, -5):
                self.h_servo.set_to(i)
    
    def precise_shoot(self, tag_id: int):
        self.aim(tag_id)
        self.摇摇乐()
        self.shoot(2)
    
    def smart_shoot(self, tag_ids: Sequence[int]):
        try:
            for i in tag_ids:
                self.precise_shoot(i)
        except TagNotFoundError:
            self.brutal_shoot()


if __name__ == '__main__':
    pan = Pan()
