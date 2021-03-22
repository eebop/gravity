import sys
import numpy as np

class Data:
    def __init__(self):
        self.SPEED = 10
        ZOOM = [x.split('=')[1] for x in sys.argv if '-z' in x and '=' in x]
        if ZOOM:
            self.ZOOM = float(Z[-1])
        else:
            self.ZOOM = 1

        ALLOW = [x.split('=')[1] for x in sys.argv if '-a' in x and '=' in x]
        if ALLOW:
            self.ALLOWTRACE = int(ALLOW[-1])
        else:
            self.ALLOWTRACE = 1

        TRACE = [x.split('=')[1] for x in sys.argv if '-t' in x and '=' in x]
        if TRACE and self.ALLOWTRACE:
            self.TRACE = int(TRACE[-1])
        else:
            self.TRACE = self.ALLOWTRACE

        SPACETIME = [x.split('=')[1] for x in sys.argv if '-s' in x and '=' in x]
        if SPACETIME and self.ALLOWTRACE:
            self.SPACETIME = int(SPACETIME[-1])
        else:
            self.SPACETIME = self.ALLOWTRACE

        self.ADD = np.array((0, 0))

data = Data()
