import pygame as p
import sys
from random import*
import os
import math
import random

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

SCREENSIZE = (704, 512)
SCREEN = p.display.set_mode(SCREENSIZE)
p.display.set_caption("Battle_City_Remake")

menu_screen = 'start'

clock = p.time.Clock()
FPS = 60

p.mixer.init()
menu_music_path = "music/menu_music.mp3"
playlist = ["music/music1.mp3", "music/music2.mp3"]

MUSIC_ENDED = p.USEREVENT + 1
p.mixer.music.set_endevent(MUSIC_ENDED)

current_music_type = None

def play_menu_music():
    global current_music_type
    if current_music_type != 'menu':
        current_music_type = 'menu'
        p.mixer.music.load(menu_music_path)
        p.mixer.music.play(-1)

def play_game_music():
    global current_music_type
    current_music_type = 'game'
    track = random.choice(playlist)
    p.mixer.music.load(track)
    p.mixer.music.play()


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def get_sound(obj, name):
    return p.mixer.Sound(os.path.join(BASE_PATH, "obj", obj, "sound", name))

background = p.image.load("img/bg.jpeg")
background = p.transform.scale(background, SCREENSIZE)

medal = p.transform.scale(p.image.load("img/gold.png"), (90, 150))

p.font.init()


title_font = p.font.SysFont("Arial", 30)
play_text = title_font.render("Play Game", True, (255, 255, 255))
close_text = title_font.render("Close Game", True, (255, 255, 255))
continue_text = title_font.render("Continue", True, (255, 255, 255))


play_button_rect = p.Rect(250, 200, 200, 60)
close_button_rect = p.Rect(250, 300, 200, 60)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255,0) 