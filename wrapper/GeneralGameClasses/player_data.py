import sys
import sdl2
import sdl2.ext


class PlayerData(object):
    def __init__(self, ai):
        super(PlayerData, self).__init__()
        self.ai = ai
        self.points = 0
