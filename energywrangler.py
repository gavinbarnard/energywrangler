#!/usr/bin/env python
""" Energy wrangler
version 2 write
"""

import logging
import os
from datetime import datetime

import pygame
from pygame.locals import * #pylint:disable=wildcard-import,unused-wildcard-import

from wrang import * #pylint:disable=wildcard-import,unused-wildcard-import

SCREENRECT = Rect(0, 0, 1024, 768)
GAME_NAME = "Energy Wrangler"


def main(p_win_style=0):
    "the main function"
    date_time_obj = datetime(1, 1, 1)
    date_time_obj = date_time_obj.today()
    year = date_time_obj.year
    day = date_time_obj.day
    month = date_time_obj.month
    hour = date_time_obj.hour
    minute = date_time_obj.minute
    second = date_time_obj.second
    try:
        os.mkdir("log")
    except FileExistsError:
        pass

    logging.basicConfig(
        level=logging.INFO,
        filename="log/{}-{}{:02d}{:02d}-{:02d}{:02d}{:02d}.log".format(
            __file__,
            year,
            month,
            day,
            hour,
            minute,
            second,
            ),
        format='%(asctime)s %(levelname)s %(message)s')
    logging.info("e wrangler logging init")

    clock = pygame.time.Clock()

    instructions_sprite_group = pygame.sprite.Group()
    menu_sprite_group = pygame.sprite.Group()
    pipe_sprite_group = pygame.sprite.Group()
    last_sprite = pygame.sprite.GroupSingle()
    last_laid_pipe = pygame.sprite.GroupSingle()
    s_group = pygame.sprite.RenderUpdates()

    PipeTile.containers = s_group, pipe_sprite_group, last_sprite
    StartGameButton.containers = s_group, menu_sprite_group
    InstructionsButton.containers = s_group, menu_sprite_group
    QuitButton.containers = s_group, menu_sprite_group
    InstructionsSprite.containers = s_group, instructions_sprite_group

    if pygame.get_sdl_version()[0] == 2:
        pygame.mixer.pre_init(44100, 16, 2, 1024)
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        pygame.mixer = None
    else:
        pygame.mixer.init()

    flow_sound = load_sound("flow.ogg")
    flow_sound.set_volume(0.15)


    win_style = p_win_style
    best_depth = pygame.display.mode_ok(SCREENRECT.size, win_style, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, win_style, best_depth)

    pygame.display.set_caption(GAME_NAME)
    pygame.mouse.set_visible(1)

    chance_for_straight = 70
    level_length = 20
    oozeby = 1
    pipe_queue = random_level(random_watermark=chance_for_straight, level_length=level_length)

    background = pygame.Surface(SCREENRECT.size)
    background.fill(Color("WHITE"))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    first = True
    #game states
    game_menu = True
    game_on = False
    game_flood = False
    game_win = False
    game_instructions = False
    pipe_slots = []
    pipe_slots.append([])
    pipe_slots.append([])
    pipe_slots.append([])
    while game_menu:
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                game_menu = False

            for sprite in pipe_sprite_group:
                sprite.remove()
                sprite.kill()
            flow_sound.stop()
            if not menu_sprite_group and not game_instructions:
                for sprite in instructions_sprite_group:
                    sprite.remove()
                    sprite.kill()

                StartGameButton(SCREENRECT.width/2, SCREENRECT.height/2)
                InstructionsButton(SCREENRECT.width/2, SCREENRECT.height/2)
                QuitButton(SCREENRECT.width/2, SCREENRECT.height/2)

            if game_instructions and not instructions_sprite_group:
                for sprite in menu_sprite_group:
                    sprite.remove()
                    sprite.kill()
                InstructionsSprite(50, 200)

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                for sprite in menu_sprite_group:
                    if sprite.check_click(mouse):
                        if isinstance(sprite, StartGameButton):
                            game_on = True
                        elif isinstance(sprite, InstructionsButton):
                            game_instructions = not game_instructions
                        elif isinstance(sprite, QuitButton):
                            return
                for sprite in instructions_sprite_group:
                    if isinstance(sprite, InstructionsSprite):
                        game_instructions = not game_instructions

        while game_on:
            if menu_sprite_group:
                for sprite in menu_sprite_group:
                    sprite.remove()
                    sprite.kill()
            if instructions_sprite_group:
                for sprite in instructions_sprite_group:
                    sprite.remove()
                    sprite.kill()
            next_pipe = None
            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                    game_on = False
                    oozeby = 1
                    chance_for_straight = 70
                    level_length = 20
                    oozeby = 1
                    first = True
                    pipe_queue = random_level(random_watermark=chance_for_straight, level_length=level_length)
                if event.type == KEYDOWN and (event.key == K_d):
                    if last_sprite:
                        for sprite in last_sprite:
                            if not sprite.placed and sprite.pipe_type != PIPE.SNSTART:
                                pipe_queue.append([sprite.pipe_type, sprite.rotate, sprite.max_capacity])
                                sprite.kill()
                                next_pipe = pipe_queue.pop(0)
                                PipeTile(next_pipe[0], next_pipe[1], next_pipe[2])

                if event.type == KEYDOWN and (event.key in (K_1, K_2, K_3)):
                    if last_sprite:
                        for sprite in last_sprite:
                            if not sprite.placed and sprite.pipe_type != PIPE.SNSTART:
                                if pipe_slots[event.key - K_1]:
                                    pipe_slots[event.key - K_1].append([sprite.pipe_type, sprite.rotate, sprite.max_capacity])
                                    next_pipe = pipe_slots[event.key - K_1].pop(0)
                                elif pipe_queue:
                                    pipe_slots[event.key - K_1].append([sprite.pipe_type, sprite.rotate, sprite.max_capacity])
                                    next_pipe = pipe_queue.pop(0)
                                if next_pipe:
                                    sprite.kill()
                                    PipeTile(next_pipe[0], next_pipe[1], next_pipe[2])

                if event.type == KEYDOWN and (event.key == K_SPACE):
                    oozeby = oozeby * 2

                if event.type == KEYDOWN and (event.key in(K_KP_ENTER, K_RETURN)):
                    if pipe_queue: # if there's anything in queue
                        pop_next = first
                        if last_sprite:
                            for sprite in last_sprite:
                                if sprite.placed:
                                    pop_next = True
                        if first:
                            first = False
                        if pop_next:
                            next_pipe = pipe_queue.pop(0)
                            PipeTile(next_pipe[0], next_pipe[1], next_pipe[2])
                    elif pipe_slots[0] or pipe_slots[1] or pipe_slots[2]: # if there's anything in the holding slots
                        pop_next = first
                        if last_sprite:
                            for sprite in last_sprite:
                                if sprite.placed:
                                    pop_next = True
                        if first:
                            first = False
                        if pop_next:
                            if pipe_slots[0]:
                                next_pipe = pipe_slots[0].pop(0)
                            elif pipe_slots[1]:
                                next_pipe = pipe_slots[1].pop(0)
                            elif pipe_slots[2]:
                                next_pipe = pipe_slots[2].pop(0)
                            PipeTile(next_pipe[0], next_pipe[1], next_pipe[2])
                    else: # nothing left give them the end piece
                        if last_sprite:
                            for sprite in last_sprite:
                                if sprite.pipe_type != PIPE.S_N_END:
                                    pipe_queue.append([PIPE.S_N_END, choice(list(CARDINAL)).value, 36])
                                    next_pipe = pipe_queue.pop(0)
                                    PipeTile(next_pipe[0], next_pipe[1], next_pipe[2])
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if last_sprite:
                        for sprite in last_sprite:
                            sprite.place(last_laid_pipe, pipe_sprite_group)
                            if sprite.placed:
                                last_laid_pipe.add(sprite)
                if event.type == MOUSEBUTTONDOWN and event.button == 3:
                    if last_sprite:
                        for sprite in last_sprite:
                            if not sprite.placed:
                                sprite.rotate_pipe()


            for pipe in pipe_sprite_group:
                if pipe.placed:
                    pipe.ooze(oozeby)
                    if not pygame.mixer.get_busy():
                        flow_sound.play(-1)
                    if pipe.fill == pipe.max_capacity:
                        pipe.fill = pipe.fill + 1
                        if pipe.next_pipe:
                            pipe.next_pipe.fill = 1
                        elif sprite.pipe_type == PIPE.S_N_END and pipe.fill == pipe.max_capacity+1:
                            game_win = True
                        else:
                            logging.info("Game Over")
                            game_on = False
                            game_flood = True
                else:
                    mouse = pygame.mouse.get_pos()
                    pipe.rect.center = mouse
                    # snap on to last laid pipe edges
                    collision = pygame.sprite.spritecollideany(pipe, last_laid_pipe)
                    if collision:
                        if collision != pipe:
                            top = collision.rect.top - pipe.rect.top
                            left = collision.rect.left - pipe.rect.left
                            if top > 0 and abs(top) > abs(left):
                                pipe.rect.top = collision.rect.top - 36
                                pipe.rect.left = collision.rect.left
                            elif top < 0 and abs(top) > abs(left):
                                pipe.rect.top = collision.rect.top + 36
                                pipe.rect.left = collision.rect.left
                            elif left > 0 and abs(top) < abs(left):
                                pipe.rect.left = collision.rect.left - 36
                                pipe.rect.top = collision.rect.top
                            elif left < 0 and abs(top) < abs(left):
                                pipe.rect.left = collision.rect.left + 36
                                pipe.rect.top = collision.rect.top
                pipe.update()

            if game_win:
                for sprite in pipe_sprite_group:
                    sprite.remove()
                    sprite.kill()
                flow_sound.stop()
                if chance_for_straight > 45:
                    chance_for_straight = chance_for_straight - 1
                level_length = level_length + 1
                oozeby = 1
                first = True
                pipe_queue = random_level(
                    random_watermark=chance_for_straight,
                    level_length=level_length)
                game_win = False

            s_group.clear(screen, background)
            s_group.draw(screen)
            pygame.display.flip()

            clock.tick(40)

        loop = 0
        last_flood = 0
        while game_flood:
            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                    game_flood = False
            background = pygame.Surface(SCREENRECT.size)
            background.fill(Color("WHITE"))
            center_x = None
            center_y = None
            if last_laid_pipe:
                for sprite in last_laid_pipe:
                    center_x = sprite.rect.centerx
                    center_y = sprite.rect.centery

            if center_x and center_y:
                pygame.draw.rect(background, Color("YELLOW"), Rect(center_x - 20 * loop, center_y - 20 * loop, 40 * loop, 40 * loop))

            if pygame.time.get_ticks() - last_flood > 250:
                loop = loop +1
                last_flood = pygame.time.get_ticks()

            if loop * 40 > 1280:
                game_flood = False

            if not game_flood:
                for sprite in pipe_sprite_group:
                    sprite.remove()
                    sprite.kill()
                    background = pygame.Surface(SCREENRECT.size)
                    background.fill(Color("WHITE"))
                    flow_sound.stop()
                    game_menu = True
                    game_on = False
                    game_win = False
                    game_instructions = False
                    oozeby = 1
                    first = True
            screen.blit(background, (0, 0))
            s_group.clear(screen, background)
            s_group.draw(screen)
            pygame.display.flip()
            clock.tick(40)
        s_group.clear(screen, background)
        s_group.draw(screen)
        pygame.display.flip()

        clock.tick(40)

if __name__ == "__main__":
    main()
