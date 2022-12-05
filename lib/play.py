import pyglet
from typing import Union
from pathlib import Path

class List:
    def __init__(self, window:pyglet.window.Window, items:list=[], item_width:int=64, padding:int=5, place:str="top", color:tuple[int, int, int]=(200, 200, 200)):
        self.bg = pyglet.shapes.Rectangle(0, 0, 0, 0, color)
        self.items = items
        self.item_width = item_width
        self.padding = padding
        self.place = place
        self.window = window
    
    def draw(self):
        self.bg.draw()
        for i in self.buttons:
            i.draw()

    def _update_buttons(self, w, h):
        in_row = (w) // (self.item_width+self.padding)
        buttons = ["road", "quit"]
        match self.place:
            case "top":
                self.bg.width = w
                self.bg.height = (len(self.items) // in_row + 1) * (self.item_width+self.padding) + self.padding
                self.bg.x = 0
                self.bg.y = self.window.height - self.bg.height
        self.buttons = [Button(
            image = x[0],
            x = self.padding+(n%in_row)*(self.item_width+self.padding), 
            y = h - self.item_width - (self.padding+(n//in_row)*(self.item_width+self.padding)), 
            width = self.item_width, 
            action = buttons[n],
            image_mouse_on = x[1]) for n, x in enumerate(self.items)]

    def update(self, w, h):
        self.bg.y = h - self.bg.height
        self.bg.width = w
        self._update_buttons(w, h)

def spritesheet(image:Union[str, Path], width:int=1, height:int=1):
    a = list(pyglet.image.ImageGrid(pyglet.image.load(image), height, width))
    for row in range(0, len(a)//height):
        yield [a[row+x*width] for x in range(len(a)//width)][::-1]

class Button:
    def __init__(self, image, x, y, width, action, image_mouse_on=None, image_pressed=None):
        self.sprite = pyglet.sprite.Sprite(image, x, y)
        self.sprite.scale = width / self.sprite.width
        self.forms = [image, image_mouse_on, image_pressed]
        self.action = action

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
        self.sprite.draw()