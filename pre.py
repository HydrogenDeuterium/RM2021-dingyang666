"""
预赛脚本
"""
from drivers import Car

tag_seq = [1, 2, 3, 4]

if __name__ == "__main__":
    car = Car()
    car.go(1.5)
    car.left(90)
    car.go(0.5)
    # at save#1
    
    car.left(90)
    car.go(0.5)
    car.auto_shoot(tag_seq)
    car.back(0.5)
    car.right(90)
    car.go(1.5)
    car.left(90)
    car.go(2)
    car.right(90)
    car.go(0.5)
    # done
    pass
