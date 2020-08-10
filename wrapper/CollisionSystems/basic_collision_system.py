import sys
import sdl2
import sdl2.ext

import random
import time

from wrapper.MovementSystems.basic_movement_system import Velocity
from wrapper.GeneralGameClasses.player_data import PlayerData

class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy, p1data, p2data):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.p1data = p1data
        self.p2data = p2data

    def _overlap(self, item):
        sprite = item[1]
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return (bleft < right and bright > left and
                btop < bottom and bbottom > top)

    def ball_score(direction):
        if (sign(direction) < 1):
            self.p2data.points += 1
        else:
            self.p1data.points += 1
        print("Player 1: {0}, Player 2: {1}".format(self.p1data.points, self.p2data.points))
        self.ball.sprite.position = 390, 290
        self.ball.velocity.vx = 0
        self.ball.velocity.vy = 0
        time.sleep(2)
        self.ball.velocity.vx = sign(direction) * 3
        self.ball.velocity.vy = 0

    def process(self, world, componentsets):
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if len(collitems) != 0:
            self.ball.velocity.vx = -self.ball.velocity.vx

            sprite = collitems[0][1]
            ballcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
            halfheight = sprite.size[1] // 2
            stepsize = halfheight // 10
            degrees = 0.7
            paddlecentery = sprite.y + halfheight
            if ballcentery < paddlecentery:
                factor = (paddlecentery - ballcentery) // stepsize
                self.ball.velocity.vy = -int(round(factor * degrees))
            elif ballcentery > paddlecentery:
                factor = (ballcentery - paddlecentery) // stepsize
                self.ball.velocity.vy = int(round(factor * degrees))
            else:
                self.ball.velocity.vy = -self.ball.velocity.vy

        if (self.ball.sprite.y <= self.miny or
            self.ball.sprite.y + self.ball.sprite.size[1] >= self.maxy):
            self.ball.velocity.vy = -self.ball.velocity.vy


        if self.ball.sprite.x <= self.minx:
            ball_score(-1)
        elif self.ball.sprite.x + self.ball.sprite.size[0] >= self.maxx:
            ball_score(1)
