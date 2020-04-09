from random import random


def rand_range_f(low, high):
    return random() * (high - low) + low


def is_default(default_probability):
    return random() < default_probability
