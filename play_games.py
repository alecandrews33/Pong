import sys
import sdl2
import sdl2.ext

from traits.api import Enum, HasTraits
from traitsui.api import Item, OKCancelButtons, View


# import other games here
from pong2 import PongGame

class GameInfo(HasTraits):
    game_mode = Enum('Classic Pong')
    num_players = Enum(1, 2)
    difficulty = Enum('Easy', 'Medium', 'Pong Master')
    
    view = View(Item(name='game_mode'),
                Item(name='num_players'),
                Item(name='difficulty',
                     enabled_when='num_players == 1'),
                buttons = OKCancelButtons
                )


if __name__ == "__main__":
    game_info = GameInfo()
    game_info.configure_traits()

    if game_info.game_mode == 'Classic Pong':
        sys.exit(PongGame.run(game_info))
