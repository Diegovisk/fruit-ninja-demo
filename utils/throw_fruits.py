import random

from models.Fruit import Fruit
from utils.configs import FRUIT_LIST


def throw_fruits(fruits, win):
    num_fruits = random.randint(0, 3)
    for _ in range(num_fruits + 1):
        option = random.randint(0, len(FRUIT_LIST) - 1)
        fruits.append(Fruit(FRUIT_LIST[option], win))
