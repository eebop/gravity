import numpy as np
import pygame
import sys
import math

SIZE = 2001
DISTANCE = 50
INTERVAL = 20

class VBody:
    def __init__(self, x, y):
        self.location = np.array((x, y, 0), dtype=float)
        self.default = (x, y)
        self.mass = 0
        self.main = x == y
        self.get0 = lambda o: o.location[0]
        self.get1 = lambda o: o.location[1]
        self.geta = lambda o: o.location[:2]

    def _build(self, x, ALL):
        if x:
            get = self.get0
        else:
            get = self.get1
        return [x for x in ALL if get(x) == get(self) and x is not self]

    def build(self, ALL):
        self.x = self._build(1, ALL)
        self.x.sort(key=self.get0)
        self.y = self._build(0, ALL)
        self.y.sort(key=self.get1)
        return True

    def update(self, locs, masses):
        if len(locs):
            direction = self.location - locs
            bd = np.array(np.sum(direction, 1), dtype=bool)
            masses = masses[bd]
            direction = direction[bd]
            force = self.gravity(masses, self.get_distance(direction))
            direction_matrix = -direction.T / np.sum(np.abs(direction), 1)
            self.location += np.sum(direction_matrix * force, 1)

    def get_distance(self, loc):
        return np.sqrt(np.sum(loc ** 2, 1))

    def gravity(self, m, r):
        return np.min((1e-10 * m / (r ** 2), r), 0)

    def draw(self, screen):
        pygame.draw.lines(screen, (50, 50, 200), False, sys.modules['__main__'].data.ZOOM*np.array(tuple(map(self.geta, self.x))) + sys.modules['__main__'].data.ADD)
        pygame.draw.lines(screen, (50, 50, 200), False, sys.modules['__main__'].data.ZOOM*np.array(tuple(map(self.geta, self.y))) + sys.modules['__main__'].data.ADD)

    def reset(self):
        self.location = np.array((*self.default, 0), dtype=float)

def draw(screen, locs, masses):
    tuple(map(lambda o:o.update(locs, np.array(masses, dtype=float)), ALL))
    tuple(map(lambda o:o.draw(screen), MAINS))
    tuple(map(lambda o:o.reset(), ALL))

MAINS = [VBody(x, x) for x in range(-100, SIZE, DISTANCE)]
ALL = [VBody(x, y) for x in range(-100, SIZE, INTERVAL) for y in range(-100, SIZE, DISTANCE) if (x % DISTANCE) and (x != y)] + [VBody(x, y) for x in range(-100, SIZE, DISTANCE) for y in range(-100, SIZE, INTERVAL) if (y % DISTANCE) and (x != y)] + MAINS
[x.build(ALL) for x in MAINS]
