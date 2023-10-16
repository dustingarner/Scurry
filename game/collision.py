import pygame as pg
import game.observer as observer


class CollisionRect:
    def __init__(self, screen, screen_size, parent, dimensions: tuple, position: pg.Vector2, \
            offset: pg.Vector2 = pg.Vector2(0,0)):
        self.screen = screen
        self.screen_size = screen_size
        self.parent = parent
        self.rectangle = pg.Rect(position + offset, dimensions)
        self.offset = offset

        self.potential_colliders = []
        self.current_colliders = []
        self.body_entered = observer.Subject()
        self.body_exited = observer.Subject()
        self.mouse_entered = observer.Subject()
        self.mouse_exited = observer.Subject()
        self.mouse_inside = False
        self.collider_observer = observer.Observer(self.add_potential_collider)

        self.clicked_already = False
        self.mouse_clicked = observer.Subject()
    
    def set_position(self, new_position):
        self.rectangle.update(pg.Rect(new_position + self.offset, self.rectangle.size))

    def add_potential_collider(self, collider):
        self.potential_colliders.append(collider)

    def remove_potential_collider(self, collider):
        self.potential_colliders.remove(collider)

    def check_collisions(self):
        for i in self.potential_colliders:
            collides = self.rectangle.colliderect(i.rectangle)
            if i in self.current_colliders and not collides:
                self.current_colliders.remove(i)
                self.body_exited.notify(i)
                continue
            elif i in self.current_colliders or not collides:
                continue
            self.current_colliders.append(i)
            self.body_entered.notify(i)

    def check_mouse_collisions(self):
        collides = self.rectangle.collidepoint(pg.mouse.get_pos())
        if self.mouse_inside and not collides:
            self.mouse_inside = False
            self.mouse_exited.notify()
            return
        elif self.mouse_inside or not collides:
            return
        self.mouse_inside = True
        self.mouse_entered.notify()
        
    def check_mouse_click(self) -> None:
        if not self.mouse_inside:
            return
        if self.clicked_already:
            return
        if not pg.mouse.get_pressed()[0]:
            return
        self.clicked_already = True
        self.mouse_clicked.notify()

    def draw(self, color = "blue") -> None:
        pg.draw.rect(self.screen, color, self.rectangle)

    def process(self, delta):
        self.check_collisions()
        self.check_mouse_collisions()
        if self.clicked_already and not pg.mouse.get_pressed()[0]:
            self.clicked_already = False
        self.check_mouse_click()
        
