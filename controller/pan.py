"""云台"""
import time

try:
    from .drivers.camera import Camera
    from car.pan.servo import Servo
    from car.pan.gun import Gun
except ImportError:
    from drivers.camera import Camera
    from car.pan.servo import Servo
    from car.pan.gun import Gun


class Pan(Gun):
    def __init__(self):
        # 水平和垂直方向的舵机
        super().__init__()
        self.camera = Camera()
        self.v_servo: Servo = Servo(11)
        self.h_servo: Servo = Servo(12)
        # self.v_servo.set(80)
    
    def scan_shoot(self):
        with self.shooting(65), self.v_servo.set(90):
            for i in range(60, 120, 5):
                self.h_servo.set_to(i)
            for i in range(120, 60, -5):
                self.h_servo.set_to(i)
    
    # 搜索目标
    def __scan_target(self, target_id):
        if target_id in self.camera.auto_anal():
            print('不用找直接就是了')
            return True
        for l_angle in range(0, 180, 30):
            self.h_servo.set(l_angle)
            location_map = self.camera.auto_anal()
            if target_id in location_map:
                print('已经找到目标')
                return True
        print('你妈的 没找到')
        return False
    
    def p_aim(self, tag_id):
        kp = -0.035
        bias = self.camera.auto_anal()[tag_id]
        # 计算积分常量
        print(bias)
        
        diff = kp * bias[0], kp * bias[1]
        print(diff)
        return diff
    
    def aim(self, tag_id: int):
        print('搜索目标！')
        found = self.__scan_target(tag_id)
        # 找不到就扫射
        if not found:
            print('你妈的 找不到 扫你妈的')
            # self.scan_shoot()
            return False
        
        # 瞄准范围
        eps = 35, 35
        diff = 1000, 1000
        
        try:
            while diff[0] > eps[0] or diff[1] > eps[1]:
                diff = self.p_aim(tag_id)
                with self.h_servo.i_set(diff[0]),\
                        self.v_servo.i_set(diff[1]):
                    time.sleep(0.5)
            return True
        
        except KeyError:
            print('你妈的 好像出了点问题 扫他丫的')
            # self.scan_shoot()
            # 无法成功瞄准
            return False
    
    def auto_shoot(self):
        # 抖一抖减轻卡弹
        now = self.v_servo.angle
        for i in range(3):
            with self.v_servo.set(35):
                time.sleep(0.15)
            with self.v_servo.set(75):
                time.sleep(0.15)
        self.v_servo.set_to(now)
        self.shoot(2)
    
    def shoot_down(self, tag_id: int):
        result = self.aim(tag_id)
        if result:
            self.auto_shoot()
            while self.aim(tag_id):
                self.auto_shoot()
        
        return True

    def pid_aim(self, tag_id):
        pass


if __name__ == '__main__':
    pan = Pan()
    print("开始")
    # pan.scan_shoot()
    # pan.pid_aim(2)
    pan.aim(1)
    # pan.auto_shoot()
    print('整完了')
