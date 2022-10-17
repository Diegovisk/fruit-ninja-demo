import random
from models.Fruit import Fruit
from utils.coin_flip import coin_flip


def add_bombs(fruits, win):
    if coin_flip():
        for _ in range(random.randint(1, 2)):
            fruits.append(Fruit("bomb", win))
