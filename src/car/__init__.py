from src.car.chassis import Chassis
from src.car.pan import Pan


class Car(Chassis, Pan):
    
    def __init__(self):
        Chassis.__init__(self)
        Pan.__init__(self)
    
    def __del__(self):
        Chassis.__del__(self)
        Pan.__del__(self)


if __name__ == '__main__':
    car = Car()
