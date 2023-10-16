import os
import sys
from enum import Enum
import pygame as pg
import game.enemies as enemies
import game.mouse as mouse
import game.shelter as shelter
import game.observer as observer
import game.menu as menu
import game.audio as audio


if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))


class GameLoop:
    def __init__(self, screen: pg.Surface, screen_size: pg.Vector2) -> None:
        self.screen = screen
        self.screen_size = screen_size
        self.current_state = self.States.MAIN
        self.click_observer = observer.Observer(self.click_sound)
        self.main_song = audio.create_sound("Music/Song.mp3")
        self.sound_volume = 0.5
        self.main_song.set_volume(self.sound_volume)
        self.main_song.play()
        self.open_main()

    class States(Enum):
        MAIN = 1
        INFO = 2
        GAME = 3
        END = 4

    def change_state(self, new_state) -> None:
        if self.current_state == self.States.END:
            self.main_song.play()
            del self.end_screen
        elif self.current_state == self.States.MAIN:
            del self.main_menu
        elif self.current_state == self.States.INFO:
            del self.info_menu

        self.current_state = new_state
        if new_state == self.States.GAME:
            self.game = Scurry(self.screen, self.screen_size)
        elif new_state == self.States.END:
            self.main_song.stop()
            del self.game
        elif new_state == self.States.MAIN:
            self.open_main()
        elif new_state == self.States.INFO:
            self.open_info()

    def switch_to_main(self) -> None:
        self.change_state(self.States.MAIN)
    
    def switch_to_info(self) -> None:
        self.change_state(self.States.INFO)

    def open_main(self) -> None:
        self.main_menu = menu.MainMenu(screen = self.screen, screen_size = self.screen_size)
        self.play_observer = observer.Observer(self.play_game)
        self.main_menu.play_button.collision.mouse_clicked.add_observer(self.play_observer)
        self.main_menu.play_button.collision.mouse_clicked.add_observer(self.click_observer)
        self.info_observer = observer.Observer(self.switch_to_info)
        self.main_menu.info_button.collision.mouse_clicked.add_observer(self.info_observer)
        self.main_menu.info_button.collision.mouse_clicked.add_observer(self.click_observer)
        
    def open_info(self) -> None:
        self.info_menu = menu.InfoMenu(screen = self.screen, screen_size = self.screen_size)
        self.back_observer = observer.Observer(self.switch_to_main)
        self.info_menu.back_button.collision.mouse_clicked.add_observer(self.back_observer)
        self.info_menu.back_button.collision.mouse_clicked.add_observer(self.click_observer)

    def play_game(self) -> None:
        self.change_state(self.States.GAME)
        self.end_observer = observer.Observer(self.end_game)
        
        self.game = Scurry(screen = self.screen, screen_size = self.screen_size)
        self.game.game_over.add_observer(self.end_observer)
    
    def end_game(self, casualties: int, safe: int) -> None:
        self.change_state(self.States.END)
        if casualties == 0:
            sound = audio.create_sound("Music/Congrats.mp3")
            self.end_screen = menu.CongratsScreen(self.screen, self.screen_size)
        else:
            sound = audio.create_sound("Music/End.mp3")
            self.end_screen = menu.EndScreen(self.screen, self.screen_size, casualties = casualties, safe = safe)
        sound.set_volume(self.sound_volume)
        sound.play()
        self.main_observer = observer.Observer(self.switch_to_main)
        self.end_screen.timer.add_observer(self.main_observer)

    def click_sound(self) -> None:
        sound = audio.create_sound("Sounds/Click.mp3")
        sound.play()

    def process(self, delta) -> None:
        match self.current_state:
            case self.States.MAIN:
                self.main_menu.process(delta)
            case self.States.INFO:
                self.info_menu.process(delta)
            case self.States.GAME:
                self.game.process(delta)
            case self.States.END:
                self.end_screen.process(delta)



class Scurry:
    def __init__(self, screen: pg.Surface, screen_size: pg.Vector2) -> None:
        self.screen = screen
        self.screen_size = screen_size
        self.casualties = 0
        self.safe = 0

        self.draw_observer = observer.Observer(self.add_drawable)
        self.draw_order = {}

        self.shelter = shelter.Shelter(screen, screen_size)
        self.shelter.draw_subject.add_observer(self.draw_observer)

        self.players = []
        self.shift_observer = observer.Observer(action = self.shift_control)
        self.delete_player_observer = observer.Observer(self.delete_player)
        for i in [pg.Vector2(100, 500), pg.Vector2(200, 500), pg.Vector2(100, 400), pg.Vector2(200, 400)]:
            player = mouse.Mouse(screen = self.screen, screen_size = self.screen_size, position = i)
            player.draw_subject.add_observer(self.draw_observer)
            player.make_playable.add_observer(self.shift_observer)
            player.delete_self.add_observer(self.delete_player_observer)
            player.add_shelter(self.shelter)
            self.players.append(player)
        self.playable_player = self.players[0]
        self.playable_player.change_state(self.playable_player.ControlStates.PLAYABLE)

        self.spawner = enemies.Spawner(screen = self.screen, screen_size = self.screen_size)
        self.add_observer = observer.Observer(self.add_enemy)
        self.spawner.add_subject.add_observer(self.add_observer)

        self.game_over = observer.Subject()
    
    def shift_control(self, player: mouse.Mouse) -> None:
        if player.current_state == player.ControlStates.TAKEN:
            return
        for i in self.players:
            if i.current_state == i.ControlStates.TAKEN:
                continue
            i.change_state(i.ControlStates.IDLE)
        self.playable_player = player
        player.change_state(player.ControlStates.PLAYABLE)


    def add_drawable(self, item, y_pos) -> None:
        self.draw_order[item] = y_pos

    def add_enemy(self, enemy: enemies.Enemy) -> None:
        enemy.draw_subject.add_observer(self.draw_observer)
        for player in self.players:
            player.add_enemy(enemy)
            enemy.deletion_subject.add_observer(player.enemy_deletion_observer)
        enemy.deletion_subject.add_observer(self.spawner.delete_observer)

    def delete_player(self, player: mouse.Mouse, by_shelter: bool) -> None:
        self.players.remove(player)
        del player
        if by_shelter:
            self.safe += 1
        else:
            self.casualties += 1
        self.check_game_over()

    def check_game_over(self) -> None:
        if len(self.players) == 0:
            self.game_over.notify(self.casualties, self.safe)
        

    def process(self, delta) -> None:
        self.screen.fill((196,170,153))
        self.draw_order = {}

        for player in self.players:
            player.process(delta)
        self.spawner.process(delta)
        self.shelter.process(delta)

        self.draw_order = dict(sorted(self.draw_order.items(), key = lambda x : x[1]))
        for item in self.draw_order.keys():
            item.draw()

        pg.display.flip()

def main():
    pg.init()
    screen_size = pg.Vector2(800, 600)
    screen = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()
    delta = 0

    running = True
    game_loop = GameLoop(screen, screen_size)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        game_loop.process(delta)
        delta = clock.tick(60) / 1000
    
    pg.quit()






if __name__ == "__main__":
    main()
