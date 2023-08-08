import pygame
import os
import Merge
obstacle = []
attackObstacles = pygame.sprite.Group()

class Jump_Obstacle(pygame.sprite.Sprite) :
    def __init__(self) :
        for i in range( 3 ) :
            image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
            if i+1 == 3:
                image = pygame.transform.scale( image, (300, 300) )
            obstacle.append( image )
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 10
        self.image = obstacle[0]
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
        for i in range( 3 ) :
            image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
            if i+1 == 3:
                image = pygame.transform.scale( image, (300, 300) )
            obstacle.append( image )
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
        for i in range( 3 ) :
            image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
            if i+1 == 3:
                image = pygame.transform.scale( image, (300, 300) )
            obstacle.append( image )
        pygame.sprite.Sprite.__init__(self)
        self.speed_X = 15
        self.radius = 80
        self.image = obstacle[2]
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