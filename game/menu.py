import pygame as pg
import game.sprite as sprite
import game.collision as collision
import game.observer as observer

class Button:
    def __init__(self, screen, screen_size, name: str, position: pg.Vector2, scale: float) -> None:
        self.screen = screen
        self.screen_size = screen_size

        self.position = position
        self.sprite = sprite.Sprite(image_name = "menu/" + name + ".png", \
                offset = pg.Vector2(0,0), scale = scale)
        self.collision = collision.CollisionRect(screen = screen, screen_size = screen_size, parent = self,\
                dimensions = self.sprite.dimensions * scale, position = self.position)
    
    def draw(self):
        self.sprite.draw(self.screen, self.position)
    
    def process(self, delta):
        self.draw()
        self.collision.set_position(self.position)
        self.collision.process(delta)
        
        

class MainMenu:
    def __init__(self, screen, screen_size) -> None:
        self.screen = screen
        self.screen_size = screen_size

        self.title_pos = (400 - 260,40)
        self.title = sprite.Sprite("Menu/Title.png", (0,0), 1)

        self.play_button = Button(screen = screen, screen_size = screen_size, name = "Play", \
                position = (400 - (167 / 2), 325), scale = 0.5)
        self.info_button = Button(screen = screen, screen_size = screen_size, name = "Info", \
                position = (400- (167 / 2), 450), scale = 0.5)
        
        

        
    
    def process(self, delta) -> None:
        self.screen.fill((175,174,170))
        self.title.draw(self.screen, self.title_pos)
        for i in [self.play_button, self.info_button]:
            i.process(delta)
            
        pg.display.flip()



class InfoMenu:
    def __init__(self, screen, screen_size) -> None:
        self.screen = screen
        self.screen_size = screen_size

        self.text_pos = (400 - 335, 25)
        self.text = sprite.Sprite("Menu/Info Text.png", (0,0), 0.5)
        self.back_button = Button(screen = screen, screen_size = screen_size, name = "Back", \
                position = (50, 475), scale = 0.5)
        
    def process(self, delta) -> None:
        self.screen.fill((174,173,169))
        self.text.draw(self.screen, self.text_pos)
        self.back_button.process(delta)
        pg.display.flip()


class EndScreen:
    def __init__(self, screen, screen_size, casualties: int, safe: int) -> None:
        self.screen = screen
        self.sreen_size = screen_size

        self.casualties_text = sprite.Sprite("Menu/Casualties.png", (0,0), 0.5)
        self.safe_text = sprite.Sprite("Menu/Safe.png", (0,0), 0.5)
        self.casualties_number = sprite.Sprite("Menu/Counter/" + str(casualties) + ".png", (0,0), 0.5)
        self.safe_number = sprite.Sprite("Menu/Counter/" + str(safe) + ".png", (0,0), 0.5)

        self.counter = 0
        self.TIMEOUT = 4

        self.timer = observer.Subject()

    def process(self, delta) -> None:
        self.screen.fill((174,173,169))
        
        self.counter += delta
        if self.counter >= self.TIMEOUT:
            self.timer.notify()

        self.casualties_text.draw(self.screen, (150, 125))
        self.casualties_number.draw(self.screen, (450, 125))
        self.safe_text.draw(self.screen, (150, 325))
        self.safe_number.draw(self.screen, (450, 325))

        pg.display.flip()

class CongratsScreen:
    def __init__(self, screen, screen_size) -> None:
        self.screen = screen
        self.screen_size = screen_size

        self.congrats = sprite.Sprite("Menu/Congratulations.png", (0,0), 0.6)

        self.counter = 0
        self.TIMEOUT = 5

        self.timer = observer.Subject()

    def process(self, delta) -> None:
        self.screen.fill((174,173,169))
        
        self.counter += delta
        if self.counter >= self.TIMEOUT:
            self.timer.notify()

        self.congrats.draw(self.screen, (90, 200))

        pg.display.flip()
