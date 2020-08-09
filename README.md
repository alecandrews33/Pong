# Pong
Pong implementation written in Python and run in SDL


Dependencies:

-PySDL2

-pysdl2-dll

-traitsui (and a GUI backend: e.g PyQt5, wxPython, or PySide2)

(all available on PyPi)



On mac run:

    defaults write -g ApplePressAndHoldEnabled -bool false
    
(prevents option to select accents from coming up when you hold down a key)




Good options for next steps:

1) add dashed line in middle for aesthetic (no collisions)

2) allow paddles to move horizontally

    - create a new airhockey mode for this (maybe eventually change goal size)

3) fix the delay after a score

4) make the score render on the screen (the pong tutorial gives a brief 
suggestion on how to do this) and not print to the command line

5) right now there is this BALL_SPEED variable that sets the initial speed of
the ball right when the game starts, I originally changed it in medium mode 
thinking a faster ball might make it harder, but then I added the ball reset
with a random velocity stuff after a score so now that change seems kind of 
pointless.  Should the initial ball speed be random too?

6) (Aaron can do later today) right now everything is in the pong file related 
to running the game.  We should pull out the game menu where games are selected
and run, and just like import the needed run functions (for now while eerything
is in python at least, eventually wont just be a run function, will be way to
run game in whatever form)





?) train the Pong Master AI 


