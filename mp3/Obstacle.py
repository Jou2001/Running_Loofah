import pygame
import os
import Merge
obstacle = []
attackObstacles = pygame.sprite.Group()

class Jump_Obstacle(pygame.sprite.Sprite) :
    def __init__(self) :
        image = pygame.image.load(os.path.join("img", "obstacle4.png")).convert_alpha()
        image = pygame.transform.scale( image, (204, 204) ) # 球 408*408
        '''
        for i in range( 4 ) :
            image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
            if i+1 == 1:
                image = pygame.transform.scale( image, (101, 140) ) # 蟲蟲 202*279
            if i+1 == 2:
                image = pygame.transform.scale( image, (140, 151) ) # 老鼠 281*303
            if i+1 == 3:
                image = pygame.transform.scale( image, (300, 300) ) # 飛天雞 2048*2048
            if i+1 == 4:
                image = pygame.transform.scale( image, (408, 408) ) # 球 408*408
            obstacle.append( image )
        '''
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 10
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 960
        self.rect.bottom = 500
        self.energy = 10

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0:
            self.kill()

class Attack_Obstacle(pygame.sprite.Sprite) :
    def __init__(self) :
        for i in range( 0, 2 ) :
            image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
            if i+1 == 1:
                image = pygame.transform.scale( image, (101, 140) ) # 蟲蟲 202*279
            if i+1 == 2:
                image = pygame.transform.scale( image, (140, 151) ) # 老鼠 281*303
            obstacle.append( image )
        '''
        for i in range( 4 ) :
            image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
            if i+1 == 1:
                image = pygame.transform.scale( image, (101, 140) ) # 蟲蟲 202*279
            if i+1 == 2:
                image = pygame.transform.scale( image, (140, 151) ) # 老鼠 281*303
            if i+1 == 3:
                image = pygame.transform.scale( image, (300, 300) ) # 飛天雞 2048*2048
            if i+1 == 4:
                image = pygame.transform.scale( image, (408, 408) ) # 球 408*408
            obstacle.append( image )
        '''
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 10
        self.image = obstacle[1]
        self.rect = self.image.get_rect()
        self.rect.x = 960
        self.rect.bottom = 500
        self.energy = 10

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0:
            self.kill()

class Slide_Obstacle(pygame.sprite.Sprite) :
    def __init__(self) :
        image = pygame.image.load(os.path.join("img", "obstacle3.png")).convert_alpha()
        image = pygame.transform.scale( image, (300, 300) ) # 飛天雞 2048*2048

        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 80
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 960
        self.rect.bottom = 350
        self.energy = 15

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