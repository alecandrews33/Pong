import sys
import sdl2
import sdl2.ext

from traits.api import Enum, HasTraits
from traitsui.api import Item, OKCancelButtons, View


# import other games here
from Games.air_hockey import AirHockeyGame
from Games.pong2 import PongGame
from Games.hello_world import HelloWorldGame

class GameInfo(HasTraits):
    game_mode = Enum('Classic Pong', 'Hello World', 'Air Hockey')
    num_players = Enum(1, 2)
    difficulty = Enum('Easy', 'Medium', 'Pong Master')

    view = View(Item(name='game_mode'),
                Item(name='num_players'),
                Item(name='difficulty',
                     enabled_when='num_players == 1'),
                buttons = OKCancelButtons
                )


# basically now in order to add a new game all we need to do is make a class
# for that game and make it have a run method that accepts game info. Actually
# the requirement is probably looser than that, it just needs to be importable
# and runable from inside this script


if __name__ == "__main__":
    game_info = GameInfo()
    game_info.configure_traits()

    if game_info.game_mode == 'Classic Pong':
        sys.exit(PongGame.run(game_info))
    elif game_info.game_mode == 'Hello World':
        sys.exit(HelloWorldGame.run(game_info))
    elif game_info.game_mode == 'Air Hockey':
        sys.exit(AirHockeyGame.run(game_info))
