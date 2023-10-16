import pygame as pg
import game.observer as observer
import game.collision as collision
import game.sprite as sprite


class Shelter:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.position = pg.Vector2(self.screen_size.x - 150, -9)

        self.rectangle = pg.Rect(self.position, (150, 75))

        self.sprite = sprite.Sprite(image_name = "Shelter.png", offset = (0,0), scale = 0.2)

        self.collision = collision.CollisionRect(screen = self.screen, screen_size = self.screen_size,\
                parent = self, dimensions = (37.6, 35.2), position = self.position, \
                offset = pg.Vector2(48.8,38.4))
        self.draw_subject = observer.Subject()
    
    def draw(self):
        self.sprite.draw(screen = self.screen, position = self.position)

    def process(self, delta):
        self.draw_subject.notify(self, self.position.y)
