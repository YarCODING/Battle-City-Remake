import pygame as p
import sys
from random import*
import os
import math

SCREENSIZE = (700, 500)
SCREEN = p.display.set_mode(SCREENSIZE)
p.display.set_caption("Battle_City_Remake")

clock = p.time.Clock()
FPS = 60

# p.mixer.init()
# p.mixer.music.load('music/music1.mp3')
# p.mixer.music.set_volume(1)
# p.mixer.music.play(-1)

background = p.image.load("img/bg.jpg")
background = p.transform.scale(background, SCREENSIZE)

p.font.init()


title_font = p.font.SysFont("Arial", 30)
play_text = title_font.render("Play Game", True, (255, 255, 255))
close_text = title_font.render("Close Game", True, (255, 255, 255))


play_button_rect = p.Rect(250, 200, 200, 60)
close_button_rect = p.Rect(250, 300, 200, 60)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255,0) 