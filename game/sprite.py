import os
from PIL import Image
import pygame as pg


class Sprite:
    def __init__(self, image_name: str, offset: pg.Vector2, scale: float):
        self.scale = scale
        self.surface = self.load_surface(image_name = image_name)
        self.image = self.load_image(image_name = image_name)
        self.offset = offset
    
    def load_surface(self, image_name: str) -> pg.Surface:
        path = os.path.abspath("assets/")
        file = os.path.join(path, image_name)
        image_info = Image.open(file)
        self.dimensions = pg.Vector2(image_info.width, image_info.height) #Bad place to define this
        surface = pg.Surface(self.dimensions).convert()
        return surface
    
    def load_image(self, image_name: str) -> pg.Surface:
        path = os.path.abspath("assets/")
        file = os.path.join(path, image_name)
        image = pg.image.load(file).convert()
        return image

    def draw(self, screen: pg.Surface, position: pg.Vector2):
        new_position = position + self.offset
        self.surface.blit(self.image, (0,0))
        surface = pg.transform.scale(surface = self.surface, \
                size = self.dimensions * self.scale)
        screen.blit(surface, new_position)

