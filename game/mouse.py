from enum import Enum
import pygame as pg
import game.observer as observer
import game.enemies as enemies
import game.collision as collision
import game.shelter as shelter
import game.sprite as sprite
import game.audio as audio


class Mouse:
    def __init__(self, screen, screen_size, position):
        self.screen = screen
        self.screen_size = screen_size
        self.position = position

        self.draw_subject = observer.Subject()
        self.current_state = self.ControlStates.IDLE
        self.speed = 300
        self.enemy_collision = collision.CollisionRect(screen = self.screen, screen_size = self.screen_size, \
                parent = self, dimensions = (50, 25), position = self.position)
        self.shelter_collision = collision.CollisionRect(screen = self.screen, screen_size = self.screen_size, \
                parent = self, dimensions = (75, 36), position = self.position, offset = pg.Vector2(-22.3, -9.85))
        self.enemy_collision_observer = observer.Observer(self.collide_with_enemy)
        self.enemy_collision.body_entered.add_observer(self.enemy_collision_observer)
        self.shelter_collision_observer = observer.Observer(self.enter_shelter)
        self.shelter_collision.body_entered.add_observer(self.shelter_collision_observer)

        self.mouse_collision = collision.CollisionRect(screen = self.screen, screen_size = self.screen_size, \
                parent = self, dimensions = (131.25, 75), position = self.position, offset = pg.Vector2(-70, -28.75))

        self.sprite = sprite.Sprite(image_name = "Mouse.png", offset = pg.Vector2(-70,-28.75), scale = 0.25)

        self.make_playable = observer.Subject()
        
        self.update_collision()

        self.enemy_add_observer = observer.Observer(self.add_enemy)
        self.enemy_deletion_observer = observer.Observer(self.remove_enemy)
        self.taken_direction = pg.Vector2(0,0)

        self.delete_self = observer.Subject()

    def change_state(self, new_state):
        self.current_state = new_state

    class ControlStates(Enum):
        IDLE = 0
        PLAYABLE = 1
        TAKEN = 2

    def add_enemy(self, enemy: enemies.Enemy) -> None:
        self.enemy_collision.add_potential_collider(enemy.collision)

    def remove_enemy(self, enemy: enemies.Enemy) -> None:
        self.enemy_collision.remove_potential_collider(enemy.collision)

    def add_shelter(self, shelter: shelter.Shelter) -> None:
        self.shelter_collision.add_potential_collider(shelter.collision)

    def update_collision(self) -> None:
        for collision in [self.enemy_collision, self.shelter_collision, self.mouse_collision]:
            collision.set_position(self.position)

    def move(self, delta):
        direction = self.get_direction()
        self.position += direction * self.speed * delta
        if self.position.x < 0:
            self.position.x = 0
        if self.position.x > self.screen_size.x:
            self.position.x = self.screen_size.x
        if self.position.y < 0:
            self.position.y = 0
        if self.position.y > self.screen_size.y:
            self.position.y = self.screen_size.y
        self.update_collision()

    def taken_move(self, delta):
        self.position += self.taken_direction * self.speed * delta
        if (self.position.y < -46.25 or self.position.x < 61.25) and self.taken_direction.x < 0:
            self.delete_self.notify(self, False)
            return
        elif (self.position.y > self.screen_size.y + 28.75 or self.position.x > self.screen_size.x + 70) \
                and self.taken_direction.x > 0:
            self.delete_self.notify(self, False)
            return
        self.update_collision()
    
    def enter_shelter(self, shelter):
        audio.hooray()
        self.delete_self.notify(self, True)

    def draw(self):
        self.sprite.draw(screen = self.screen, position = self.position)

    def collide_with_enemy(self, enemy) -> None:
        self.change_state(self.ControlStates.TAKEN)
        self.taken_direction = enemy.parent.direction
        self.speed = enemy.parent.MOVE_SPEED
        self.enemy_collision_observer.disconnect()
        audio.dead()

    def get_direction(self) -> pg.Vector2:
        keys = pg.key.get_pressed()
        direction = pg.Vector2(0,0)
        if keys[pg.K_w] or keys[pg.K_UP]:
            direction.y -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            direction.y += 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            direction.x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            direction.x += 1
        if direction == pg.Vector2(0,0):
            return direction
        return direction.normalize()

    def test_mouse(self) -> None:
        if pg.mouse.get_pressed()[0] and self.mouse_collision.mouse_inside:
            self.make_playable.notify(self)

    def process(self, delta):
        self.enemy_collision.process(delta)
        self.shelter_collision.process(delta)
        self.mouse_collision.process(delta)
        if self.current_state == self.ControlStates.IDLE:
            self.test_mouse()
        elif self.current_state == self.ControlStates.TAKEN:
            self.taken_move(delta)
        else:
            self.move(delta)

        self.draw_subject.notify(self, self.position.y)



    


