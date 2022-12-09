import pyglet
from typing import Union
from pathlib import Path



class Button:
    def __init__(self, image, x, y, width, action, image_mouse_on=None, image_pressed=None):
        self.sprite = pyglet.sprite.Sprite(image, x, y)
        # self.sprite.scale = width / self.sprite.width
        self.forms = [image, image_mouse_on, image_pressed]
        self.action = action
        self.x = x
        self.y = y

    def check_mouse_over(self, x:int=0, y:int=0, pressed:bool=False):
        if x > self.sprite.x and x < self.sprite.x + self.sprite.width and y > self.sprite.y and y < self.sprite.y + self.sprite.height:
            if not pressed:
                self.sprite.image = self.forms[1]
            else:
                return self.action
        else:
            if not self.sprite.image == self.forms[0]:
                self.sprite.image = self.forms[0]

    def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw()




class TopList:
    def __init__(self, window:pyglet.window.Window, items:list[Button]=[], item_width:int=64, padding:int=5, place:str="top", color:tuple[int, int, int]=(200, 200, 200)):
        self.bg = pyglet.shapes.Rectangle(0, 0, 0, 0, color)
        self.buttons = items
        self.item_width = item_width
        self.padding = padding
        self.place = place
        self.window = window
        self.update(window.width, window.height)
        buttons = ["road", "map ", "quit"]    # THIS MAY RAISE AN ERROR - just add new command
        for n, i in enumerate(self.buttons):
            i.sprite.scale = 0.5
            i.action = buttons[n]
    
    def draw(self):
        self.bg.draw()
        for i in self.buttons:
            i.draw()

    def _update_buttons(self, w, h):
        in_row = (w) // (self.item_width+self.padding)
        match self.place:
            case "top":
                self.bg.width = w
                self.bg.height = (len(self.buttons) // in_row + 1) * (self.item_width+self.padding) + self.padding
                self.bg.x = 0
                self.bg.y = self.window.height - self.bg.height

        for n, b in enumerate(self.buttons): 
            b.x = self.padding+(n%in_row)*(self.item_width+self.padding)
            b.y = h - self.item_width - (self.padding+(n//in_row)*(self.item_width+self.padding))

    def update(self, w, h):
        self.bg.y = h - self.bg.height
        self.bg.width = w
        self._update_buttons(w, h)



class SideList:
    def __init__(self, window:pyglet.window.Window, buttons:list[Button]=[], item_height:int=64, padding:int=2, color:tuple[int, int, int]=(100, 100, 100), opacity:int=50):
        self.buttons = buttons
        self.item_height = item_height
        self.padding = padding
        _height = len(buttons) * (item_height + padding) + padding
        self.bg = pyglet.shapes.Rectangle(0, window.height//2-_height//2, item_height+2*padding, _height, color)
        self.bg.opacity = opacity
        self.update(window.height)
        actions = ["++++", "----", "base"]
        for n, i in enumerate(self.buttons):
            i.action = actions[n]

    def update(self, h):
        self.bg.y = h//2 - self.bg.height//2
        for n, i in enumerate(self.buttons):
            i.x = self.padding
            i.y = self.bg.y + n*(self.padding+self.item_height)

    def draw(self):
        self.bg.draw()
        for i in self.buttons:
            i.draw()



def spritesheet(image:Union[str, Path], width:int=1, height:int=1):
    a = list(pyglet.image.ImageGrid(pyglet.image.load(image), height, width))
    for col in range(0, len(a)//height):
        yield Button(a[width+col], 0, 0, 0, "noe", image_mouse_on=a[col])

# print(list(spritesheet("S:\\Matysek\\_PROGRAMOVÁNÍ\\Python\\_hry\\_Transporter\\img\\buttons1.png", 3, 2)))