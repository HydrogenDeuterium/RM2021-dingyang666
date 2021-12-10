from controller.chassisXZq import Chassis
from controller.pan import Pan
from controller.drivers.servo import Servo

print('import finished')


class Car(Chassis):
    def __init__(self):
        super().__init__()
        self.pan = Pan()
    
    def pid_aim(self, tag_id):
        self.pan.pid_aim(tag_id)


if __name__ == '__main__':
    car = Car()
    print('初始化完毕')
    pass
