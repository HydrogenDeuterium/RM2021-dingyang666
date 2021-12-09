from controller.chassisXZq import Chassis
from controller.pan import Pan
from controller.drivers.servo import Servo

print('import finished')


class Car(Chassis, Pan):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    print('Hello!')
