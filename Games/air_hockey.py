"""Air Hockey Game."""
import os

import sys
import sdl2
import sdl2.ext

from wrapper.MovementSystems.air_hockey_movement_system import *
from wrapper.CollisionSystems.air_hockey_collision_system import *
from wrapper.Renderers.basic_software_renderer import *
from wrapper.CPUplayers.air_hockey_AI import *

BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
BALL_SPEED = 3
PADDLE_SPEED = 3


class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0, ai=False):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()
        self.playerdata = PlayerData(ai)


class Ball(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()

class Midline(sdl2.ext.Entity):
    def __init__(self, world, sprite):
        self.sprite = sprite
        self.sprite.position = 398, 0

class DisplayScore1(sdl2.ext.Entity):
    def __init__(self, world, score, factory, fontmanager):
        self.spritefactory = factory
        self.fontmanager = fontmanager
        self.sprite = factory.from_text(str(score),fontmanager=fontmanager, size=30)
        self.sprite.position = 336, 40

class DisplayScore2(sdl2.ext.Entity):
    def __init__(self, world, score, factory, fontmanager):
        self.spritefactory = factory
        self.fontmanager = fontmanager
        self.sprite = factory.from_text(str(score),fontmanager=fontmanager, size=30)
        self.sprite.position = 448, 40

class AirHockeyGame():
    def run(game_info):
        sdl2.ext.init()
        window = sdl2.ext.Window("Air Hockey Game", size=(800, 600))
        window.show()


        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

        # Create the paddles - we want white ones. To keep it easy enough for us,
        # we create a set of surfaces that can be used for Texture- and
        # Software-based sprites.
        sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
        sp_paddle2 = factory.from_color(WHITE, size=(20, 100))
        sp_ball = factory.from_color(WHITE, size=(20, 20))
        sp_midline = factory.from_color(WHITE, size=(4, 600))

        world = sdl2.ext.World()

        movement = MovementSystemAirHockey(0, 0, 800, 600, 400)
        movement.paddle1 = sp_paddle1
        movement.paddle2 = sp_paddle2
        spriterenderer = SoftwareRenderSystem(window)

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../wrapper/Fonts/battle_star/Battle Star.ttf')
        fontmanager = sdl2.ext.FontManager(font_path=os.path.join(dirname, filename))


        world.add_system(movement)
        world.add_system(spriterenderer)
        #world.add_componenttype(sdl2.ext.SpriteFactory)

        # add a midline for aesthetic
        midline = Midline(world, sp_midline)


        if game_info.num_players == 1:
            if game_info.difficulty == 'Easy':
                PADDLE_SPEED_AI = 3
                BALL_SPEED = 3
            elif game_info.difficulty == 'Medium':
                PADDLE_SPEED_AI = 5
                BALL_SPEED = 4
            # Eventually this else will handle a much better AI
            else:
                PADDLE_SPEED_AI = 3
                BALL_SPEED = 3

            aicontroller = TrackingAIController(0, 600, PADDLE_SPEED_AI)
            world.add_system(aicontroller)

            ball = Ball(world, sp_ball, 390, 290)
            ball.velocity.vx = -BALL_SPEED
            aicontroller.ball = ball


            player1 = Player(world, sp_paddle1, 0, 250)
            player2 = Player(world, sp_paddle2, 780, 250, True)

            displayscore1 = DisplayScore1(world, player1.playerdata.points, factory, fontmanager)
            displayscore2 = DisplayScore2(world, player2.playerdata.points, factory, fontmanager)

            collision = CollisionSystem(0, 0, 800, 600, player1, player2)
            world.add_system(collision)
            collision.ball = ball

            collision.displayscore1 = displayscore1
            collision.displayscore2 = displayscore2

            running = True
            while running:
                for event in sdl2.ext.get_events():
                    if event.type == sdl2.SDL_QUIT:
                        running = False
                        break
                    if event.type == sdl2.SDL_KEYDOWN:
                        if event.key.keysym.sym == sdl2.SDLK_UP:
                            player1.velocity.vy = -PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                            player1.velocity.vy = PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                            player1.velocity.vx = -PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                            player1.velocity.vx = PADDLE_SPEED
                    elif event.type == sdl2.SDL_KEYUP:
                        if event.key.keysym.sym in (sdl2.SDLK_UP,
                                                    sdl2.SDLK_DOWN,
                                                    sdl2.SDLK_LEFT,
                                                    sdl2.SDLK_RIGHT):
                            player1.velocity.vy = 0
                            player1.velocity.vx = 0
                sdl2.SDL_Delay(10)
                world.process()

        else:
            BALL_SPEED = 3
            ball = Ball(world, sp_ball, 390, 290)
            ball.velocity.vx = -BALL_SPEED

            player1 = Player(world, sp_paddle1, 0, 250)
            player2 = Player(world, sp_paddle2, 780, 250)

            displayscore1 = DisplayScore1(world, player1.playerdata.points, factory, fontmanager)
            displayscore2 = DisplayScore2(world, player2.playerdata.points, factory, fontmanager)

            collision = CollisionSystem(0, 0, 800, 600, player1, player2)
            world.add_system(collision)
            collision.ball = ball

            collision.displayscore1 = displayscore1
            collision.displayscore2 = displayscore2

            running = True
            while running:
                for event in sdl2.ext.get_events():
                    if event.type == sdl2.SDL_QUIT:
                        running = False
                        break
                    if event.type == sdl2.SDL_KEYDOWN:
                        if event.key.keysym.sym == sdl2.SDLK_w:
                            player1.velocity.vy = -PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_s:
                            player1.velocity.vy = PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_a:
                            player1.velocity.vx = -PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_d:
                            player1.velocity.vx = PADDLE_SPEED

                        if event.key.keysym.sym == sdl2.SDLK_UP:
                            player2.velocity.vy = -PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                            player2.velocity.vy = PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                            player2.velocity.vx = -PADDLE_SPEED
                        elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                            player2.velocity.vx = PADDLE_SPEED
                    elif event.type == sdl2.SDL_KEYUP:
                        if event.key.keysym.sym in (sdl2.SDLK_w, sdl2.SDLK_s, sdl2.SDLK_a, sdl2.SDLK_d):
                            player1.velocity.vy = 0
                            player1.velocity.vx = 0
                        if event.key.keysym.sym in (sdl2.SDLK_UP,
                                                    sdl2.SDLK_DOWN,
                                                    sdl2.SDLK_LEFT,
                                                    sdl2.SDLK_RIGHT):
                            player2.velocity.vy = 0
                            player2.velocity.vx = 0
                sdl2.SDL_Delay(10)
                world.process()
