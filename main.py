import pyglet
from lib.generate import *
from lib.play import *
from lib.transport import *

w = pyglet.window.Window(resizable=True)

buttons1_list = list(spritesheet("img/buttons1.png", 4, 2))
buttons2_list = list(spritesheet("img/buttons2.png", 3, 2))
l = TopList(w, [buttons1_list[0], buttons1_list[3], buttons1_list[1]])
s = SideList(w, buttons2_list)
g = Grid(100, 100)

# c = Car1("car1.png", 10)

@w.event
def on_draw():
    w.clear()
    g.draw(w.width, w.height-l.bg.height)
    l.draw()
    s.draw()
    # c.draw()

@w.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    g.move(dx, dy)

@w.event
def on_mouse_motion(x, y, dx, dy):
    for b in l.buttons:
        b.check_mouse_over(x, y)
    for b in s.buttons:
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
    print(action)

@w.event
def on_resize(w, h):
    l.update(w, h)

@w.event
def on_key_press(sym, m):
    if sym == 65453:
        g.set_scale(g.scale - 0.5, w.width//2, w.height//2)
    elif sym == 65451:
        g.set_scale(g.scale + 0.5, w.width//2, w.height//2)

pyglet.app.run()