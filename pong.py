"""The Pong Game."""
import sys
import sdl2
import sdl2.ext

import traitsui.api

from .wrapper.MovementSystems.basic_movement_system import MovementSystem
from .wrapper.CollisionSystems.basic_collision_system import CollisionSystem
from .wrapper.Renderers.basic_software_renderer import SoftwareRenderSystem
from .wrapper.CPUplayers.basicAI import TrackingAIController




BLACK = sdl2.ext.Color(0, 0, 0)
WHITE = sdl2.ext.Color(255, 255, 255)
PADDLE_SPEED = 3
BALL_SPEED = 3


class GameInfo(HasTraits):
    num_players = Enum(1, 2)
    difficulty = Enum('Easy', 'Medium', 'Pong Master')




def run(game_info):
    sdl2.ext.init()
    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    window.show()

    if "-hardware" in sys.argv:
        print("Using hardware acceleration")
        renderer = sdl2.ext.Renderer(window)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    else:
        print("Using software rendering")
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    # Create the paddles - we want white ones. To keep it easy enough for us,
    # we create a set of surfaces that can be used for Texture- and
    # Software-based sprites.
    sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = factory.from_color(WHITE, size=(20, 100))
    sp_ball = factory.from_color(WHITE, size=(20, 20))

    world = sdl2.ext.World()

    movement = MovementSystem(0, 0, 800, 600)
    collision = CollisionSystem(0, 0, 800, 600)
    aicontroller = TrackingAIController(0, 600)
    if factory.sprite_type == sdl2.ext.SOFTWARE:
        spriterenderer = SoftwareRenderSystem(window)
    else:
        spriterenderer = TextureRenderSystem(renderer)

    world.add_system(aicontroller)
    world.add_system(movement)
    world.add_system(collision)
    world.add_system(spriterenderer)

    ball = Ball(world, sp_ball, 390, 290)
    ball.velocity.vx = -BALL_SPEED
    collision.ball = ball
    aicontroller.ball = ball

    if game_info.num_players == 1:
        player1 = Player(world, sp_paddle1, 0, 250)
        player2 = Player(world, sp_paddle2, 780, 250, True)

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
        player1 = Player(world, sp_paddle1, 0, 250)
        player2 = Player(world, sp_paddle2, 780, 250)

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



if __name__ == "__main__":
    game_info = GameInfo()
    game_info.configure_traits()

    sys.exit(run(game_info))
