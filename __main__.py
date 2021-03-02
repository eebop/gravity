import sys
import pygame
import numpy as np
import time
import math
import random

PHYSICS = 'Newton'
PHYSICS_OPTIONS = ('Newton',)
if PHYSICS.title() not in map(lambda o: o.title(), PHYSICS_OPTIONS):
    sys.exit(f'Invalid physics type: {PHYSICS}.\nValid types are: {PHYSICS_OPTIONS}.')
PHYSICS = PHYSICS.title()

if PHYSICS == 'Newton':
    G = 6.67e-11

if PHYSICS == 'Einstein':
    K = 8 * math.pi * 6.67e-11 / 2.998e+4


class Data:
    def __init__(self):
        self.SPEED = 1/1000000
        Z = [x.split('=')[1] for x in sys.argv if '-z' in x]
        if Z:
            self.ZOOM = int(Z[-1])
        else:
            self.ZOOM = 1

        ALLOW = [x.split('=')[1] for x in sys.argv if '-a' in x]
        if ALLOW:
            self.ALLOWTRACE = int(ALLOW[-1])
        else:
            self.ALLOWTRACE = 1

        TRACE = [x.split('=')[1] for x in sys.argv if '-t' in x]
        if TRACE and self.ALLOWTRACE:
            self.TRACE = int(TRACE[-1])
        else:
            self.TRACE = self.ALLOWTRACE

        self.ADD = np.array((0, 0))

DISPLAY_SIZE = (0, 0)
pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)


data = Data()

VIEW_DIRECTION = np.array([
[1, 0, 0],
[0, 1, 0],
[0, 0, 1]],
dtype=float)

pause = pygame.Surface((50, 50))
pause.set_colorkey((0, 0, 0))
pygame.draw.polygon(pause, (255, 0, 0), ((0, 0), (0, 50), (50, 25)))

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


def get_tracer_image():
    if data.ALLOWTRACE:
        if data.TRACE:
            return on
        return off
    return nothing

m_motion = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

def paused(screen):
    done = False
    l, g, c = zip(*map((lambda o: (o.location, o.gsize(), o.color)), objects))
    while not done:
        view(screen, l, g, c, [], False)
        events = pygame.event.get()
        screen.blit(play, (75, 0))
        screen.blit(get_tracer_image(), (150, 12))
        screen.blit(bar, (75, 112))
        screen.blit(slider, (data.ZOOM*100+75, 75))
        [sys.exit() for e in events if e.type == pygame.QUIT]
        mousedown = [x.pos for x in events if x.type == pygame.MOUSEBUTTONDOWN]
        mouseup = [x.pos for x in events if x.type == pygame.MOUSEBUTTONUP]
        keydown = [x.text for x in events if x.type == pygame.TEXTINPUT and x.text in 'wasd']

        for loc in mousedown:
            if (75 < loc[0] < 125) and (0 < loc[1] < 50):
                done = True

            if (150 < loc[0] < 175) and (12 < loc[1] < 37):
                data.TRACE = not data.TRACE

            if (75 < loc[0] < 275) and (75 < loc[1] < 175):
                data.ZOOM = ((loc[0]-75) / 100)

        for loc in mouseup:
            if (75 < loc[0] < 275) and (75 < loc[1] < 175):
                data.ZOOM = ((loc[0]-75) / 100)


        pygame.display.flip()



def info(screen, events):
    screen.blit(pause, (75, 0))
    mouse = [x.pos for x in events if x.type == pygame.MOUSEBUTTONDOWN]
    for loc in mouse:
        if (75 < loc[0] < 125) and (0 < loc[1] < 50):
            paused(screen)



def view(screen, locations, sizes, colors, events, info_draw=True):

    keydown = [x.text for x in events if x.type == pygame.TEXTINPUT and x.text in 'wasd']


    for key in keydown:
        data.ADD += m_motion[key]


    screen.fill((0, 0, 0))
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
        info(screen, events)
        pygame.display.flip()

vtracer = []
extra = []

