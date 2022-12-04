from typing import Literal, Union
from pathlib import Path as pth
from generate import Grid
import pyglet

Path = Union[pth, str]

class Vehicle:
    _id = 0
    _batch = pyglet.graphics.Batch()

    def __init__(self, image:Path):
        self.MAX_CARGO_AMOUNT:int
        self.MAXIMUM_EXCEED:Literal["not load", "error"]
        self.id = Vehicle._id
        Vehicle._id += 1

        self.cargo_amount = 0

        self.image = pyglet.image.load(image)
        self.sprite = pyglet.sprite.Sprite(self.image, batch=Vehicle._batch, group=Grid.vehicles)

    def draw(self) -> None:
        self.sprite.draw()

    def move_to(self, x, y) -> None:
        self.sprite.x = x
        self.sprite.y = y

    def move_by(self, dx, dy) -> None:
        self.sprite.x += dx
        self.sprite.y += dy

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
                    raise OverflowError(f"<Vehicle {self.id}> Too much cargo to fit in this vehicle")

    def get_cargo_amount(self) -> int:
        return self.cargo_amount