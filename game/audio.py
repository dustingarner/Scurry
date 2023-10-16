import os
import random
import pygame as pg


def create_sound(file_name: str) -> pg.mixer.Sound:
    data_folder = os.path.abspath("assets/")
    sound_file = os.path.join(data_folder, file_name)
    return pg.mixer.Sound(sound_file)

def hooray() -> None:
    random.seed()
    num = random.random()

    if num < 0.28:
        sound = create_sound("Sounds/Hooray.mp3")
    elif num < 0.55:
        sound = create_sound("Sounds/Yippee.mp3")
    elif num < 0.85:
        sound = create_sound("Sounds/Yayy.mp3")
    elif num < 0.95:
        sound = create_sound("Sounds/Thanks.mp3")
    else:
        sound = create_sound("Sounds/Yay I didn't die.mp3")
    
    sound.play()

def dead() -> None:
    random.seed()
    num = random.random()

    if num < 0.33:
        sound = create_sound("Sounds/Aaahhgghhh.mp3")
    elif num < 0.66:
        sound = create_sound("Sounds/Nooo.mp3")
    else:
        sound = create_sound("Sounds/Oof.mp3")
    
    sound.play()
