# sprite
from typing import Any
import pygame
import random
import os
import sys
import cv2
import RecognitionSquat
import HeadPlusBody
import numpy as np

# frame after state
preview = []
# initial
pygame.init()
# define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINHONG = (255, 215, 255) # 品紅
PURPLE = (238, 130, 238) # 紫色
GREEN = (101,221,146) # 65DD92
YELLO = (248,218,110) # F8DA6E
RED = (248,141,110) # F88D6E
# define screen size
WIDTH = 960
HEIGHT = 600
# define player initial position
PLAYER_Y = 270
#define player continuous jump time
PLAYER_JUMP = 2
gravity = 5
# define player health
HEALTH = 100
# define health size
BAR_LENGTH = 200
BAR_HEIGHT = 20
# define speed
fps = 60 # 每秒60幀 
# define time
timer = pygame.time.Clock()


screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create screen
pygame.display.set_caption('Running loofah') # 開始前標題
# load into picture
ground_img = pygame.image.load(os.path.join("img", "ground.png")).convert_alpha()
background1_img = pygame.image.load(os.path.join("img", "background01.png")).convert()
background2_img = pygame.image.load(os.path.join("img", "background02.png")).convert()
takephoto = pygame.image.load(os.path.join("img", "takephoto.png")).convert_alpha()
takephoto = pygame.transform.scale( takephoto, (WIDTH, HEIGHT) )
button_start = pygame.image.load(os.path.join("img", "button_start.png")).convert_alpha()
button_start = pygame.transform.scale( button_start, (200, 200) )
startgame_word = pygame.image.load(os.path.join("img", "startgame_word.png")).convert_alpha()
startgame_word = pygame.transform.scale( startgame_word, (WIDTH, HEIGHT) )
load_image = []
obstacle = []
player_slip_img = pygame.image.load(os.path.join("img", "player_slip.png")).convert_alpha()
healthstate_head = pygame.image.load(os.path.join("img", "healthstate_head.png")).convert_alpha()
# load into txt
fout_txt = os.path.join( "Handwriting.ttf" )

def draw_text( surf, text, size, x, y ) :
    font = pygame.font.Font( fout_txt, size )
    text_surface = font.render( text, True, WHITE )
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit( text_surface, text_rect )

def draw_start() :
    key_pressed = pygame.key.get_pressed()
    screen.blit(background1_img, (0,0))
    # screen.blit(startgame_word, (0,0))
    # screen.blit(button_start, (380,300))
    pygame.display.update()
    waiting = True
    init_time = 3
    time = init_time
    past = pygame.time.get_ticks()
    while time != 0 :
        timer.tick(fps)
        time, past = times_1(time, past)
        screen.blit(background1_img, (0,0))
        txt_line = [ "在某一天，火星撞擊地球，", "一顆絲瓜因此長出手腳，", "開始奔跑起來，", "請協助絲瓜逃離變種生物的掌控，", "勇往直前吧!!", "In a cataclysmic event, Mars collided with Earth,", \
                        "Transforming a loofah with hands and feet,", "It races frantically,", "Help the loofah escape mutant creatures,", "Go all out!"]
        count_line = HEIGHT/10
        plus = 20
        txt_size = 20
        draw_text( screen, "INTRODUCE", 50, WIDTH/2, count_line ) # 60
        count_line = count_line + plus + 50
        for txt in txt_line :
            draw_text( screen, txt, txt_size, WIDTH/2, count_line ) 
            count_line = count_line + plus + txt_size
        
        pygame.display.update()

    init_time = 30
    time = init_time
    active = 1
    while waiting :
        timer.tick(fps)
        time, past = times_1(time, past)
        screen.blit(background1_img, (0,0))
        if time >= init_time - 2 :
            draw_text( screen, "PLEASE DO THE FOLLOWING", 50, WIDTH/2, HEIGHT/10 ) # 60
        else :
            waiting = False
            # key_pressed = pygame.key.get_pressed()
            # print( key_pressed[pygame.K_RIGHT] )
            # if active == 1 :
            #     draw_text( screen, "HOW TO JUMP", 50, WIDTH/2, HEIGHT/10 ) # 60
            #     if key_pressed[pygame.K_RIGHT] :
            #         print( "????????????" )
            #         active += 1
            # elif active == 2 :
            #     draw_text( screen, "HOW TO SLIP", 50, WIDTH/2, HEIGHT/10 ) # 60
            #     if key_pressed[pygame.K_UP] :
            #         active += 1
            # elif active == 3 :
            #     draw_text( screen, "HOW TO ATTACK", 50, WIDTH/2, HEIGHT/10 ) # 60
            #     if key_pressed[pygame.K_UP] :
            #         active += 1
            # else :
            #     waiting = False
        
        pygame.display.update()

    
