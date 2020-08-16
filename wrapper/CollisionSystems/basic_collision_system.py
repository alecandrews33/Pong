import sys
import sdl2
import sdl2.ext

import random
import time

from wrapper.MovementSystems.basic_movement_system import Velocity
from wrapper.GeneralGameClasses.player_data import PlayerData

class CollisionSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy, player1, player2):
        super(CollisionSystem, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.p1 = player1
        self.p2 = player2
        self.score = False
        self.scoredOnLeftSide = False
        self.displayscore1 = None 
        self.displayscore2 = None

    def _overlap(self, item):
        sprite = item[1]
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return (bleft < right and bright > left and
                btop < bottom and bbottom > top)

    def ball_score(self, scoredOnLeftSide, componentsets):
        self.score = True
        self.scoredOnLeftSide = scoredOnLeftSide
        if (scoredOnLeftSide):
            self.p2.playerdata.points += 1
        else:
            self.p1.playerdata.points += 1
        self.displayscore1.sprite = self.displayscore1.factory.from_text(str(self.p1data.points),fontmanager=self.displayscore1.fontmanager)
        self.displayscore2.sprite = self.displayscore2.factory.from_text(str(self.p2data.points),fontmanager=self.displayscore2.fontmanager)
        print("Player 1: {0}, Player 2: {1}".format(self.p1.playerdata.points, self.p2.playerdata.points))
        self.ball.sprite.position = 390, 290
        self.ball.velocity.vx = 0
        self.ball.velocity.vy = 0
        self.p1.sprite.position = 0, 250
        self.p2.sprite.position = 780, 250

    def process(self, world, componentsets):
        if (not self.score):
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
                self.ball_score(True, componentsets)
            elif self.ball.sprite.x + self.ball.sprite.size[0] >= self.maxx:
                self.ball_score(False, componentsets)
        else:
            self.score = False
            time.sleep(1)
            if (self.scoredOnLeftSide):
                self.ball.velocity.vx = -3
            else:
                self.ball.velocity.vx = 3
