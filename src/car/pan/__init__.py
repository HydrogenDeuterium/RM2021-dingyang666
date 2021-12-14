import time
from typing import Sequence

from src.car.pan.camera import Camera
from src.car.pan.gun import Gun
from src.car.pan.servo import Servo


class TagNotFoundError(Exception):
    pass


#
# class Pan():
#     def __del__(self):
#         pass


class Pan(Camera, Gun):
    def __init__(self):
        Camera.__init__(self)
        Gun.__init__(self)
        self.v_servo: Servo = Servo(11)
        self.h_servo: Servo = Servo(12)
    
    def scan_tag(self, tag_id: int):
        if tag_id in self.auto_anal():
            return True
        with self.v_servo.set(110):
            for angle in range(30, 151, 20):
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
            time.sleep(1)
            bias = self.auto_anal()
            if tag_id not in bias:
                print('P瞄准中丢失目标！')
                raise TagNotFoundError
            bias = bias[tag_id]
        
        diff = kp * bias[0], kp * bias[1]
        return diff
    
    def aim(self, tag_id: int):
        self.scan_tag(tag_id)
        eps = 1, 1
        diff = 1000, 1000
        while abs(diff[0]) > eps[0] or abs(diff[1]) > eps[1]:
            diff = self.p_aim(tag_id)
            print(f'误差：{diff}')
            with self.h_servo.i_set(diff[0]),\
                    self.v_servo.i_set(diff[1]):
                time.sleep(0.5)
        print(f'瞄准完成,{diff=}')
        # self.h_servo.set_to(self.h_servo.angle + diff[0])
    
    def 摇摇乐(self):
        now = self.v_servo.angle
        for i in range(3):
            with self.v_servo.set(35):
                time.sleep(0.15)
            with self.v_servo.set(80):
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
        print('进入扫射')
        self.摇摇乐()
        with self.shooting(85), self.v_servo.set(110):
            for i in range(45, 150, 5):
                self.h_servo.set_to(i)
            for i in range(150, 45, -5):
                self.h_servo.set_to(i)
    
    def precise_shoot(self, tag_id: int):
        self.aim(tag_id)
        self.摇摇乐()
        self.shoot(1.5)
    
    def smart_shoot(self, tag_ids: Sequence[int]):
        try:
            for i in tag_ids:
                self.precise_shoot(i)
        except TagNotFoundError:
            self.brutal_shoot()


if __name__ == '__main__':
    pan = Pan()