def draw_init() :
    global player_slip_img, healthstate_head
    screen.blit(background1_img, (0,0))
    draw_text( screen, 'running loofah', 65, WIDTH/2, HEIGHT/10 )
    draw_text( screen, 'align your head with the circle', 30, WIDTH/2, HEIGHT/5 )
    pygame.display.update()
    faceOK = HeadPlusBody.main( screen, fps, timer ) 
    waiting = True
    while waiting :
      timer.tick(fps)
      for event in pygame.event.get() :
          if event.type == pygame.QUIT :
            pygame.quit()
          elif faceOK :
            waiting = False

    screen.blit(background1_img, (0,0))
    draw_text( screen, 'squat to jump', 30, WIDTH/2, HEIGHT/2 )
    pygame.display.update()
    waiting = True
    while waiting :
      timer.tick(fps)
      for event in pygame.event.get() :
        if event.type == pygame.QUIT :
          pygame.quit()
        elif event.type == pygame.KEYUP :
          waiting = False

    for i in range( 16 ) :
      image = pygame.image.load(os.path.join("picture", "player" , "RUN_" + str(i+1) + ".png")).convert_alpha()
      image = pygame.transform.scale( image, (178, 215) )
      load_image.append( image )

    player_slip_img = pygame.image.load(os.path.join("img", "player_slip.png")).convert_alpha()
    healthstate_head = pygame.image.load(os.path.join("picture","player" , "HEALTHHEAD_1.png")).convert_alpha()
    healthstate_head = pygame.transform.scale( healthstate_head, (58, 53) )
    for i in range( 3 ) :
      image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
      obstacle.append( image )

def times_1(time, past) :
    now = pygame.time.get_ticks()
    if ( int(( now - past ) / 1000) == 1 ) :
        past = now
        time -= 1
    return time, past

def times_2(time, past, player) :
    now = pygame.time.get_ticks()
    if ( int(( now - past ) / 1000) == 1 ) :
        past = now
        time -= 1
        player.count_jump()
    
    secs = time % 60
    mins = int(time/60) % 60
    hours = int(time/3600) % 24
    draw_text( screen, f"{hours:02}:{mins:02}:{secs:02}", 20, WIDTH/2, BAR_HEIGHT )
    return time, past

