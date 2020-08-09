import sys
import sdl2
import sdl2.ext

from wrapper.MovementSystems.basic_movement_system import Velocity

#PADDLE_SPEED = 3


class PlayerData(object):
    def __init__(self):
        super(PlayerData, self).__init__()
        self.ai = False
        self.points = 0

class TrackingAIController(sdl2.ext.Applicator):
    def __init__(self, miny, maxy, PADDLE_SPEED):
        super(TrackingAIController, self).__init__()
        self.componenttypes = PlayerData, Velocity, sdl2.ext.Sprite
        self.miny = miny
        self.maxy = maxy
        self.ball = None
        self.PADDLE_SPEED = PADDLE_SPEED

    def process(self, world, componentsets):
        for pdata, vel, sprite in componentsets:
            if not pdata.ai:
                continue

            sheight = sprite.size[1]
            centery = sprite.y + sheight // 2
            if self.ball.velocity.vx < 0:
                # ball is moving away from the AI
                if centery < self.maxy // 2 - self.PADDLE_SPEED:
                    vel.vy = self.PADDLE_SPEED
                elif centery > self.maxy // 2 + self.PADDLE_SPEED:
                    vel.vy = -self.PADDLE_SPEED
                else:
                    vel.vy = 0
            else:
                bcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
                if bcentery < centery:
                    vel.vy = -self.PADDLE_SPEED
                elif bcentery > centery:
                    vel.vy = self.PADDLE_SPEED
                else:
                    vel.vy = 0
