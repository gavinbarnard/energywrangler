#!/usr/bin/env
"""menu buttons"""


import pygame

from pygame.locals import * #pylint:disable=wildcard-import,unused-wildcard-import

class StartGameButton(pygame.sprite.Sprite):
    " the start button "
    image = None
    def __init__(self, start_x, start_y, sprite_color=Color("BLACK")):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.Font(None, 36)
        msg = "Start Game"
        self.sprite_color = sprite_color
        msg_image = self.font.render(msg, True, self.sprite_color, Color("WHITE"))
        self.image = pygame.Surface(
            (msg_image.get_width() + 6, msg_image.get_height() + 6)
        )
        pygame.draw.rect(
            self.image,
            Color(0, 0, 0),
            (1, 1, msg_image.get_width() + 5, msg_image.get_height() + 5),
            1
        )
        self.image.blit(msg_image, (3, 3))
        self.rect = self.image.get_rect().move(start_x - self.image.get_rect().width/2, start_y - self.image.get_rect().height * 4 )
    def check_click(self, mouse):
        """ Checks if there is a collision at the fed coords """
        if self.rect.collidepoint(mouse):
            return True
        return False
    def update(self):
        "updates the start button"


class InstructionsButton(pygame.sprite.Sprite):
    " the start button "
    image = None
    def __init__(self, start_x, start_y, sprite_color=Color("BLACK")):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.Font(None, 36)
        msg = "Story / Instructions"
        self.sprite_color = sprite_color
        msg_image = self.font.render(msg, True, self.sprite_color, Color("WHITE"))
        self.image = pygame.Surface(
            (msg_image.get_width() + 6, msg_image.get_height() + 6)
        )
        pygame.draw.rect(
            self.image,
            Color(0, 0, 0),
            (1, 1, msg_image.get_width() + 5, msg_image.get_height() + 5),
            1
        )
        self.image.blit(msg_image, (3, 3))
        self.rect = self.image.get_rect().move(start_x - self.image.get_rect().width/2, start_y - self.image.get_rect().height )
    def check_click(self, mouse):
        """ Checks if there is a collision at the fed coords """
        if self.rect.collidepoint(mouse):
            return True
        return False
    def update(self):
        "updates the start button"

class QuitButton(pygame.sprite.Sprite):
    " the start button "
    image = None
    def __init__(self, start_x, start_y, sprite_color=Color("BLACK")):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.Font(None, 36)
        msg = "Quit"
        self.sprite_color = sprite_color
        msg_image = self.font.render(msg, True, self.sprite_color, Color("WHITE"))
        self.image = pygame.Surface(
            (msg_image.get_width() + 6, msg_image.get_height() + 6)
        )
        pygame.draw.rect(
            self.image,
            Color(0, 0, 0),
            (1, 1, msg_image.get_width() + 5, msg_image.get_height() + 5),
            1
        )
        self.image.blit(msg_image, (3, 3))
        self.rect = self.image.get_rect().move(start_x - self.image.get_rect().width/2, start_y + self.image.get_rect().height * 2 )
    def check_click(self, mouse):
        """ Checks if there is a collision at the fed coords """
        if self.rect.collidepoint(mouse):
            return True
        return False
    def update(self):
        "updates the start button"

class InstructionsSprite(pygame.sprite.Sprite):
    "displays the game instructions"
    image = None
    def __init__(self, start_x=0, start_y=0, sprite_color=Color("BLACK")):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.Font(None, 24)
        self.sprite_color = sprite_color
        msg = []
        msg.append("                                                               Welcome Player to The Whitespace,")
        msg.append("a 2dimensional plane that has existed since long before the cosmic event that brought your 3dimensional world to exist")
        msg.append("        However a strange abberation has appeared and is forcing us to channel their energies through our plane")
        msg.append("                 Please assist us in safe guarding these passages by laying out a tunnel for the engery")
        msg.append("                                   A rainbow light indicates the start and the end of a tunnel")
        msg.append("                                   If you successfully complete a tunnel a new set will load")
        msg.append("                                        If you fail the energy will flood The Whitespace")
        msg.append(" ")
        msg.append("Enter - Get the next piece")
        msg.append("D - Dump the current piece to the end")
        msg.append("1 or 2 or 3 - Holding slots if you do not like the current piece")
        msg.append("ESC - return to menu")
        msg.append("SPACE - increase the speed the energy goes")
        msg.append("Left Click - Place a piece")
        msg.append("Right Click - Rotate a piece 90 degrees")
        msg_image_r = []
        line_height = 0
        for msg_render in msg:
            msg_image_r.append(self.font.render(msg_render, True, self.sprite_color, Color("WHITE")))
            line_height = msg_image_r[len(msg_image_r)-1].get_rect().height
        line_height = line_height + 2
        self.image = pygame.Surface((1022, 766))
        self.image.fill(Color("WHITE"))
        counter = 0
        for msg_image in msg_image_r:
            self.image.blit(msg_image, (2, 2 + line_height*counter))
            counter = counter + 1
    
        self.rect = self.image.get_rect().move(start_x, start_y)
    def check_click(self, mouse):
        """ Checks if there is a collision at the fed coords """
        if self.rect.collidepoint(mouse):
            return True
        return False