import sys
import sdl2
import sdl2.ext

class MovementSystemAirHockey(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy, midline):
        super(MovementSystemAirHockey, self).__init__()
        self.componenttypes = Velocity, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.midline = midline
        self.paddle1 = None
        self.paddle2 = None

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            if sprite == self.paddle1:
                swidth, sheight = sprite.size
                sprite.x += velocity.vx
                sprite.y += velocity.vy

                sprite.x = max(self.minx, sprite.x)
                sprite.y = max(self.miny, sprite.y)
                
                pmaxx = sprite.x + swidth
                pmaxy = sprite.y + sheight
                if pmaxx > self.midline:
                    sprite.x = self.midline - swidth
                if pmaxy > self.maxy:
                    sprite.y = self.maxy - sheight
            elif sprite == self.paddle2:
                swidth, sheight = sprite.size
                sprite.x += velocity.vx
                sprite.y += velocity.vy

                sprite.x = max(self.midline, sprite.x)
                sprite.y = max(self.miny, sprite.y)
                
                pmaxx = sprite.x + swidth
                pmaxy = sprite.y + sheight
                if pmaxx > self.maxx:
                    sprite.x = self.maxx - swidth
                if pmaxy > self.maxy:
                    sprite.y = self.maxy - sheight
            else:
                swidth, sheight = sprite.size
                sprite.x += velocity.vx
                sprite.y += velocity.vy

                sprite.x = max(self.minx, sprite.x)
                sprite.y = max(self.miny, sprite.y)
                
                pmaxx = sprite.x + swidth
                pmaxy = sprite.y + sheight
                if pmaxx > self.maxx:
                    sprite.x = self.maxx - swidth
                if pmaxy > self.maxy:
                    sprite.y = self.maxy - sheight
                

class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0
