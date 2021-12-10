"""云台"""

try:
    from .drivers.camera import Camera
    from .drivers.servo import Servo
    from .drivers.gun import Gun
except ImportError:
    from drivers.camera import Camera
    from drivers.servo import Servo
    from drivers.gun import Gun


class Pan(Gun):
    def __init__(self):
        # 水平和垂直方向的舵机
        super().__init__()
        self.camera = Camera()
        self.h_servo: Servo = Servo(12, min_ratio=2, max_ratio=12.5)
        self.v_servo: Servo = Servo(11, min_ratio=5, max_ratio=15)
        self.v_servo.set(80)
        # self.v_servo.set(120)
    
    # 默认射击
    def __shoot(self, tags):
        for i in tags:
            self.pid_aim(i)
            self.auto_shoot(5)
    
    # 水平方向角度调整
    def __horizontal(self, angle=None):
        if angle:
            return self.h_servo.set(angle)
        return self.h_servo.get()
    
    # 水平方向角度
    def __vertical(self, angle=None):
        if angle:
            return self.v_servo.set(angle)
        return self.v_servo.get()
    
    # 搜索目标
    def __scan_target(self, target_id):
        if target_id in self.camera.auto_anal():
            print('不用找直接就是了')
            return
        for l_angle in range(0, 180, 25):
            self.h_servo.set(l_angle)
            location_map = self.camera.auto_anal()
            if target_id in location_map:
                print('已经找到目标')
                return True
        print('你妈的 没找到')
        return False
    
    def pid_aim(self, tag_id):
        print('搜索目标！')
        found = self.__scan_target(tag_id)
        if not found:
            self.v_servo.set(80)
        
        integrate = [0., 0.]
        last = [0., 0.]
        kp, ki, kd = -0.035, 0.0, 0.0
        
        # 瞄准范围
        eps = 50
        
        bias = self.camera.auto_anal()[tag_id]
        # 到达瞄准范围后则不再瞄准
        while abs(bias[0]) > eps or abs(bias[1]) > eps:
            # 计算积分常量
            print(bias)
            integrate[0] += bias[0]
            integrate[1] += bias[1]
            # 计算调整值
            diff = (
                kp * bias[0] + ki * integrate[0] + (bias[0] - last[0]) * kd,
                kp * bias[1] + ki * integrate[1] + (bias[1] - last[1]) * kd
            )
            print(diff)
            print()
            # 调整舵机
            angle_h = self.h_servo.get() + diff[0]
            self.h_servo.set(angle_h)
            angle_v = self.v_servo.get() + diff[1]
            self.v_servo.set(angle_v)
            # 保存微分常量
            last = bias
            # 获取调整后的结果
            result = self.camera.auto_anal()
            bias = result[tag_id]
        print(bias)


if __name__ == '__main__':
    pan = Pan()
    print("开始")
    for i in range(0,180,30):
        pan.h_servo.set(i)
    # pan.pid_aim(1)
    print('瞄完了')
