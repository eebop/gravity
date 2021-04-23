import sys
import pygame
import numpy as np
import math
import random
import space_time
from data import data
import graphics
from gmath import distance
import time

FAST = True
PHYSICS = 'Newton'
PHYSICS_OPTIONS = ('Newton',)
if PHYSICS.title() not in map(lambda o: o.title(), PHYSICS_OPTIONS):
    sys.exit(f'Invalid physics type: {PHYSICS}.\nValid types are: {PHYSICS_OPTIONS}.')
PHYSICS = PHYSICS.title()

if PHYSICS == 'Newton':
    G = 6.67e-11

if PHYSICS == 'Einstein':
    C = 2.998e+4
    K = 8 * math.pi * 6.67e-11 / (C ** 4)
    LAMBDA = 1.1056e+52
    raise NotImplementedError

pygame.display.set_caption(f"Gravity - {PHYSICS}")



DISPLAY_SIZE = (0, 0)
pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)

print(screen.get_size())


class body:
    def __init__(self, location, momentum, mass, color=None):
        if not color:
            color = tuple(np.random.random_sample((3,)) * 255)
        self.color = color
        self.location = np.array(location, dtype=float)
        self.momentum = np.array(momentum, dtype=float)
        self.mass = float(mass)

    def update(self, locs, masses):


        if len(locs):
            direction = (self.location + ([self.gsize()/2] * 2 + [0])) - (locs + self.gsize_all(masses)/2)
            force = self.gravity(masses, self.get_distance(direction))
            direction_matrix = np.copysign(direction ** 2, -direction).T / np.sum(direction ** 2, 1)
            self.momentum += np.sum(direction_matrix * force, 1) / data.SPEED
        self.location += self.momentum / data.SPEED

    def get_distance(self, loc):
        return np.sqrt(np.sum(loc ** 2, 1))

    def gravity(self, m, r):
        # it should be m1 * m2, but that cancels out, so to optimize everything, I'm just using one mass
        return np.min((r, G * m / (r ** 2)), 0)

    def gsize_all(self, masses):
        volume = self.volume(masses)
        answer = (volume * 3 / (4 * math.pi)) ** (1/3) / 100
        return np.array((answer, answer, [0] * len(answer))).T


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
            if data.ALLOWTRACE:
                if len(graphics.vtracer[si]) >= 2:
                    graphics.extra.append(graphics.vtracer[si])
                if len(graphics.vtracer[oi]) >= 2:
                    graphics.extra.append(graphics.vtracer[oi])
                del graphics.vtracer[si]
                del graphics.vtracer[oi]
            del objects[objects.index(self)]
            del objects[objects.index(other)]
            mass = self.mass + other.mass
            sp = self.mass / mass
            op = other.mass / mass
            loc = ((sp * (self.location + ([self.gsize()/2] * 2 + [0]))) + (op * (other.location + ([other.gsize()/2] * 2 + [0])))) - ([self.gsize(mass)/2] * 2 + [0])
            momentum = (sp * self.momentum) + (op * other.momentum)
            color = tuple((sp * np.array(self.color, dtype=float)) + (op * np.array(other.color, dtype=float)))
            objects.append(body(loc, momentum, mass, color))
        except (ValueError, IndexError):
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
(body((800, 780, 0), (-7.4, 0, 0), 1e+14), body((800, 820, 0), (7.4, 0, 0), 1e+14), body((500, 800, 0), (0, 5.7, 0), 1e+14), body((1100, 800, 0), (0, -5.7, 0), 1e+14)),
(body((800, 800, 0), (0, 0, -10), 1e+16), body((700, 700, 0), (-40, 40, 0), 1e+14))
]
objects = SAVES[0]


objects = list(objects)
tick = 0
old_time = time.time()
average = []
while True:
    new_time = time.time()
    average.append(new_time - old_time)
    old_time = new_time
    colisions = set()
    locs = np.array([x.location for x in objects])
    masses = np.array([x.mass for x in objects])
    indexes = np.arange(len(objects))

    for count, o in enumerate(objects):
        o.update(locs[indexes!=count], masses[indexes!=count])
    for self in objects:
        for item in objects:
            if self != item and distance(self.location, item.location) < (self.gsize(self.mass) + self.gsize(item.mass)):
                add = True
                for c in colisions:
                    if self in c:
                        add = False
                        break
                if add:
                    colisions.add((self, item))

    events = pygame.event.get()
    [sys.exit() for e in events if e.type == pygame.QUIT]
    screen.fill((0, 0, 0))
    graphics.draw(screen, *zip(*map((lambda o: (o.location, o.gsize(), o.color, o.mass)), objects)), events)
    pygame.image.save(screen, 'pic%s.png' % tick)
    tick += 1
    #print(sum(average)/len(average))
    pygame.display.flip()
    for c in colisions:
        c[0].colide(objects, c[1])
