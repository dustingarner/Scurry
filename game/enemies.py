import random
import pygame as pg
import game.observer as observer
import game.collision as collision
import game.sprite as sprite



class Enemy:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.MOVE_SPEED = 75
        self.direction = self.new_direction()
        self.position = self.new_position()

        self.type = self.new_type()
        scale = 0.4
        self.sprite = sprite.Sprite(image_name = self.type + ".png", offset = pg.Vector2(0,0), scale = scale)
        if self.type == "Cat":
            dimensions = pg.Vector2(184.2, 73.5)
            offset = pg.Vector2(220.5, 144.8)
        else:
            dimensions = pg.Vector2(94.5, 138.4)
            offset = pg.Vector2(295.4, 80.4)
        self.collision = collision.CollisionRect(screen = self.screen, screen_size = self.screen_size, 
                parent = self, dimensions = dimensions * scale, position = self.position, offset = offset * scale)
        
        self.update_collision()

        self.draw_subject = observer.Subject()
        self.deletion_subject = observer.Subject()

    def new_direction(self) -> pg.Vector2:
        random.seed()
        option = random.randrange(1, 3)
        if option == 1:
            return pg.Vector2(1,1).normalize()
        else:
            return pg.Vector2(-1,-1).normalize()
    
    def new_position(self) -> pg.Vector2:
        random.seed()
        if self.direction.x < 0:
            x = random.randrange(150, 800)
            return pg.Vector2(x, self.screen_size.y)
        else:
            x = random.randrange(0, self.screen_size.x - 150)
            return pg.Vector2(x, 0)

    def new_type(self) -> str:
        random.seed()
        num = random.random()
        if num <= 0.5:
            return "Owl"
        return "Cat"

    def update_collision(self) -> None:
        self.collision.set_position(self.position)

    def move(self, delta) -> None:
        self.position += self.MOVE_SPEED * self.direction * delta
        if self.position.y < -30 and self.direction.x < 0:
            self.delete()
        elif self.position.y > self.screen_size.y + 30 and self.direction.x > 0:
            self.delete()
        self.update_collision()

    def draw(self) -> None:
        self.sprite.draw(self.screen, self.position)
    
    def delete(self) -> None:
        self.deletion_subject.notify(self)

    def process(self, delta):
        self.move(delta)
        self.draw_subject.notify(self, self.position.y)
        self.collision.draw()


class Cat(Enemy):
    def __init__(self):
        super().__init__()

class Owl(Enemy):
    def __init__(self):
        super().__init__()



class Spawner:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size

        self.SPAWN_SPEED = 200
        self.counter = 0
        self.max_count = self.new_max_count()

        self.add_subject = observer.Subject()
        self.enemies = []

        self.delete_observer = observer.Observer(self.delete_enemy)
    
    def new_max_count(self) -> float:
        random.seed()
        return random.randrange(200, 300)
    
    def spawn_enemy(self) -> None:
        new_enemy = Enemy(self.screen, self.screen_size)
        self.enemies.append(new_enemy)
        self.add_subject.notify(new_enemy)

    def delete_enemy(self, enemy: Enemy) -> None:
        self.enemies.remove(enemy)
        del enemy

    def process(self, delta) -> None:
        self.counter += self.SPAWN_SPEED * delta
        if self.counter >= self.max_count:
            self.spawn_enemy()
            self.counter = 0
            self.max_count = self.new_max_count()
        for enemy in self.enemies:
            enemy.process(delta)


