from typing import Literal, Union
from pathlib import Path as pth
from lib.generate import Grid
from math import sin, cos, radians
import pyglet

Path = Union[pth, str]

class Vehicle:
    _id = 0
    _batch = pyglet.graphics.Batch()

    def __init__(self, image:Path):
        self.MAX_CARGO_AMOUNT :int
        self.MAXIMUM_EXCEED   :Literal["not load", "error"]
        self.CAN_GO_THROUGH   :list[Literal["G", "W"]]
        self.PATH             :Literal["straight", "blocks"] = "blocks"
        
        self.id = Vehicle._id
        Vehicle._id += 1
        self.type = "non-specified vehicle"

        self.cargo_amount = 0

        self.image = pyglet.image.load(image)
        self.image.anchor_x = self.image.width//2
        self.image.anchor_y = self.image.height//2
        self.sprite = pyglet.sprite.Sprite(self.image, 32, 32, batch=Vehicle._batch, group=Grid.vehicles)

    def draw(self) -> None:
        self.sprite.draw()

    def move_to(self, x, y) -> None:
        self.sprite.x = x
        self.sprite.y = y

    def move_by(self, dx, dy) -> None:
        self.sprite.x += dx
        self.sprite.y += dy

    def move_dir(self, speed):
        dx = sin(radians(self.sprite.rotation)) * speed
        dy = cos(radians(self.sprite.rotation)) * speed
        self.move_by(dx, dy)

    def rotate_to(self, deg) -> None:
        self.sprite.rotation = deg

    def rotate_by(self, deg) -> None:
        self.sprite.rotation += deg

    def show(self) -> None:
        self.sprite.visible = True

    def hide(self) -> None:
        self.sprite.visible = False

    def load(self, amount) -> None:
        if self.cargo_amount + amount > self.MAX_CARGO_AMOUNT:
            match self.MAXIMUM_EXCEED:
                case "not load":
                    pass
                case "error":
                    raise OverflowError(f"<{self.type} {self.id}> Too much cargo to fit in this vehicle")

    def get_cargo_amount(self) -> int:
        return self.cargo_amount

class Car1(Vehicle):
    def __init__(self, image:Path, capacity:int):
        super().__init__(image)

        self.type = "car 1"
        self.MAX_CARGO_AMOUNT = capacity
        self.CAN_GO_THROUGH = ["G"]
        self.MAXIMUM_EXCEED = "not load"

class Car2(Vehicle):
    def __init__(self, image:Path, capacity:int):
        super().__init__(image)

        self.type = "car 2"
        self.MAX_CARGO_AMOUNT = capacity
        self.CAN_GO_THROUGH = ["G"]
        self.MAXIMUM_EXCEED = "not load"

class Ship(Vehicle):
    def __init__(self, image:Path, capacity:int):
        super().__init__(image)

        self.type = "ship"
        self.MAX_CARGO_AMOUNT = capacity
        self.CAN_GO_THROUGH = ["W"]
        self.MAXIMUM_EXCEED = "not load"

class Plane(Vehicle):
    def __init__(self, image:Path, capacity:int):
        super().__init__(image)

        self.type = "plane"
        self.MAX_CARGO_AMOUNT = capacity
        self.CAN_GO_THROUGH = ["G", "W"]
        self.PATH = "straight"
        self.MAXIMUM_EXCEED = "not load"