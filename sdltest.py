
import sdl2.ext

sdl2.ext.init()
window = sdl2.ext.Window("Hello World!", size=(800, 500))
window.show()

processor = sdl2.ext.TestEventProcessor()
processor.run(window)
