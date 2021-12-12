from controller import Car

car = Car()


def a2A():
    car.front(1)
    car.left(90)
    car.front(0.5)
    car.right()
    car.front(0.5)
    car.left(90)
    car.front(0.5)
    car.right()
    car.back()


def A2a():
    car.front()
    car.left()
    car.back()
    car.right()
    car.back()
    car.left()
    car.back()
    car.right()
    car.back(1)


def A2B():
    car.front(1)
    car.left()
    car.front()
    car.right()
    car.back()
    car.left()
    car.front()
    car.right()
    car.front(1)
    car.left()
    car.front(1.5)
    car.right()
    car.front()
    car.left()
    car.front()


def B2A():
    car.back()
    car.right()
    car.back()
    car.left()
    car.back(1.5)
    car.right()
    car.back(1)
    car.left()
    car.back()
    car.right()
    car.front()
    car.left()
    car.back()
    car.right()
    car.back(1)


def b2B():
    car.back(0.5)
    car.back(0.5)
    car.right(90)
    car.front(0.5)
    car.left(90)
    car.front(0.5)
    car.right(0)
    car.front()
    car.front()


def B2b():
    car.back(1)
    car.left()
    car.back()
    car.right()
    car.back()
    car.left()
    car.front(1)


def c2C():
    car.back(1)
    car.left(90)
    car.front(0.5)
    car.right()
    car.back(90)
    car.left()
    car.back(0.5)
    car.right()
    car.back()
    car.left()
    car.right()
    car.back()
    car.left()
    car.back(1)


if __name__ == '__main__':
    # a2A()
    B2b()