class Player(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image[0]
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.y = PLAYER_Y
        self.speed_y = 8
        self.change_y = 0
        self.radius = 100
        self.run_time = 0
        self.health = HEALTH
        self.countJump = PLAYER_JUMP
        self.mode = 0
        self.key_pressed = 0

    def count_jump(self) :
        self.countJump -= 1
        if self.countJump < 0 :
            self.countJump = 0
    
    def change_post(self) :
        self.run_time += 1
        if self.run_time == 16 :
            self.run_time = 0
        self.image = load_image[self.run_time]

    def update(self) :
        self.mode = RecognitionSquat.main(preview)
        key_pressed = pygame.key.get_pressed()
        self.change_post()
        
        if self.mode == 1 and self.change_y == 0 and self.countJump >= 0 :
        # if key_pressed[pygame.K_UP] and self.change_y == 0 and self.countJump >= 0 : # key_pressed[pygame.K_RIGHT]
           print( "pressed\n" )
           self.change_y = 60
           self.countJump = PLAYER_JUMP

        if self.change_y > 0 or self.rect.y < PLAYER_Y :
            self.rect.y -= self.change_y
            self.change_y -= gravity
            if self.countJump > 0 and self.change_y < 0 and self.mode != 3 :
            #if self.countJump > 0 and self.change_y < 0 and ( key_pressed[pygame.K_UP] or key_pressed[pygame.K_RIGHT] ) :
                self.rect.y += self.change_y
                self.change_y += gravity
            if self.countJump > 0 and self.change_y < 0 and self.mode == 3 :
            #if self.countJump > 0 and self.change_y < 0 and ( not key_pressed[pygame.K_UP] and not key_pressed[pygame.K_RIGHT] ) :
                self.countJump = 0

        # keep height and low
        if self.rect.y >= PLAYER_Y : 
            self.rect.y = PLAYER_Y
            self.countJump = PLAYER_JUMP
        if self.rect.y < 50 :
            self.rect.y = 50
        
        if self.rect.y == PLAYER_Y and self.change_y < 0 :
            self.change_y = 0

        # print( "count: ", self.countJump, " change_y: ", self.change_y ) 

class Obstacle(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        print("size: ", len(obstacle))
        self.image = obstacle[random.randrange(0,2)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(960,1200)
        self.rect.bottom = 500
        self.speed_X = 10
        self.radius = 10
        self.randomtype = random.randrange(0,2)
       
    def change_obstacle(self) :
        self.randomtype = random.randrange(0,2)
        self.image = obstacle[self.randomtype]

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0 :
            self.rect.x = random.randrange(960,1200)
            self.speed_X = 10
            self.change_obstacle()

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
        self.rect.x = WIDTH 
        self.rect.bottom = HEIGHT
        self.speed_X = 3

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right < 0 :
            self.rect.x = WIDTH - 10

def New_Obstacle(all_sprites, obstacles) :
    o = Obstacle()
    all_sprites.add(o)
    obstacles.add(o)    

def draw_health(surf, hp, x, y ):
    if hp < 0:
      hp = 0
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if ( hp >= HEALTH / 2 ) :
        pygame.draw.rect(surf, GREEN, fill_rect)
    elif ( hp >= HEALTH / 6 ) :
        pygame.draw.rect(surf, YELLO, fill_rect)
    else :
        pygame.draw.rect(surf, RED, fill_rect)

    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def run():
    global preview 

    show_init = True
    running = True
    
    draw_start()

    while running :
        # get input
        timer.tick(fps)
        
        if show_init :
            draw_init()
            # init timer
            time = 200
            now = pygame.time.get_ticks()
            past = now
            # open camera
            cap = cv2.VideoCapture(0)

            show_init = False
            all_sprites = pygame.sprite.Group()
            obstacles = pygame.sprite.Group()

            ground1 = Ground1()
            all_sprites.add(ground1)
            ground2 = Ground2()
            all_sprites.add(ground2)
            player = Player()
            all_sprites.add(player)

            for i in range(3) :
                New_Obstacle(all_sprites, obstacles)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False

        ret, frame = cap.read()


        if ret:
            frame = cv2.resize(frame, (150, 100))
            frame = np.rot90(frame)
            preview = frame.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = pygame.surfarray.make_surface(frame)
            #frame = cv2.flip(frame, 1) #矩陣左右翻轉 
            #frame = cv2.resize(frame, (650, 500))

            # update game
            all_sprites.update()
            #screen.blit(frame, ( 0,0 ) )
            pygame.display.update()
            #cv2.imshow('frame', preview)
            
            hits = pygame.sprite.spritecollide(player, obstacles, True, pygame.sprite.collide_circle) # 注意碰撞範圍
            for hit in hits :
                New_Obstacle(all_sprites, obstacles)
                player.health -= hit.radius
                if player.health <= 0 :
                    show_init = True
                    cap.release()
                    cv2.destroyAllWindows()
            # display
            screen.blit(background2_img, (0,0))
            all_sprites.draw(screen)
            screen.blit(frame, ( 0, 500 ) )
            draw_health(screen, player.health, 60, 32 )
            screen.blit(healthstate_head, (10,10))
            # timer
            time, past = times_2(time, past, player)
            if ( time == -1 ) :
                show_init = True

            # print( "now: ", now, " past: ", past, "now-past: ", ( now - past ) / 1000 )

            player.key_pressed = pygame.key.get_pressed()
            if player.mode == 1 :
            #if player.key_pressed[pygame.K_UP] :
                draw_text( screen, "Good!" , 20, WIDTH/2, BAR_HEIGHT + 20 )
            elif player.mode == 2 :
            #elif player.key_pressed[pygame.K_RIGHT] :
                draw_text( screen, "So so!" , 20, WIDTH/2, BAR_HEIGHT + 20 )
            else :
                draw_text( screen, "Bad!" , 20, WIDTH/2, BAR_HEIGHT + 20 )

            pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    run()