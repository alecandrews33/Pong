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


Ross

add dashed line in middle for aesthetic (no collisions)

Alec

fix the delay after a score -> return paddles to the center

Aaron

make the score render on the screen (the pong tutorial gives a brief 
suggestion on how to do this) and not print to the command line


2) allow paddles to move horizontally

    - create a new airhockey mode for this (maybe eventually change goal size)

?) train the Pong Master AI 


