"""
预赛脚本
"""
from controller import Car

tag_seq = [2, 1, 3, 4]

if __name__ == "__main__":
    car = Car()
    pass
    # car.front(1.5)
    # car.left(70)
    # car.front(0.5)
    # car.right(70)
    # car.back(0.5)
    # # at save#1
    #
    # car.smart_shoot(tag_seq)
    car.front(1.5)
    car.left(60)
    car.front(2)
    # 那一块有点胶带所以转的特别快
    car.right(60)
    car.front(0.5)
    # done
    pass
