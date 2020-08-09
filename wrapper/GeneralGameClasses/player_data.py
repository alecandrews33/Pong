import sys
import sdl2
import sdl2.ext


class PlayerData(object):
    def __init__(self):
        super(PlayerData, self).__init__()
        self.ai = False
        self.points = 0
