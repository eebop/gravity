from data import data
import space_time
import numpy as np
import pygame

VIEW_DIRECTION = np.array([
[1, 0, 0],
[0, 1, 0],
[0, 0, 1]],
dtype=float)

pause = pygame.Surface((50, 50))
pause.set_colorkey((0, 0, 0))
#pygame.draw.polygon(pause, (255, 0, 0), ((0, 0), (0, 50), (50, 25)))

play = pygame.Surface((50, 50))
play.set_colorkey((0, 0, 0))
pygame.draw.rect(play, (0, 255, 0), [0, 0, 15, 50])
pygame.draw.rect(play, (0, 255, 0), [32, 0, 15, 50])

on = pygame.Surface((25, 25))
on.set_colorkey((0, 0, 0))
pygame.draw.circle(on, (0, 255, 0), (12, 12), 12)

off = pygame.Surface((25, 25))
off.set_colorkey((0, 0, 0))
pygame.draw.circle(off, (128, 128, 128), (12, 12), 12)

bar = pygame.Surface((200, 25))
bar.fill((200, 200, 200))

slider = pygame.Surface((12, 100))
slider.fill((255, 0, 0))

nothing = pygame.Surface((1, 1))
nothing.set_colorkey((0, 0, 0))


def get_tracer_image(t):
    if data.ALLOWTRACE:
        if (data.TRACE and t == 0):
            return on
        elif (data.SPACETIME and t == 1):
            return on
        return off
    return nothing

m_motion = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

def paused(screen, l, s, c, m):
    done = False
    while not done:
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        draw(screen, l, s, c, m, events, False)
        screen.blit(play, (75, 0))
        screen.blit(get_tracer_image(0), (150, 12))
        screen.blit(get_tracer_image(1), (200, 12))
        screen.blit(bar, (75, 112))
        screen.blit(slider, (data.ZOOM*100+75, 75))
        [sys.exit() for e in events if e.type == pygame.QUIT]
        mousedown = [x.pos for x in events if x.type == pygame.MOUSEBUTTONDOWN]
        mouseup = [x.pos for x in events if x.type == pygame.MOUSEBUTTONUP]
        keydown = [x.text for x in events if x.type == pygame.TEXTINPUT and x.text in 'wasd gt']

        for loc in mousedown:
            if (75 < loc[0] < 125) and (0 < loc[1] < 50):
                done = True

            if (150 < loc[0] < 175) and (12 < loc[1] < 37):
                data.TRACE = not data.TRACE

            if (200 < loc[0] < 225) and (12 < loc[1] < 37):
                data.SPACETIME = not data.SPACETIME


            if (75 < loc[0] < 275) and (75 < loc[1] < 175):
                data.ZOOM = ((loc[0]-75) / 100)

        for loc in mouseup:
            if (75 < loc[0] < 275) and (75 < loc[1] < 175):
                data.ZOOM = ((loc[0]-75) / 100)

        for text in keydown:
            if text == ' ':
                pygame.display.flip()
                return
        pygame.display.flip()


def info(screen, locations, sizes, colors, masses, events):
    screen.blit(pause, (75, 0))
    mouse = [x.pos for x in events if x.type == pygame.MOUSEBUTTONDOWN]
    for loc in mouse:
        if (75 < loc[0] < 125) and (0 < loc[1] < 50):
            return paused(screen, locations, sizes, colors, masses)



def view(screen, locations, sizes, colors, masses, events, info_draw=True):
    keydown = [x.text for x in events if x.type == pygame.TEXTINPUT and (x.text in 'wasdgt' or (x.text == ' ' and info_draw))]


    for key in keydown:
        if key == ' ':
            return paused(screen, locations, sizes, colors, masses)
        else:
            data.ADD += m_motion[key]


    vectors = VIEW_DIRECTION
    l = []
    for loc in locations:
        l.append(np.sum(vectors * (loc), 1))


    l.sort(key=lambda o: o[2])
    for loc, size, color, num in zip(l, sizes, colors, range(len(l))):
        if data.ALLOWTRACE:
            if len(vtracer) > num:
                iloc = (loc[:2].astype(dtype=int),)
                if not (iloc[0] == vtracer[-1]).all():
                    vtracer[num] = np.concatenate((vtracer[num], iloc))
            else:
                vtracer.append(np.array((loc[:2],), dtype=int))
        pygame.draw.circle(screen, color, loc[:2]*data.ZOOM+data.ADD, (size + (loc[2]/10))*data.ZOOM)

        if data.ALLOWTRACE and data.TRACE:
            for loc in (vtracer+extra):
                if len(loc) >= 2:
                    pygame.draw.lines(screen, (255, 0, 0), False, loc*data.ZOOM+data.ADD)
    if info_draw:
        info(screen, locations, sizes, colors, masses, events)

vtracer = []
extra = []

def draw(screen, l, s, c, m, events, info_draw=True):
    if data.SPACETIME:
        space_time.draw(screen, l, m)
    view(screen, l, s, c, m, events, info_draw)
