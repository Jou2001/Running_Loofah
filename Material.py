# sprite
from typing import Any
import pygame
import os
import sys
from moviepy.editor import *
import mediapipe as mp
import pyautogui
import math

WHITE = (255, 255, 255)
PURPLE = (171, 38, 201)
# initial
pygame.init()
pygame.mixer.init()

# define color
WHITE = (255, 255, 255)
# define screen size
S_WIDTH, S_HEIGHT = pyautogui.size()
COMMOM_R_W = S_WIDTH / 1920.0
COMMOM_R_H = S_HEIGHT / 1200.0
COMMOM_R = COMMOM_R_H
if COMMOM_R_W > COMMOM_R_H :
    COMMOM_R = COMMOM_R_H
elif COMMOM_R_W < COMMOM_R_H :
    COMMOM_R = COMMOM_R_W

WIDTH = int(1920*COMMOM_R)
HEIGHT = int(1200*COMMOM_R)
# define player initial position
PLAYER_Y = int(540*COMMOM_R)
#define player continuous jump time
PLAYER_JUMP = 2
PLAYER_DOWN = 2
PLAYER_ATTACK = 2
gravity = int(10*COMMOM_R)
# define player health
HEALTH = 100
# define health size
BAR_LENGTH = int(400*COMMOM_R_W)
BAR_HEIGHT = int(40*COMMOM_R_W)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) # create screen
pygame.display.set_caption('Running loofah') # 開始前標題
# load into picture
background1_img = pygame.image.load(os.path.join("img", "background01.png")).convert()
background1_img = pygame.transform.scale( background1_img, (S_WIDTH, S_HEIGHT) )
background2_img = pygame.image.load(os.path.join("img", "background02.png")).convert()
background2_img = pygame.transform.scale( background2_img, (S_WIDTH, S_HEIGHT) )
background3_img = pygame.image.load(os.path.join("img", "background03.png")).convert()
background3_img = pygame.transform.scale( background3_img, (1920*COMMOM_R, 1200*COMMOM_R) )
background4_img = pygame.image.load(os.path.join("img", "background04.png")).convert()
background4_img = pygame.transform.scale( background4_img, (S_WIDTH, S_HEIGHT) )

GROUND_NUM = math.ceil(S_WIDTH / int(420*COMMOM_R)) + 1
ground_img = []
for i in range(0, 5) :
    image = pygame.image.load(os.path.join("img", "ground_" + str(i+1) + ".png")).convert_alpha()
    image = pygame.transform.scale( image, (int(420*COMMOM_R), 406*COMMOM_R) ) 
    ground_img.append( image )

takephoto = pygame.image.load(os.path.join("img", "takephoto.png")).convert_alpha()
takephoto = pygame.transform.scale( takephoto, (1920*COMMOM_R, 1200*COMMOM_R) )

intro_attack = pygame.image.load(os.path.join("img", "intro_attack.png")).convert_alpha()
intro_attack = pygame.transform.scale( intro_attack, (420*COMMOM_R, 680*COMMOM_R) ) # 420*680
intro_jump = pygame.image.load(os.path.join("img", "intro_jump.png")).convert_alpha()
intro_jump = pygame.transform.scale( intro_jump, (340*COMMOM_R, 590*COMMOM_R) ) # 340*590
intro_slip_1 = pygame.image.load(os.path.join("img", "intro_slip_1.png")).convert_alpha()
intro_slip_1 = pygame.transform.scale( intro_slip_1, (560*COMMOM_R, 600*COMMOM_R) ) # 560*600
intro_slip_2 = pygame.image.load(os.path.join("img", "intro_slip_2.png")).convert_alpha()
intro_slip_2 = pygame.transform.scale( intro_slip_2, (560*COMMOM_R, 600*COMMOM_R) ) # 560*600
intro_handup_left = pygame.image.load(os.path.join("img", "intro_handup_left.png")).convert_alpha()
intro_handup_left = pygame.transform.scale( intro_handup_left, (468*COMMOM_R, 668*COMMOM_R) ) # 468*668
intro_handup_right = pygame.image.load(os.path.join("img", "intro_handup_right.png")).convert_alpha()
intro_handup_right = pygame.transform.scale( intro_handup_right, (468*COMMOM_R, 668*COMMOM_R) ) # 468*668

intro_attack_2 = pygame.image.load(os.path.join("img", "intro_attack-2.png")).convert_alpha()
intro_attack_2 = pygame.transform.scale( intro_attack_2, (420*COMMOM_R, 680*COMMOM_R) ) # 420*680
intro_jump_2 = pygame.image.load(os.path.join("img", "intro_jump-2.png")).convert_alpha()
intro_jump_2 = pygame.transform.scale( intro_jump_2, (340*COMMOM_R, 590*COMMOM_R) ) # 340*590
intro_slip_1_2 = pygame.image.load(os.path.join("img", "intro_slip_1-2.png")).convert_alpha()
intro_slip_1_2 = pygame.transform.scale( intro_slip_1_2, (560*COMMOM_R, 600*COMMOM_R) ) # 560*600
intro_slip_2_2 = pygame.image.load(os.path.join("img", "intro_slip_2-2.png")).convert_alpha()
intro_slip_2_2 = pygame.transform.scale( intro_slip_2_2, (560*COMMOM_R, 600*COMMOM_R) ) # 560*600

