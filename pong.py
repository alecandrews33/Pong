"""The Pong Game."""
import sys
import sdl2
import sdl2.ext

from traits.api import Enum, HasTraits
from traitsui.api import Item, OKCancelButtons, View

from wrapper.MovementSystems.basic_movement_system import *
from wrapper.CollisionSystems.basic_collision_system import *
from wrapper.Renderers.basic_software_renderer import *
from wrapper.CPUplayers.basicAI import *

BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
BALL_SPEED = 3
PADDLE_SPEED = 3


class GameInfo(HasTraits):
    num_players = Enum(1, 2)
    difficulty = Enum('Easy', 'Medium', 'Pong Master')

    view = View(Item(name='num_players'),
                Item(name='difficulty',
                     enabled_when='num_players == 1'),
                buttons = OKCancelButtons
                )



class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0, ai=False):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()
        self.playerdata = PlayerData()
        self.playerdata.ai = ai


class Ball(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()


def run(game_info):
    sdl2.ext.init()
    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    window.show()


    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    # Create the paddles - we want white ones. To keep it easy enough for us,
    # we create a set of surfaces that can be used for Texture- and
    # Software-based sprites.
    sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = factory.from_color(WHITE, size=(20, 100))
    sp_ball = factory.from_color(WHITE, size=(20, 20))

    world = sdl2.ext.World()

    movement = MovementSystem(0, 0, 800, 600)
    spriterenderer = SoftwareRenderSystem(window)


    world.add_system(movement)
    world.add_system(spriterenderer)


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

        collision = CollisionSystem(0, 0, 800, 600, player1.playerdata, player2.playerdata)
        world.add_system(collision)
        collision.ball = ball

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
                elif event.type == sdl2.SDL_KEYUP:
                    if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                        player1.velocity.vy = 0
            sdl2.SDL_Delay(10)
            world.process()

    else:
        BALL_SPEED = 3
        ball = Ball(world, sp_ball, 390, 290)
        ball.velocity.vx = -BALL_SPEED

        player1 = Player(world, sp_paddle1, 0, 250)
        player2 = Player(world, sp_paddle2, 780, 250)

        collision = CollisionSystem(0, 0, 800, 600, player1.playerdata, player2.playerdata)
        world.add_system(collision)
        collision.ball = ball

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

                    if event.key.keysym.sym == sdl2.SDLK_UP:
                        player2.velocity.vy = -PADDLE_SPEED
                    elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                        player2.velocity.vy = PADDLE_SPEED
                elif event.type == sdl2.SDL_KEYUP:
                    if event.key.keysym.sym in (sdl2.SDLK_w, sdl2.SDLK_s):
                        player1.velocity.vy = 0
                    if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                        player2.velocity.vy = 0
            sdl2.SDL_Delay(10)
            world.process()



if __name__ == "__main__":
    game_info = GameInfo()
    game_info.configure_traits()

    sys.exit(run(game_info))
