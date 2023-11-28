import pygame
import os
import Material
from Merge import show_hint

JUMP_BOTTOM = 900*Material.COMMOM_R
ATTACK_BOTTOM = 960*Material.COMMOM_R
SLIDE_BOTTOM = 720*Material.COMMOM_R
STEP1 = 1
STEP2 = 2
STEP3 = 3
ATTACK_HIGH = 190*Material.COMMOM_R 
CHICKEN = 2
BALL = 3   
PIG = 4

class Jump_Obstacle(pygame.sprite.Sprite) : # 4.球 408*408
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.img_ori = Material.obstacle[BALL]
        self.image = self.img_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.x = Material.S_WIDTH
        self.rect.bottom = JUMP_BOTTOM # 450
        self.energy = 10
        self.rot_degree = 3
        self.total_degree = 0
        self.mask = pygame.mask.from_surface(self.image) 

    def update(self) :
        self.rotate()
        self.rect.x -= self.speed_X
        if self.rect.right < 0:
            self.kill()

        if self.rect.x < int(Material.S_WIDTH*5/12) and self.rect.x > int(Material.COMMOM_R_W/4):
            show_hint("jump")
    
    def rotate(self) :
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate( self.img_ori, self.total_degree )

class Attack_Obstacle(pygame.sprite.Sprite) : # 1.蟲蟲 202*279  2.老鼠 281*303 4.~6.+7.野豬 
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 10
        self.image = Material.obstacle[PIG]
        self.rect = self.image.get_rect()
        self.rect.x = Material.S_WIDTH
        self.rect.bottom = ATTACK_BOTTOM # 480
        self.gravity = 1
        self.change_y = 3
        self.energy = 13
        self.mask = pygame.mask.from_surface(self.image)  
        self.run_time = 0 
        self.type = STEP1
        self.high = 0
        self.size = 0.7

    def update(self) :
        
        if self.type == STEP1 :
            self.change_post()
        elif self.type == STEP2 :
            self.image = Material.obstacle[7]
            self.high = ATTACK_HIGH   

        self.rect.x -= self.speed_X

        if self.type == STEP1 or self.type == STEP2 :
            self.rect.bottom -= self.change_y
            self.change_y -= self.gravity 

            if self.rect.bottom >= ATTACK_BOTTOM - self.high : # 480
                self.rect.bottom = ATTACK_BOTTOM - self.high
            if self.rect.bottom < ATTACK_BOTTOM - 10 - self.high : # 470
                self.rect.bottom = ATTACK_BOTTOM - 10 - self.high
            
            if self.rect.bottom == ATTACK_BOTTOM - self.high and self.change_y < 0 :
                self.change_y = 3 

        elif self.type == STEP3 :
            self.image = pygame.transform.scale( Material.obstacle[5], (820*Material.COMMOM_R*0.665*self.size, 570*Material.COMMOM_R*0.665*self.size) )
            self.size += 0.1
            if self.size >= 1 :
                self.size = 1
            

            self.rect.bottom += 10
            if self.rect.bottom >= ATTACK_BOTTOM : # 480
                self.rect.bottom = ATTACK_BOTTOM
                self.type = STEP1
                self.change_y = 3
                self.high = 0
                self.run_time = 0 # 0 1 2

        if self.rect.right < 0:
            self.kill()

        if self.rect.x < int(Material.S_WIDTH*5/12) and self.rect.x > int(Material.COMMOM_R_W/4):
            show_hint("attack")
        

    def change_post(self) :
        self.run_time += 1 # 0 1 2
        if self.run_time == 3 :
            self.run_time = 0
        self.image = Material.obstacle[self.run_time + 4] # 4 5 6

class Slide_Obstacle(pygame.sprite.Sprite) : # 3.飛天雞 2048*2048
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.gravity = 5
        self.change_y = 10
        self.radius = 160*Material.COMMOM_R
        self.image = Material.obstacle[CHICKEN]
        self.rect = self.image.get_rect()
        self.rect.x = Material.S_WIDTH
        self.rect.bottom = SLIDE_BOTTOM # 360
        self.energy = 15
        self.mask = pygame.mask.from_surface(self.image)  

    def update(self) :
        self.rect.x -= self.speed_X
        self.rect.bottom -= self.change_y
        self.change_y -= self.gravity 

        if self.rect.bottom >= SLIDE_BOTTOM : # 360
            self.rect.bottom = SLIDE_BOTTOM
        if self.rect.bottom < SLIDE_BOTTOM - 70 : # 290
            self.rect.bottom = SLIDE_BOTTOM - 70
        
        if self.rect.bottom == SLIDE_BOTTOM and self.change_y < 0 :
            self.change_y = 10    

        if self.rect.right < 0:
            self.kill()

        if self.rect.x < int(Material.S_WIDTH*5/12) and self.rect.x > int(Material.COMMOM_R_W/4):
            show_hint("slip")

def New_JumpObstacle(all_sprites, obstacles) :
    o = Jump_Obstacle()
    all_sprites.add(o)
    obstacles.add(o) 

def New_AttackObstacle(all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up) :
    o = Attack_Obstacle()
    all_sprites.add(o)
    obstacles.add(o)
    attackObstacles.add(o)
    attackObstacles_down.add(o)
    o = Attack_Obstacle()
    o.type = STEP2
    o.rect.bottom = ATTACK_BOTTOM - ATTACK_HIGH # 480-95
    o.rect.x = Material.S_WIDTH + 50*Material.COMMOM_R
    all_sprites.add(o)
    obstacles.add(o)
    attackObstacles.add(o)
    attackObstacles_up.add(o)


def New_SlideObstacle(all_sprites, obstacles) :
    o = Slide_Obstacle()
    all_sprites.add(o)
    obstacles.add(o)  