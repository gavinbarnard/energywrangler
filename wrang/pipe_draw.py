#!/usr/bin/env
"""drawing pipes"""

import logging
from enum import Enum

import pygame

from pygame.locals import * #pylint:disable=wildcard-import,unused-wildcard-import


RAINBOW = ["RED", "ORANGE", "YELLOW", "GREEN", "LIGHTBLUE", "WHITE"]

class PIPE(Enum):
    "enum values for pipe_type"
    SNSTART = 1
    SN_PASS = 2
    SE_PASS = 3
    SW_PASS = 4
    S_N_END = 5

class CARDINAL(Enum):
    "enum values for directional thingies"
    NORTH = 0
    WEST = 90
    SOUTH = 180
    EAST = 270

class PipeTile(pygame.sprite.Sprite): #pylint:disable=too-many-instance-attributes
    "Is a pipe tile"
    fill = 0
    pipe_type = None
    lastooze = 0
    placed = False
    first = 1
    rainbow = 0
    rotate = 0
    next_pipe = None
    cardinal = None
    scardinal = None
    previous_fill = -1
    def __init__(self, #pylint:disable=too-many-arguments
                 pipe_type=0,
                 pipe_rotate=0,
                 max_capacity=36,
                 start_x=0,
                 start_y=0):
        "pipe init"
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.pipe_type = pipe_type
        self.max_capacity = max_capacity
        self.image = None
        self.image = pygame.Surface((36, 36))
        self.lastooze = 0
        self.placed = False
        self.pipe_draw()
        self.rainbow = 0
        self.rect = self.image.get_rect().move(start_x, start_y)
        self.first = 1
        self.rotate = pipe_rotate
        self.previous_fill = -1
        #sets up placement validation markers
        if self.rotate == 0:
            if pipe_type in (PIPE.SN_PASS, PIPE.SNSTART, PIPE.S_N_END):
                self.cardinal = CARDINAL.NORTH
                self.scardinal = CARDINAL.SOUTH
            elif pipe_type == PIPE.SE_PASS:
                self.cardinal = CARDINAL.EAST
                self.scardinal = CARDINAL.SOUTH
            elif pipe_type == PIPE.SW_PASS:
                self.cardinal = CARDINAL.WEST
                self.scardinal = CARDINAL.SOUTH
        elif self.rotate != 0:
            if pipe_type in (PIPE.SN_PASS, PIPE.SNSTART, PIPE.S_N_END):
                if self.rotate == CARDINAL.WEST.value:
                    self.cardinal = CARDINAL.WEST
                    self.scardinal = CARDINAL.EAST
                elif self.rotate == CARDINAL.SOUTH.value:
                    self.cardinal = CARDINAL.SOUTH
                    self.scardinal = CARDINAL.NORTH
                elif self.rotate == CARDINAL.EAST.value:
                    self.cardinal = CARDINAL.EAST
                    self.scardinal = CARDINAL.WEST
            elif pipe_type == PIPE.SE_PASS:
                if self.rotate == CARDINAL.WEST.value:
                    self.cardinal = CARDINAL.NORTH
                    self.scardinal = CARDINAL.EAST
                elif self.rotate == CARDINAL.SOUTH.value:
                    self.cardinal = CARDINAL.WEST
                    self.scardinal = CARDINAL.NORTH
                elif self.rotate == CARDINAL.EAST.value:
                    self.cardinal = CARDINAL.SOUTH
                    self.scardinal = CARDINAL.WEST
            elif pipe_type == PIPE.SW_PASS:
                if self.rotate == CARDINAL.WEST.value:
                    self.cardinal = CARDINAL.SOUTH
                    self.scardinal = CARDINAL.EAST
                elif self.rotate == CARDINAL.SOUTH.value:
                    self.cardinal = CARDINAL.EAST
                    self.scardinal = CARDINAL.NORTH
                elif self.rotate == CARDINAL.EAST.value:
                    self.cardinal = CARDINAL.NORTH
                    self.scardinal = CARDINAL.WEST
        self.fill = 0
        self.rainbow = 0
        self.next_pipe = None
        logging.debug("PipeTile(%s, %s, %d, %d, %d) created",
                      pipe_type,
                      pipe_rotate,
                      max_capacity,
                      start_x,
                      start_y)

    def draw_arrows(self, direction, left, top):
        "draws an arrow"
        if self.fill < (self.max_capacity/5) * 4: # don't draw arrows when filled
            if direction[0].lower() == "n":
                pygame.draw.rect(self.image,
                                 Color("GREEN"),
                                 Rect(left + 2, top + 4, 8, 1)) # green arrow
                pygame.draw.rect(self.image,
                                 Color("GREEN"),
                                 Rect(left + 3, top + 3, 6, 1))
                pygame.draw.rect(self.image,
                                 Color("GREEN"),
                                 Rect(left + 4, top + 2, 4, 1))
                pygame.draw.rect(self.image,
                                 Color("GREEN"),
                                 Rect(left + 5, top + 1, 2, 1))
            elif direction[0].lower() == "e":
                pygame.draw.rect(self.image, Color("GREEN"), Rect(left + 4, top + 5, 1, 2))
                pygame.draw.rect(self.image, Color("GREEN"), Rect(left + 3, top + 4, 1, 4))
                pygame.draw.rect(self.image, Color("GREEN"), Rect(left + 2, top + 3, 1, 6))
                pygame.draw.rect(self.image, Color("GREEN"), Rect(left + 1, top + 2, 1, 8))

    def pipe_draw(self):
        "draws or updates the pipe"
        self.image = pygame.Surface((36, 36))
        self.image.fill(Color("BLACK"), Rect(0, 0, 36, 36))

        if self.pipe_type in (PIPE.SNSTART, PIPE.SN_PASS, PIPE.S_N_END):
            pygame.draw.rect(self.image, Color("GREY"), Rect(0, 0, 12, 36)) # left side border
            pygame.draw.rect(self.image, Color("GREY"), Rect(24, 0, 12, 36)) # right side border
            pygame.draw.rect(self.image, Color("DARKBLUE"), Rect(12, 0, 2, 36)) # left side of pipe
            pygame.draw.rect(self.image, Color("DARKBLUE"), Rect(22, 0, 2, 36)) # right side of pipe
            for arrow_multipler in range(0, 3):
                self.draw_arrows('n', 12, 12 * arrow_multipler)
            if self.pipe_type == PIPE.SNSTART:
                pygame.draw.rect(self.image,
                                 Color(RAINBOW[self.rainbow]),
                                 Rect(14, 35, 8, 1))
                self.rainbow = self.rainbow + 1
                if self.rainbow >= len(RAINBOW):
                    self.rainbow = 0
            elif self.pipe_type == PIPE.S_N_END:
                pygame.draw.rect(self.image,
                                 Color(RAINBOW[self.rainbow]),
                                 Rect(14, 0, 8, 1))
                self.rainbow = self.rainbow + 1
                if self.rainbow >= len(RAINBOW):
                    self.rainbow = 0
        elif self.pipe_type in (PIPE.SE_PASS, PIPE.SW_PASS):
            pygame.draw.rect(self.image, Color("GREY"), Rect(0, 0, 36, 12))
            pygame.draw.rect(self.image, Color("GREY"), Rect(0, 0, 12, 36))
            pygame.draw.rect(self.image, Color("GREY"), Rect(24, 24, 12, 12))
            pygame.draw.rect(self.image, Color("DARKBLUE"), Rect(12, 12, 2, 24))
            pygame.draw.rect(self.image, Color("DARKBLUE"), Rect(12, 12, 24, 2))
            pygame.draw.rect(self.image, Color("DARKBLUE"), Rect(22, 22, 12, 2))
            pygame.draw.rect(self.image, Color("DARKBLUE"), Rect(22, 22, 2, 12))
            self.draw_arrows('n', 12, 24)
            self.draw_arrows('e', 24, 12)

        if self.fill > 0:
            if self.pipe_type in (PIPE.SNSTART, PIPE.SN_PASS, PIPE.S_N_END):
                pygame.draw.rect(self.image,
                                 Color("YELLOW"),
                                 Rect(14, 36 - self.fill, 8, self.fill))
            elif self.pipe_type in (PIPE.SE_PASS, PIPE.SW_PASS):
                half_fill = self.fill - 18
                if self.fill <= 18:
                    pygame.draw.rect(self.image,
                                    Color("YELLOW"),
                                    Rect(14, 36 - self.fill, 8, self.fill))
                if self.fill > 18:
                    pygame.draw.rect(self.image,
                                    Color("YELLOW"),
                                    Rect(14, 18, 8, 18))
                    pygame.draw.rect(self.image,
                                    Color("YELLOW"),
                                    Rect(14, 14, half_fill+3, 8))

        if self.pipe_type == PIPE.SW_PASS:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.rotate > 0:
            self.image = pygame.transform.rotate(self.image, self.rotate)

    def rotate_pipe(self):
        "rotates the pipe tile"
        if self.cardinal == CARDINAL.EAST:
            self.cardinal = CARDINAL.NORTH
        else:
            self.cardinal = CARDINAL(self.cardinal.value + 90)
        if self.scardinal == CARDINAL.EAST:
            self.scardinal = CARDINAL.NORTH
        else:
            self.scardinal = CARDINAL(self.scardinal.value + 90)
        self.rotate = self.rotate + 90
        if self.rotate >= 360:
            self.rotate = 0
        self.pipe_draw()

    def _placed(self, pipe):
        self.placed = True
        pipe.next_pipe = self

    def place(self, last_pipe_group, pipe_group):
        """places the pipe tile validates the pipe flow direction to adjacent pipe
        tiles defined at top of script for import into base script
        """
        if self.pipe_type == PIPE.SNSTART:
            self.placed = True
        for pipe in pipe_group:
            if pygame.sprite.spritecollide(self, [pipe], False) and self != pipe:
                return
        for pipe in last_pipe_group:
            place = None
            if self.rect.left == pipe.rect.left and pipe.rect.top - self.rect.top == 36: #up
                place = CARDINAL.NORTH
            elif self.rect.top == pipe.rect.top and pipe.rect.left - self.rect.left == 36: #left
                place = CARDINAL.WEST
            elif self.rect.left == pipe.rect.left and pipe.rect.top - self.rect.top == -36: #down
                place = CARDINAL.SOUTH
            elif self.rect.top == pipe.rect.top and pipe.rect.left - self.rect.left == -36: #right
                place = CARDINAL.EAST
            if place:
                if pipe.cardinal == CARDINAL.WEST and self.scardinal == CARDINAL.EAST or \
                    pipe.cardinal == CARDINAL.NORTH and self.scardinal == CARDINAL.SOUTH or \
                        pipe.cardinal == CARDINAL.SOUTH and self.scardinal == CARDINAL.NORTH or \
                            pipe.cardinal == CARDINAL.EAST and self.scardinal == CARDINAL.WEST:
                    self._placed(pipe)

    def ooze(self, oozeby=1):
        "oozes liquid from the pipe"
        last_temp = pygame.time.get_ticks()
        if (self.pipe_type == PIPE.SNSTART or self.fill > 0) and self.fill < self.max_capacity:
            if last_temp - self.lastooze > 250:
                self.fill = self.fill + oozeby - self.first
                if self.fill > self.max_capacity:
                    self.fill = self.max_capacity
                self.lastooze = last_temp
                self.first = 0


    def update(self):
        "updates the pipe"
        if self.fill != self.previous_fill or self.pipe_type in (PIPE.S_N_END, PIPE.SNSTART):
            self.pipe_draw()
            self.previous_fill = self.fill
