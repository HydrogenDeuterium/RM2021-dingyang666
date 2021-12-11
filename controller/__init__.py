from controller.chassisXZq import Chassis
from controller.pan import Pan

print('import finished')


class Car(Chassis):
    def __init__(self):
        super().__init__()
        self.pan = Pan()
    
    def pid_aim(self, tag_id):
        self.pan.pid_aim(tag_id)
    
    def auto_shoot(self):
        self.pan.shoot(3)
    
    def smart_shoot(self, tag_seq):
        for tags in tag_seq:
            self.pan.pid_aim(tags)
            self.pan.shoot(3)


if __name__ == '__main__':
    car = Car()
    print('初始化完毕')
    # car.front(0.5)
    # car.back(1)
    # car.left()
    # car.right()
    pass
