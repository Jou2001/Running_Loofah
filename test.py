# sprite
from typing import Any
import pygame
import random
import os
import sys

# initial
pygame.init()
# define color
BLACK = (0, 0, 0)
PINHONG = (255, 215, 255) # 品紅
PURPLE = (238, 130, 238) # 紫色
# define screen size
WIDTH = 960
HEIGHT = 600
PLAYER_Y = 270
gravity = 3
# define speed
fps = 50 # 每秒60幀 
# define time
timer = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create screen
pygame.display.set_caption('Running cucumber') # 開始前標題

# load into picture
ground_img = pygame.image.load(os.path.join("img", "ground.png")).convert_alpha()
background_img = pygame.image.load(os.path.join("img", "background01.png")).convert()
background2_img = pygame.image.load(os.path.join("img", "background02.png")).convert()
player_slip_img = pygame.image.load(os.path.join("img", "player_slip.png")).convert_alpha()

obstacle1_img = pygame.image.load(os.path.join("img", "obstacle1.png")).convert_alpha()
obstacle2_img = pygame.image.load(os.path.join("img", "obstacle2.png")).convert_alpha()

class Player(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.load_image = pygame.image.load(os.path.join("img", "player01.png")).convert_alpha()
        self.image = self.load_image
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = PLAYER_Y
        self.speed_y = 8
        self.change_y = 0
        self.radius = 50
        self.run_time = 1
    
    def change_post(self) :
        self.run_time += 1
        if self.run_time == 17 :
            self.run_time = 1

        if self.run_time < 10 :
            self.load_image = pygame.image.load(os.path.join("img", "player0" + str(self.run_time) + ".png")).convert_alpha()
        else :
            self.load_image = pygame.image.load(os.path.join("img", "player" + str(self.run_time) + ".png")).convert_alpha()

        self.image = pygame.transform.scale( self.load_image, (178, 215) )

    def update(self) :
        key_pressed = pygame.key.get_pressed()
        self.change_post()
        if key_pressed[pygame.K_UP] and self.change_y == 0:
            self.change_y = 60

        if self.change_y > 0 or self.rect.y < PLAYER_Y :
            self.rect.y -= self.change_y
            self.change_y -= gravity
        
        if self.rect.y > PLAYER_Y :
            self.rect.y = PLAYER_Y
        if self.rect.y < 50 :
            self.rect.y = 50
        
        if self.rect.y == PLAYER_Y and self.change_y < 0 :
            self.change_y = 0

class Obstacle(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = obstacle2_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(960,1200)
        self.rect.bottom = 500
        self.speed_X = random.randrange(2,4)
        self.radius = 8
        self.randomtype = 1
       
    def change_obstacle(self) :
        self.randomtype = random.randrange(2,3)
        self.image = pygame.image.load(os.path.join("img", "obstacle" + str(self.randomtype) + ".png")).convert_alpha()

    def update(self) :
        self.change_obstacle()
        self.rect.x -= self.speed_X
        if self.rect.right < 0 :
            self.rect.x = random.randrange(960,1200)
            self.speed_X = random.randrange(2,4)

class Ground1(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.bottom = HEIGHT
        self.speed_X = 3

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0 :
            self.rect.x = WIDTH - 10

class Ground2(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 10
        self.rect.bottom = HEIGHT
        self.speed_X = 3

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0 :
            self.rect.x = WIDTH - 10

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
players = pygame.sprite.Group()

ground1 = Ground1()
all_sprites.add(ground1)
ground2 = Ground2()
all_sprites.add(ground2)
player = Player()
all_sprites.add(player)
for i in range(3) :
    o = Obstacle()
    all_sprites.add(o)
    obstacles.add(o)

running = True
while running :
    # get input
    timer.tick(fps)
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

    # update game
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_circle)
    if hits :
        running = False

    # display
    screen.fill(PINHONG)
    screen.blit(background2_img, (0,0))
    all_sprites.draw(screen)
    pygame.display.update()


pygame.quit()