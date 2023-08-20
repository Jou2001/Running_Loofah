import pygame
import os
import Merge

attackObstacles = pygame.sprite.Group()    

class Jump_Obstacle(pygame.sprite.Sprite) : # 4.球 408*408
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 100
        self.img_ori = Merge.obstacle[3]
        self.image = self.img_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 960
        self.rect.bottom = 450
        self.energy = 10
        self.rot_degree = 3
        self.total_degree = 0
        self.mask = pygame.mask.from_surface(self.image)  

    def update(self) :
        self.rotate()
        self.rect.x -= self.speed_X
        if self.rect.right < 0:
            self.kill()
    
    def rotate(self) :
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate( self.img_ori, self.total_degree )

class Attack_Obstacle(pygame.sprite.Sprite) : # 1.蟲蟲 202*279  2.老鼠 281*303
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 10
        self.image = Merge.obstacle[1]
        self.rect = self.image.get_rect()
        self.rect.x = 960
        self.rect.bottom = 500
        self.energy = 10
        self.mask = pygame.mask.from_surface(self.image)  

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0:
            self.kill()

class Slide_Obstacle(pygame.sprite.Sprite) : # 3.飛天雞 2048*2048
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 80
        self.image = Merge.obstacle[2]
        self.rect = self.image.get_rect()
        self.rect.x = 960
        self.rect.bottom = 350
        self.energy = 15
        self.mask = pygame.mask.from_surface(self.image)  

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0:
            self.kill()

def New_JumpObstacle(all_sprites, obstacles) :
    o = Jump_Obstacle()
    all_sprites.add(o)
    obstacles.add(o) 

def New_AttackObstacle(all_sprites, obstacles, attackObstacles) :
    o = Attack_Obstacle()
    all_sprites.add(o)
    obstacles.add(o)
    attackObstacles.add(o)


def New_SlideObstacle(all_sprites, obstacles) :
    o = Slide_Obstacle()
    all_sprites.add(o)
    obstacles.add(o)  