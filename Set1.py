# 跳起（深蹲）：3秒（重複三次）
# 趴下（左右跨步蹲）：3秒（重複三次）
# 攻擊（後跨步蹲抬手）：3秒（重複三次）
# 休息三秒換下一個組合


import pygame, random

obstacle = []

class Obstacle(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        print("size: ", len(obstacle))
        self.image = obstacle[random.randint(0,2)]
        self.rect = self.image.get_rect()
        self.rect.x = 960
        self.rect.bottom = 500
        self.speed_X = 15
        self.radius = 10
        self.randomtype = random.randrange(0,2)
       
    def change_obstacle(self) :
        self.randomtype = random.randrange(0,2)
        self.image = obstacle[self.randomtype]

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0 :
            self.rect.x = 960
            self.speed_X = 15
            self.change_obstacle()


def New_Obstacle(all_sprites, obstacles) :
    o = Obstacle()
    all_sprites.add(o)
    obstacles.add(o)  

def Run(time, all_sprites, obstacles, obstacle1):
    global obstacle
    obstacle = obstacle1
    if time == 60:
        New_Obstacle(all_sprites, obstacles)
    elif time == 57:
        New_Obstacle(all_sprites, obstacles)
    # return all_sprites, obstacles