bullet = pygame.image.load(os.path.join("img", "bullet.png")).convert_alpha()
bullet = pygame.transform.scale( bullet, (912*COMMOM_R*0.11, 1032*COMMOM_R*0.11) ) # 912*1032 /18

cloud = []
for i in range(0, 3) :
    image = pygame.image.load(os.path.join("img", "cloud0" + str(i+1) + ".png")).convert_alpha()
    if i+1 == 1:
        image = pygame.transform.scale( image, (348*COMMOM_R, 178*COMMOM_R) ) # 348*178
    if i+1 == 2:
        image = pygame.transform.scale( image, (218*COMMOM_R, 158*COMMOM_R) ) # 218*158
    if i+1 == 3 :
        image = pygame.transform.scale( image, (358*COMMOM_R, 208*COMMOM_R) ) # 358*208
    cloud.append( image )

tree = []
image = pygame.image.load(os.path.join("img", "grove.png")).convert_alpha()
image = pygame.transform.scale( image, (638*COMMOM_R, 478*COMMOM_R) ) # 638*478
tree.append( image )
image = pygame.image.load(os.path.join("img", "tree.png")).convert_alpha()
image = pygame.transform.scale( image, (448*COMMOM_R, 848*COMMOM_R) ) # 488*848
tree.append( image )

sun = pygame.image.load(os.path.join("img", "sun.png")).convert_alpha()
sun = pygame.transform.scale( sun, (200*COMMOM_R, 200*COMMOM_R) ) # 200*200

#load mp4
do_the_following_mp4 = VideoFileClip(os.path.join("video", "do_the_following.mp4")).resize((WIDTH,HEIGHT))
start321_mp4 = VideoFileClip(os.path.join("video", "start321_mp3.mp4")).resize((WIDTH,HEIGHT))
win_mp4 = VideoFileClip(os.path.join("video", "win_mp3.mp4")).resize((WIDTH,HEIGHT))
lose_mp4 = VideoFileClip(os.path.join("video", "lose_mp3.mp4")).resize((WIDTH,HEIGHT))

#load music mp3
camera_mp3 = pygame.mixer.Sound(os.path.join("mp3", "cameraMusic.mp3"))
jump_mp3 = pygame.mixer.Sound(os.path.join("mp3", "jumpMusic.mp3"))
good_mp3 = pygame.mixer.Sound(os.path.join("mp3", "Good.mp3"))


load_image = []
player_slip_img = pygame.image.load(os.path.join("img", "player_slip.png")).convert_alpha() # 470*256
healthstate_head = pygame.image.load(os.path.join("img", "healthstate_head.png")).convert_alpha() # 200*201


obstacle = []
for i in range(0, 7) :
    image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
    if i+1 == 1:
        image = pygame.transform.scale( image, (202*COMMOM_R, 279*COMMOM_R) ) # 蟲蟲 202*279
    elif i+1 == 2:
        image = pygame.transform.scale( image, (281*COMMOM_R, 303*COMMOM_R) ) # 老鼠 281*303
    elif i+1 == 3 :
        image = pygame.transform.scale( image, (2048*COMMOM_R*0.25, 2048*COMMOM_R*0.25) ) # 飛天雞 2048*2048
    elif i+1 == 4 :
        image = pygame.transform.scale( image, (408*COMMOM_R*0.85, 408*COMMOM_R*0.85) ) # 球 408*408
    elif i+1 == 5 or 6 or 7 :
        if i+1 == 6 :
            image01 = image.copy()
        image = pygame.transform.scale( image, (820*COMMOM_R*0.665, 570*COMMOM_R*0.665) ) # 野豬 820*570 
    obstacle.append( image )
image = pygame.transform.scale( image01, (820*COMMOM_R*0.665*0.7, 570*COMMOM_R*0.665*0.7) ) # 野豬 820*570 /3 *0.7
obstacle.append( image )

end_pig = []
for i in range(0,3) :
    image = pygame.image.load(os.path.join("img", "End_pig-" + str(i+1) + ".png")).convert_alpha()
    image = pygame.transform.scale( image, (820*COMMOM_R*0.665, 570*COMMOM_R*0.665) ) # 野豬 820*570
    obstacle.append( image )

end_chicken = pygame.image.load(os.path.join("img", "End_chicken.png")).convert_alpha()
end_chicken = pygame.transform.scale( end_chicken, (2048*COMMOM_R*0.25, 2048*COMMOM_R*0.25) ) # 飛天雞 2048*2048

end_UFO = pygame.image.load(os.path.join("img", "UFO.png")).convert_alpha()
end_UFO = pygame.transform.scale( end_UFO, (517*COMMOM_R, 435*COMMOM_R) ) # UFO 517*435

# load into txt
fout_txt = os.path.join( "Handwriting.ttf" )

def draw_text( surf, text, size, x, y, colors ) :
    font = pygame.font.Font( fout_txt, size )
    # font = pygame.font.SysFont( "arial", size )
    text_surface = font.render( text, True, colors )
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit( text_surface, text_rect )

