#!/usr/bin/env python
""" utils """

import os
import logging
from random import random, choice

import pygame

from .pipe_draw import PIPE, CARDINAL

def random_level(random_watermark=70, level_length=20, capacity=36, high_capacity=0):
    "ridiculous procedural map gen!"
    pipe_queue = []
    pipe_queue.append([PIPE.SNSTART, choice(list(CARDINAL)).value, capacity])

    for counter in range(0, level_length):
        chance = int(random() * 100)
        if high_capacity > 0:
            high_capacity_chance = int(random() * 100)
            if high_capacity_chance >= 0 and high_capacity_chance < high_capacity_chance+1:
                capacity = capacity *2
        if chance >= 0 and chance < random_watermark+1:
            pipe_queue.append([PIPE.SN_PASS, choice(list(CARDINAL)).value, capacity])
        if chance > random_watermark and chance < 101:
            pipe_queue.append([choice([PIPE.SE_PASS, PIPE.SW_PASS]), choice(list(CARDINAL)).value, capacity])
        logging.info("added %s %d", pipe_queue[counter+1][0], pipe_queue[counter+1][1])

    #pipe_queue.append([PIPE.S_N_END, choice(list(CARDINAL)).value])
    # end pipe to be handled by checking that pipe_queue has been exhausted first
    return pipe_queue

class DummySound: #pylint:disable=too-few-public-methods
    "Is a dummy sound"
    def play(self):
        'plays nothing'

def load_sound(file):
    "Loads sound"
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    if not pygame.mixer:
        return DummySound()
    file = os.path.join(main_dir, 'resources', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        logging.warning('Warning, unable to load, %s', file)
    return DummySound()