class body:
    def __init__(self, location, momentum, mass, color=None):
        if not color:
            color = tuple(np.random.random_sample((3,)) * 255)
        self.color = color
        self.location = np.array(location, dtype=float)
        self.momentum = np.array(momentum, dtype=float)
        self.mass = float(mass)


    def update(self, items, colisions):
        items = [x for x in items if x != self]
        #print(self.location)
        for item in items:
            if (np.abs(item.location - self.location) < (self.gsize(self.mass) + self.gsize(item.mass))).all():
                add = True
                for c in colisions:
                    if self in c:
                        add = False
                        break
                if add:
                    colisions.add((self, item))
            direction = self.location - item.location
            force = self.gravity(self.mass, item.mass, self.get_distance(direction)) / self.mass
            direction_matrix = -direction / np.sum(np.abs(direction))
            self.momentum += (direction_matrix * (force / self.mass)) / data.SPEED
        self.location += self.momentum / data.SPEED


    def get_distance(self, loc):
        return math.sqrt(np.sum(loc ** 2))

    def gravity(self, m1, m2, r):
        try:
            return G * m1 * m2 / (r ** 2)
        except ZeroDivisionError:
            return 0 # do it next tick

    def gsize(self, mass=None):
        if mass == None:
            mass = self.mass
        volume = self.volume(mass)
        return max((volume * 3 / (4 * math.pi)) ** (1/3) / 100, 1) # zoom out

    def volume(self, mass):
        # Using the density of the earth
        return (1/5515) * mass

    def colide(self, objects, other):
        try:
            si = objects.index(self)
            oi = objects.index(other)
            if max((si, oi)) == oi:
                si, oi = oi, si
                # print(si, oi)
            if data.ALLOWTRACE:
                if len(vtracer[si]) >= 2:
                    # print('here')
                    extra.append(vtracer[si])
                if len(vtracer[oi]) >= 2:
                    extra.append(vtracer[oi])
                del vtracer[si]
                del vtracer[oi]
            del objects[objects.index(self)]
            del objects[objects.index(other)]
            mass = self.mass + other.mass
            sp = self.mass / mass
            op = other.mass / mass
            loc = (sp * self.location) + (op * other.location)
            momentum = (sp * self.momentum) + (op * other.momentum)
            color = tuple((sp * np.array(self.color, dtype=float)) + (op * np.array(other.color, dtype=float)))
            objects.append(body(loc, momentum, mass, color))
        except ValueError:
            pass # It colided with something else already, I'll colide next tick

def rand():
    num = 0#random.randrange(3, 7)
    r = []
    for x in range(num):
        m = 10 ** random.randrange(14, 17)
        l = (random.randrange(0, 1845), random.randrange(0, 1005), 0)
        s = (*(((np.random.random_sample(2)-.5) * 1/m) * 10 ** 9), 0)
        r.append(body(l, s, m))
    for x in range(200):
        m = 10 ** random.randrange(11, 16)
        l = (random.randrange(-100, 2100), random.randrange(-100, 1100), 0)
        s = (*((np.random.random_sample(2)-.5) * .00001), 0)
        r.append(body(l, s, m))

    return r

SAVES = [
(body((800, 800, 0), (0, 0, 0), 1e+15), body((950, 800, 0), (0, -.000002, 0), 1e+14), body((1200, 800, 0), (0, .000001, 0), 1e+14)),
(body((400, 400, 0), (0, .0000001, 0), 1e+15), body((550, 400, 0), (0, -.000002, 0), 1e+14), body((800, 400, 0), (0, .000004, 0), 1e+13)),
(body((800, 800, 0), (0, -.0000004, 0), 1e+14), body((600, 800, 0), (0, .0000004, 0), 1e+14)),
(body((800, 800, 0), (0, 0, 0), 1e+15), body((950, 800, 0), (0, -.000002, 0), 1e+14), body((1200, 800, 0), (0, .000001, 0), 1e+14), body((100, 800, 0), (0, .0000005, 0), 3e+14)),
(body((800, 800, 0), (0, .00000005, 0), 1e+15), body((950, 800, 0), (0, -.000002, 0), 1e+14), body((1200, 800, 0), (0, .000001, 0), 1e+14)),

]
objects = SAVES[0]


objects = list(objects)
try:
    while True:
        colisions = set()
        for o in objects:
            o.update(objects, colisions)
        events = pygame.event.get()
        [sys.exit() for e in events if e.type == pygame.QUIT]
        view(screen, *zip(*map((lambda o: (o.location, o.gsize(), o.color)), objects)), events)
        for c in colisions:
            c[0].colide(objects, c[1])
except KeyboardInterrupt:
    pass