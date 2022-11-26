import pyglet
from generate import *
from play import *

w = pyglet.window.Window(resizable=True)

buttons_list = list(spritesheet("buttons.png", 3, 2))
l = List(w, [buttons_list[0], buttons_list[1]])
g = Grid(100, 100)

@w.event
def on_draw():
    w.clear()
    g.draw(w.width, w.height-l.bg.height)
    l.draw()

@w.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    g.set_scale(g.scale + 0.1 * scroll_y, x, y)

@w.event       
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    g.move(dx, dy)

@w.event
def on_mouse_motion(x, y, dx, dy):
    for b in l.buttons:
        b.check_mouse_over(x, y)

@w.event
def on_mouse_press(x, y, button, modifiers):
    action = None
    for b in l.buttons:
        a = b.check_mouse_over(x, y, True)
        action = a if a != None else action
    match action:
        case "quit":
            w.close()
        case "road":
            pass
        case None:
            pass

@w.event
def on_resize(w, h):
    l.update(w, h)

pyglet.app.run()