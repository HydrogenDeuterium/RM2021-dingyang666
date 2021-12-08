from drivers.camera import Camera
from drivers.chassis import Chassis
from drivers.gun import Gun
from drivers.motor import Motor
from drivers.pan import Pan, pan
from drivers.servo import Servo

print('import finished')


class Car(Chassis, Pan):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    print('Hello!')
