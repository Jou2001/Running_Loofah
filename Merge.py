# sprite
from typing import Any
import pygame
import random
import os
import sys
import cv2
import RecognitionSquat
import RecognitionSquatDown
import RecognitionAttack
import RecongnitionNext
import HeadPlusBody
import Material
import numpy as np
import Set
from moviepy.editor import *
import mediapipe as mp

GAME_TIME = 5

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

all_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
attackObstacles = pygame.sprite.Group()
attackObstacles_down = pygame.sprite.Group()
attackObstacles_up = pygame.sprite.LayeredUpdates()
grounds = pygame.sprite.LayeredUpdates()
a_player = pygame.sprite.LayeredUpdates()

cap = []
# initial
pygame.init()
pygame.mixer.init()

# define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINHONG = (255, 215, 255) # 品紅
PURPLE = (238, 130, 238) # 紫色
GREEN = (101,221,146) # 65DD92
YELLO = (248,218,110) # F8DA6E
RED = (248,141,110) # F88D6E
screen = pygame.display.set_mode((Material.S_WIDTH, Material.S_HEIGHT), pygame.FULLSCREEN) # create screen
pygame.display.set_caption('Running loofah') # 開始前標題
# define speed
fps = 60 # 每秒60幀 
# define time
timer = pygame.time.Clock()

def MoviePlay( mp4 ) :
    running = True
    frames = mp4.iter_frames()

    while running:
        # 获取Pygame事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 获取下一帧电影
        frame = next(frames, None)

        if frame is None:
            # 电影播放完毕，退出循环
            running = False
        else:
            # 在Pygame窗口上顯示
            frame = np.rot90(frame, 3, (1,0) )
            pygame_frame = pygame.surfarray.make_surface(frame)
            pygame_frame = pygame.transform.flip(pygame_frame, True, False)
            screen.blit(pygame_frame, ((int((Material.S_WIDTH-Material.WIDTH)/2)), int((Material.S_HEIGHT-Material.HEIGHT)/2)))
            #print(int((Material.S_WIDTH-Material.WIDTH)/2))
            pygame.display.flip()
            
            timer.tick(fps)

    # 释放资源
    mp4.reader.close()

def draw_start() :
    global cap

    screen.blit(Material.background1_img, (0,0))
    # screen.blit(startgame_word, (0,0))
    # screen.blit(button_start, (380,300))
    pygame.display.update()
    time = 0
    past = pygame.time.get_ticks()

    while time != 3 :
        timer.tick(fps)
        time, past = times_1(time, past)
        screen.blit(Material.background1_img, (0,0))
        txt_line = [ "在某一天，火星撞擊地球，", "一顆絲瓜因此長出手腳，", "開始奔跑起來，", "請協助絲瓜逃離變種生物的掌控，", "勇往直前吧!!", "In a cataclysmic event, Mars collided with Earth,", \
                        "Transforming a loofah with hands and feet,", "It races frantically,", "Help the loofah escape mutant creatures,", "Go all out!"]
        count_line = int(Material.S_HEIGHT/10)
        # print(count_line)
        txt_size = int(40*Material.COMMOM_R_H)
        Material.draw_text( screen, "INTRODUCE", int(100*Material.COMMOM_R_H), int(Material.S_WIDTH/2), count_line, WHITE ) # 60 
        count_line = count_line + txt_size + int(100*Material.COMMOM_R_H)
        for txt in txt_line :
            Material.draw_text( screen, txt, txt_size, int(Material.S_WIDTH/2), count_line, WHITE ) 
            count_line = count_line + 2 * txt_size

        for event in pygame.event.get() :
          if event.type == pygame.QUIT :
            pygame.quit()

        pygame.display.update()


def draw_intro() :
    global cap

    #ReadVideo(do_the_following_mp4, "PLEASE DO THE FOLLOWING", 50)
    #Material.do_the_following_mp4.preview() 
    MoviePlay( Material.do_the_following_mp4 )

   
    key_pressed = pygame.key.get_pressed()
    time = 0
    past = pygame.time.get_ticks()
    count = 0
    p = -1

    active = 1
    waiting = True
    while waiting :
        mode_jump = RecognitionSquat.main(cap)
        mode_down = RecognitionSquatDown.main(cap)
        mode_attack = RecognitionAttack.main(cap)
        mode_next = RecongnitionNext.main(cap)
        ret, img = cap.read()
        time, past = times_1(time, past)

        if time % 1 == 0 and p != time :
            count += 1
            p = time

        if not ret:
          print("Cannot receive frame")
          exit()
      
        timer.tick(fps)
        screen.blit(Material.background1_img, (0,0))

        if active == 1 :
            if count % 2 == 0 :
              screen.blit(Material.intro_jump, (int(200*Material.COMMOM_R_W),int(400*Material.COMMOM_R_H)))              
            else :
              screen.blit(Material.intro_jump_2, (int(200*Material.COMMOM_R_W),int(400*Material.COMMOM_R_H)))        

            Material.draw_text( screen, "HOW TO JUMP", int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/10, WHITE ) # 60
        elif active == 2 :
            if count % 2 == 0 :
              screen.blit(Material.intro_slip_1, (int(200*Material.COMMOM_R_W),int(400*Material.COMMOM_R_H)))
            else :
              screen.blit(Material.intro_slip_1_2, (int(200*Material.COMMOM_R_W),int(400*Material.COMMOM_R_H)))

            Material.draw_text( screen, "HOW TO SLIP No.1", int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/10, WHITE ) # 60
        elif active == 3 :
            if count % 2 == 0 :
              screen.blit(Material.intro_slip_2, (int(200*Material.COMMOM_R_W),int(400*Material.COMMOM_R_H)))
            else :
              screen.blit(Material.intro_slip_2_2, (int(200*Material.COMMOM_R_W),int(400*Material.COMMOM_R_H)))

            Material.draw_text( screen, "HOW TO SLIP No.2", int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/10, WHITE ) # 60
        elif active == 4 :
            if count % 2 == 0 :
              screen.blit(Material.intro_attack, (int(200*Material.COMMOM_R_W),int(340*Material.COMMOM_R_H)))
            else :
              screen.blit(Material.intro_attack_2, (int(200*Material.COMMOM_R_W),int(340*Material.COMMOM_R_H)))
                
            Material.draw_text( screen, "HOW TO ATTACK", int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/10, WHITE ) # 60
        elif active == 5 :
            if count % 2 == 0 :
                screen.blit(Material.intro_handup_left, (int(200*Material.COMMOM_R_W),int(340*Material.COMMOM_R_H))) # 200*340 
            else :
                screen.blit(Material.intro_handup_right, (int(200*Material.COMMOM_R_W),int(340*Material.COMMOM_R_H)))
            Material.draw_text( screen, "HOW TO SKIP", int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/10, WHITE ) # 60
        else :
            waiting = False

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            # if event.type == pygame.KEYDOWN :
            #    if event.key == pygame.K_UP :
            #        active += 1
        preview = img.copy() 
        
        rgbframe = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        
        results = pose.process(rgbframe) # 從影像增測姿勢
       
        # mp_drawing.draw_landmarks(preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # mp_drawing.draw_landmarks(preview, results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS) 
      
        preview = cv2.resize(preview,(int(preview.shape[1]*1.2*Material.COMMOM_R_W),int(preview.shape[0]*1.2*Material.COMMOM_R_H)))

        
        preview = np.rot90(preview)   
        preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        preview = pygame.surfarray.make_surface(preview)
        screen.blit(preview, ( int(900*Material.COMMOM_R_W), int(400*Material.COMMOM_R_H) ) )

        key_pressed = pygame.key.get_pressed() 

        if ((mode_jump == 1 or key_pressed[pygame.K_UP] ) and active == 1 ) or \
           ((mode_down == 1 or key_pressed[pygame.K_DOWN]) and ( active == 2 or active == 3 )) or \
           ((mode_attack == 1 or key_pressed[pygame.K_LEFT]) and active == 4) or \
           ((mode_next == 1 or key_pressed[pygame.K_RETURN]) and active == 5) :
            active += 1
            Material.good_mp3.play()
            Material.draw_text( screen, "Good!" , int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(200*Material.COMMOM_R), WHITE )
            pygame.display.update()
            pygame.time.wait(500) 
        else :
            Material.draw_text( screen, "Bad!" , int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(200*Material.COMMOM_R), WHITE )
            pygame.display.update()
         
    
def draw_init() :
    global cap
    screen.blit(Material.background1_img, (0,0))
    pygame.display.update()
    time = 0
    past = pygame.time.get_ticks()


    while time != 3 :
        timer.tick(fps)
        time, past = times_1(time, past)
        screen.blit(Material.background1_img, (0,0))
        Material.draw_text( screen, 'align your head with the circle', int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/5, WHITE )
        Material.draw_text( screen, 'please raise your hand', int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/5+int(100*Material.COMMOM_R), WHITE )

        for event in pygame.event.get() :
          if event.type == pygame.QUIT :
            pygame.quit()

        pygame.display.update()


    screen.blit(Material.background1_img, (0,0))
    pygame.display.update()
    faceOK = HeadPlusBody.Photograph( screen, fps, timer, cap ) 


    MoviePlay( Material.start321_mp4 ) 

    Material.load_image = []
    for i in range( 16 ) :
      image = pygame.image.load(os.path.join("picture", "player" , "RUN_" + str(i+1) + ".png")).convert_alpha()
      image = pygame.transform.scale( image, (359*Material.COMMOM_R, 433*Material.COMMOM_R) ) # 359*433
      Material.load_image.append( image )
      
    Material.player_slip_img = pygame.image.load(os.path.join("picture", "player", "player_slip_1.png")).convert_alpha()
    Material.player_slip_img = pygame.transform.scale( Material.player_slip_img, (470*Material.COMMOM_R, 256*Material.COMMOM_R) ) # 470*256
    Material.healthstate_head = pygame.image.load(os.path.join("picture","player" , "HEALTHHEAD_1.png")).convert_alpha()
    Material.healthstate_head = pygame.transform.scale( Material.healthstate_head, (200*Material.COMMOM_R*0.65, 201*Material.COMMOM_R*0.65) ) # 200*201


def times_1(time, past) :
    now = pygame.time.get_ticks()
    if ( int(( now - past ) / 1000) == 1 ) :
        past = now
        time += 1
    return time, past

#def times_2(time, past) :
def times_2(time, past, player) :
    now = pygame.time.get_ticks()
    if ( int(( now - past ) / 1000) == 1 ) :
        past = now
        time += 1
        player.count_jump()
    
    secs = time % 60
    mins = int(time/60) % 60
    hours = int(time/3600) % 24
    Material.draw_text( screen, f"{hours:02}:{mins:02}:{secs:02}", int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT, WHITE )
    return time, past

class Player(pygame.sprite.Sprite) :
    global cap, all_sprites

    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = Material.load_image[0]
        self.rect = self.image.get_rect()
        self.rect.x = int(160*Material.COMMOM_R_W)
        self.rect.y = Material.PLAYER_Y
        self.speed_y = 8
        self.change_y = 0
        self.radius = int(200*Material.COMMOM_R)
        self.run_time = 0
        self.health = Material.HEALTH
        self.countJump = Material.PLAYER_JUMP 
        self.countdown = Material.PLAYER_DOWN
        self.countattack = Material.PLAYER_ATTACK
        self.mode_jump = 0
        self.mode_down = 0
        self.mode_attack = 0
        self.key_pressed = 0
        self.isGoodJump = 0
        self.isGoodDown = 0    
        self.isGoodAttack = 0  
        self.keyjump = 0
        self.keydown = 0
        self.keyattack = 0   
        self.mask = pygame.mask.from_surface(self.image)  
        self.end_ground_size = 406*Material.COMMOM_R
        self.end = 0
        self.small = 0.9

    def update(self) :
        self.mode_jump = RecognitionSquat.main(cap)
        self.mode_down = RecognitionSquatDown.main(cap)
        self.mode_attack = RecognitionAttack.main(cap)
        self.change_post() # update pose
        if self.end == 0 :
            self.jump()
            self.down()
            self.shoot()
        elif self.end == 1 : # minimum player
            print("small player")
            self.image = pygame.transform.scale( self.image, (359*Material.COMMOM_R*self.small/0.9, 433*Material.COMMOM_R*self.small/0.9) )
            # print(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        elif self.end == 2 : # maintain player's size
            self.image = pygame.transform.scale( self.image, (359*Material.COMMOM_R*self.small/0.9, 433*Material.COMMOM_R*self.small/0.9) ) 
 
    def change_post(self) : # update pose
        self.run_time += 1
        if self.run_time == 16 :
            self.run_time = 0
        self.image = Material.load_image[self.run_time] # update pose

    def count_jump(self) :
        self.countJump -= 1
        if self.countJump < 0 :
            self.countJump = 0

    def jump(self):  
        key_pressed = pygame.key.get_pressed() 
        if self.mode_jump == 1:
            self.isGoodJump += 1 
        if self.mode_jump == 3:
            self.isGoodJump = 0 

        if key_pressed[pygame.K_UP] :
            self.keyjump = 1
        if key_pressed[pygame.K_RIGHT] :
            self.keyjump = 2
            
        if (self.mode_jump == 1 and self.change_y == 0 and self.countJump >= 0 and self.isGoodJump >= 2) or \
           (key_pressed[pygame.K_UP] and self.change_y == 0 and self.countJump >= 0) : # key_pressed[pygame.K_RIGHT]
            if self.rect.y == Material.PLAYER_Y :
              Material.jump_mp3.play()   

            self.change_y = 120*Material.COMMOM_R
            self.countJump = Material.PLAYER_JUMP

        elif self.change_y > 0 or self.rect.y < Material.PLAYER_Y : 
            self.rect.y -= self.change_y
            self.change_y -= Material.gravity
            if (self.countJump > 0 and self.change_y < 0 and ( self.mode_jump == 1 and self.mode_jump == 2 ) ) or \
               (self.countJump > 0 and self.change_y < 0 and ( key_pressed[pygame.K_UP] or key_pressed[pygame.K_RIGHT] )) :
                self.rect.y += self.change_y
                self.change_y += Material.gravity
            if (self.countJump > 0 and self.change_y < 0 and ( self.mode_jump == 3 or self.mode_jump == None ) ) or \
               (self.countJump > 0 and self.change_y < 0 and ( not key_pressed[pygame.K_UP] and not key_pressed[pygame.K_RIGHT] )) :
                self.countJump = 0

        # keep height and low
        if self.rect.y >= Material.PLAYER_Y : 
            self.rect.y = Material.PLAYER_Y
            self.countJump = Material.PLAYER_JUMP
        if self.rect.y < int(100*Material.COMMOM_R_H) :
            self.rect.y = int(100*Material.COMMOM_R_H)
        
        if self.rect.y == Material.PLAYER_Y and self.change_y < 0 :
            self.change_y = 0    

    def count_down(self) :
        self.countdown -= 1
        if self.countdown < 0 :
            self.countdown = 0

    def down(self):       
        key_pressed = pygame.key.get_pressed()
        if self.mode_down == 1:
            self.isGoodDown += 1
        if self.mode_down == 3:
            self.isGoodDown = 0

        if (self.mode_down == 1 and self.change_y == 0 and self.countdown >= 0 and self.isGoodDown >= 2) or \
           (key_pressed[pygame.K_DOWN] and self.countdown >= 0) : # key_pressed[pygame.K_RIGHT]
            self.countdown = Material.PLAYER_DOWN
            self.image = Material.player_slip_img     
            self.rect.y = Material.PLAYER_Y + int(170*Material.COMMOM_R_H)

        elif (self.countdown > 0 and self.mode_down == 1 and self.mode_down == 2 ) or \
             (self.countdown > 0 and ( key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_LEFT] )) :
            self.image = Material.player_slip_img 
            self.rect.y = Material.PLAYER_Y + int(170*Material.COMMOM_R_H)
            
        elif (self.countdown > 0 and ( self.mode_down == 3 or self.mode_down == None ) ) or \
             (self.countdown > 0 and ( not key_pressed[pygame.K_DOWN] and not key_pressed[pygame.K_LEFT] )) :
            self.countdown = 0
            self.image = Material.load_image[0]
            self.run_time = 0 
            self.rect.y = Material.PLAYER_Y
            self.isGoodDown = 0

    def shoot(self) :
        key_pressed = pygame.key.get_pressed()
        if self.mode_attack == 1:
            self.isGoodAttack += 1
        if self.mode_attack == 3:
            self.isGoodAttack = 0

        if (self.mode_attack == 1 and self.countattack >= 0 and self.isGoodAttack >= 2) or \
           (key_pressed[pygame.K_LEFT]) :
            bullet = Bullet(self.rect.right, ((self.rect.y+self.rect.bottom)/2+int(40*Material.COMMOM_R)))
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.countattack = Material.PLAYER_ATTACK
            
        elif (self.countattack > 0 and (self.mode_attack == 1 and self.mode_attack == 2) ) or \
             (self.countattack > 0 and ( key_pressed[pygame.K_LEFT] ) ):
            self.countattack -= 1
            bullet = Bullet(self.rect.right, ((self.rect.y+self.rect.bottom)/2+int(40*Material.COMMOM_R)))
            all_sprites.add(bullet)
            bullets.add(bullet)

    def ending_minify(self) :
        self.image = pygame.transform.scale( self.image, (359*Material.COMMOM_R*self.small, 433*Material.COMMOM_R*self.small) )


class Bullet(pygame.sprite.Sprite) :
    def __init__(self, x, y) :
        pygame.sprite.Sprite.__init__(self)
        self.img_ori = Material.bullet
        self.image = self.img_ori
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange( x, x+int(80*Material.COMMOM_R) )
        self.rect.bottom = y
        self.radius = int(46*Material.COMMOM_R)
        self.speedx = 50  
        self.rot_degree = random.randrange( 20, 40 )
        self.total_degree = 0  

    def update(self) :
        self.rotate()
        self.rect.x += self.speedx
        if self.rect.left >= Material.S_WIDTH:
            self.kill()

    def rotate(self) :
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate( self.img_ori, self.total_degree )

class Ground(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randrange(0, 5)
        self.image = Material.ground_img[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.bottom = Material.HEIGHT + int(60*Material.COMMOM_R)
        self.speed_X = 10
        self.end = 0
        self.diff = 0
        self.small = 1
        self.end_height = Material.HEIGHT + int(60*Material.COMMOM_R) - self.rect.height
        self.sum_height = 0
        self.lastPost = 0

    def update(self) :
        if self.end != 1 :
          self.rect.x -= self.speed_X

        if self.end == 1 :
            self.ending_minify()

        if self.rect.right <= 0 :
            if self.end == 0 :
                self.rect.x = (Material.GROUND_NUM-1)*(int(420*Material.COMMOM_R)) + self.rect.right
            elif self.end == 1 :
                pass
            elif self.end == 2 :
                pass
                #if self.rect.x <= -self.rect.width:
                  #self.rect.x = self.lastPost
                  #self.rect.x = (Material.GROUND_NUM-1)*(int(self.rect.width)) + self.rect.right
              
    
    def ending_minify(self) :
        pass
    

class Cloud(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = Material.cloud[random.randrange( 0, 3 )]
        self.rect = self.image.get_rect()
        self.rect.x = Material.S_WIDTH # 960
        self.rect.y = random.randrange( 0, int(400*Material.COMMOM_R) )
        self.speed_X = random.randrange( 10, 15 )

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right <= 0:
            self.kill()

class Tree(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randrange( 6, 11 )
        self.type = random.randrange( 0, 2 )
        self.image = Material.tree[self.type]
        if self.type == 0 :
            self.image = pygame.transform.scale( self.image, (638*Material.COMMOM_R*self.size/10, 478*Material.COMMOM_R*self.size/10) ) # 638*478
        else:
            self.image = pygame.transform.scale( self.image, (448*Material.COMMOM_R*self.size/10, 848*Material.COMMOM_R*self.size/10) ) # 488*848
        self.rect = self.image.get_rect()
        self.rect.x = Material.S_WIDTH # 960
        self.rect.bottom = int(1060*Material.COMMOM_R_H)
        self.speed_X = 10

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right <= 0:
            self.kill()

class Sun(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.img_ori = Material.sun
        self.image = self.img_ori
        self.rect = self.image.get_rect()
        self.rect.center = (int(1460*Material.COMMOM_R_W), int(160*Material.COMMOM_R_H)) # 960
        self.rot_degree = 2
        self.total_degree = 0  

    def update(self) :
        self.rotate()

    def rotate(self) :
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate( self.img_ori, self.total_degree )
        self.rect = self.image.get_rect()
        self.rect.center = (int(1460*Material.COMMOM_R_W), int(160*Material.COMMOM_R_H)) # 960

def draw_health(surf, hp, x, y ):
    if hp < 0:
      hp = 0
    fill = (hp/100) * Material.BAR_LENGTH
    outline_rect = pygame.Rect(x, y, Material.BAR_LENGTH, Material.BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, Material.BAR_HEIGHT)
    if ( hp >= Material.HEALTH / 2 ) :
        pygame.draw.rect(surf, GREEN, fill_rect)
    elif ( hp >= Material.HEALTH / 6 ) :
        pygame.draw.rect(surf, YELLO, fill_rect)
    else :
        pygame.draw.rect(surf, RED, fill_rect)

    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def end_animate() :
    global all_sprites, grounds, a_player

    #計算地板要加幾塊
    add_ground_num = int( Material.WIDTH / int( np.power(0.9, 6) * int(420*Material.COMMOM_R))) + 1 - Material.GROUND_NUM

    # sort
    index_max = 0
    x_max = grounds.get_sprite(0).rect.x
    index_min = 0
    x_min = grounds.get_sprite(0).rect.x
    grounds.get_sprite(0).end = 1
    a_player.get_sprite(0).end = 1

    for i in range(1, len(grounds)) :
        grounds.get_sprite(i).end = 1
        if x_max < grounds.get_sprite(i).rect.x :
            x_max = grounds.get_sprite(i).rect.x
            index_max = i
        if x_min > grounds.get_sprite(i).rect.x :
            x_min = grounds.get_sprite(i).rect.x
            index_min = i

    #for i in range(index_min, len(grounds)) :
    #    grounds.move_to_back(grounds.get_sprite(len(grounds) - 1))
    for i in range(len(grounds)):
        if i == 0:
          grounds.get_sprite(i).rect.x = 0
        else :
          grounds.get_sprite(i).rect.x = grounds.get_sprite(i-1).rect.right

    mid = len(grounds) - 1
    # add new grounds
    total_len = grounds.get_sprite(len(grounds)-1).rect.right
    for i in range(add_ground_num+1):
        ground = Ground()
        ground.rect.x = ground.rect.x + total_len
        ground.end = 1
        all_sprites.add(ground)
        grounds.add(ground)
        total_len = total_len + 420*Material.COMMOM_R
 
    # 角色縮小
    a_player.update() 
  
    # 地板縮小 、 填補空隙(前進) 
    time = 0
    screen.blit(Material.background4_img, (0,0))
    past = pygame.time.get_ticks()

    time = 0
    x_last_gd = len(grounds) - 1
    # minimum frequency
    num = 1
    # UFO
    displacement = 10*Material.COMMOM_R_H
    height = 0.2 # go down
    height_change = 0.015
    height_g = 0.005
    up_down = 1 # 0: go up 1: go down
    stop = 0
    x_UFO = Material.WIDTH
    # obstacle
    pig_num = -1 # 0 ~ 3
    pig = Material.end_pig[0]
    chick = Material.end_chicken
    ob_p_x = -30*Material.COMMOM_R
    ob_p_y = ground.rect.y + 20 * Material.COMMOM_R
    ob_ch_x = -200*Material.COMMOM_R
    ob_ch_y = Material.HEIGHT * 0.3
    while time != 18 :
        timer.tick(fps)
        time, past = times_1(time, past)  
        screen.blit(Material.background4_img, (0,0))
        # print(time)
        if num < 6 :
          # init ground's x
          for i in range(len(grounds)):
              if i <= mid :
                Material.draw_text( screen, str(i) + " " + str(grounds.get_sprite(i).rect.width) , int(40*Material.COMMOM_R), int(grounds.get_sprite(i).rect.x), Material.BAR_HEIGHT + int(400*Material.COMMOM_R), BLACK )  
              else:  
                Material.draw_text( screen, str(i) + " " + str(grounds.get_sprite(i).rect.width) , int(40*Material.COMMOM_R), int(grounds.get_sprite(i).rect.x), Material.BAR_HEIGHT + int(400*Material.COMMOM_R), WHITE )  
          # add new grounds
          for i in range(len(grounds)):   
            gd = grounds.get_sprite(i) 
            gd.image = pygame.transform.scale( gd.image, (gd.rect.width*0.9, gd.rect.height*0.9) )
            x = gd.rect.x
            bottom = gd.rect.bottom
            gd.rect = gd.image.get_rect()
            gd.rect.x = x
            gd.rect.bottom = bottom
            if i > 0 :       
                gd.rect.x = grounds.get_sprite(i-1).rect.right
     
          # minimum player's size and y
          a_player.get_sprite(0).small = a_player.get_sprite(0).small * 0.9
          a_player.get_sprite(0).end_ground_size = a_player.get_sprite(0).end_ground_size*0.9
          a_player.get_sprite(0).rect.y = a_player.get_sprite(0).rect.y + 433*Material.COMMOM_R*a_player.get_sprite(0).small*0.1 + a_player.get_sprite(0).end_ground_size*0.1

        else:
            # UFO x
            if stop == 1 :
                displacement = -10*Material.COMMOM_R_H

            x_UFO = x_UFO - displacement
            if x_UFO < Material.WIDTH * 0.72 :
                x_UFO = Material.WIDTH * 0.72
            # UFO y
            height -= height_change
            height_change -= height_g
            if height >= 0.2 :
                height = 0.2
            if height <= 0.18 :
                height = 0.18

            if up_down == 1 :
                if height == 0.2 and height_change <= 0 :
                    height_change = -0.015
                    height_g = -height_g
                    up_down = 0
            elif up_down == 0 :
                if height == 0.18 and height_change >= 0 :
                    height_change = 0.015
                    height_g = -height_g
                    up_down = 1

            # player maintain size
            a_player.get_sprite(0).end = 2
            # player go ahead
            if a_player.get_sprite(0).rect.x < Material.WIDTH * 0.8 :
                a_player.get_sprite(0).rect.x += int(18*Material.COMMOM_R_W)
            if a_player.get_sprite(0).rect.x >= Material.WIDTH * 0.8 :
                a_player.get_sprite(0).rect.x = Material.WIDTH * 0.8
                # player go up 
                a_player.get_sprite(0).rect.y -= int(10*Material.COMMOM_R_W)
                if a_player.get_sprite(0).rect.y <= Material.HEIGHT * 0.21 :
                    a_player.clear(screen, screen)
                    stop = 1


            # ground go ahead
            for i in range(len(grounds)):   
                gd = grounds.get_sprite(i)
                if num == 6:
                  gd.end = 2
                
                if gd.rect.x <= -gd.rect.width:
                    gd.rect.x = grounds.get_sprite(x_last_gd).rect.right
                    x_last_gd = i

            grounds.update()
            if num > 7 :
                pig_num += 1 
                if pig_num > 3 :
                    pig_num = 0
                print(len(Material.end_pig),pig_num)
                pig = Material.end_pig[pig_num]
                screen.blit(pig, (ob_p_x, ob_p_y))
                ob_p_x += 10*Material.COMMOM_R
            if num > 13 :
                screen.blit(chick, (ob_ch_x, ob_ch_y))
                ob_ch_x += 10*Material.COMMOM_R
                
        num = num + 1
        # 角色縮小
        grounds.draw(screen)
        if stop == 0 :
            a_player.update() 
            a_player.draw(screen)

        if num >= 6 :
            screen.blit(Material.end_UFO, (x_UFO, Material.HEIGHT * height))

        for event in pygame.event.get() :
          if event.type == pygame.QUIT :
            pygame.quit()

        pygame.display.update()

def run():
    global cap, all_sprites, attackObstacles, attackObstacles_down, attackObstacles_up

    show_init = True
    running = True
    changeTime = True
    pretime = 0

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    else :
      #pygame.mixer_music.load(os.path.join("mp3", "startMusic.mp3"))
      #pygame.mixer_music.play()
      #draw_start()
      #draw_intro()
      
      o = Sun()
      back_sprites.add(o)

      while running :       
          # get input
          timer.tick(fps)
          
          if show_init :
                # open camera
                if not pygame.mixer.music.get_busy() :
                    # pygame.mixer_music.load(os.path.join("mp3", "startMusic.mp3"))
                    # pygame.mixer_music.play()
                    pass

                draw_init()
                
                # pygame.mixer_music.load(os.path.join("mp3", "game_music.mp3"))
                # pygame.mixer_music.play()
                # init timer
                time = 0
                now = pygame.time.get_ticks()
                past = now


                show_init = False
                all_sprites = pygame.sprite.Group()
                obstacles = pygame.sprite.Group()

                total_len = 0
                for i in range(0, Material.GROUND_NUM) :
                    ground = Ground()
                    ground.rect.x = ground.rect.x + total_len
                    all_sprites.add(ground)
                    grounds.add(ground)
                    total_len = total_len + int(420*Material.COMMOM_R)

                count = random.randrange( 1, 3 )
                for i in range( 0, count ) :
                    o = Cloud()
                    o.rect.x = random.randrange( 20, Material.S_WIDTH )
                    back_sprites.add(o)

                count = random.randrange( 1, 3 )
                for i in range( 0, count ) :
                    o = Tree()
                    o.rect.x = random.randrange( 20, Material.S_WIDTH )
                    back_sprites.add(o)

                player = Player()
                a_player.add(player)
                all_sprites.add(player)

          for event in pygame.event.get() :
              if event.type == pygame.QUIT :
                  running = False

          ret, frame = cap.read()

          if not ret:
            print("Read Error")
            exit()     
          else :
              preview = frame.copy()
              rgbframe = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
              results = pose.process(rgbframe) # 從影像增測姿勢  
              mp_drawing.draw_landmarks(preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
              preview = cv2.resize(preview, (int(300*Material.COMMOM_R), int(200*Material.COMMOM_R)))
              preview = np.rot90(preview)
              preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
              preview = pygame.surfarray.make_surface(preview) 

              # Create obstacle
              functions = [(Set.Set1), (Set.Set2), (Set.Set3), (Set.Set4), (Set.Set5)]
              
              
              if changeTime and time <= GAME_TIME :
                  # 隨機選擇並調用一個函數
                  if time % 30 == 0:
                      func = random.choice(functions)
                  func(time, all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up)
                  #Set.Set1(time, all_sprites, obstacles, attackObstacles, attackObstacles_down, attackObstacles_up)

              # update game
              back_sprites.update()
              all_sprites.update()
              pygame.display.update()
             
              # display
              screen.blit(Material.background4_img, (0,0))
              backornot = random.randrange( 0, 60 )
              if backornot == 4 :
                o = Cloud()
                back_sprites.add(o)

              if backornot == 20 :
                o = Tree()
                back_sprites.add(o)
              
              back_sprites.draw(screen)
              all_sprites.draw(screen)
              screen.blit(preview, ( 0, int(1000*Material.COMMOM_R) ) )
              draw_health(screen, player.health, int(120*Material.COMMOM_R_W), int(64*Material.COMMOM_R_H) )
              screen.blit(Material.healthstate_head, (int(20*Material.COMMOM_R_W),int(20*Material.COMMOM_R_H)))
              
              # timer
              #time, past = times_2(time, past)
              time, past = times_2(time, past, player)

              if time != pretime:
                  pretime = time
                  changeTime = True
              else:
                  changeTime = False

              '''
              if ( time == -1 ) :
                  show_init = True  
              '''
              # print( "now: ", now, " past: ", past, "now-past: ", ( now - past ) / 1000 )
              player.key_pressed = pygame.key.get_pressed()
              if player.mode_jump == 1 or player.keyjump == 1 :
              #if player.key_pressed[pygame.K_UP] :
                  Material.draw_text( screen, "Good Jump!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(40*Material.COMMOM_R), WHITE )
              elif player.mode_jump == 2 or player.keyjump == 2 :
              #elif player.key_pressed[pygame.K_RIGHT] :
                  Material.draw_text( screen, "So so Jump!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(40*Material.COMMOM_R), WHITE )
              elif player.mode_jump == 3 or player.keyjump == 0 :
                  Material.draw_text( screen, "Bad Jump!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(40*Material.COMMOM_R), WHITE )
                  
              if player.mode_down == 1 or player.keydown == 1 :
              #if player.key_pressed[pygame.K_UP] :
                  Material.draw_text( screen, "Good Slip!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(80*Material.COMMOM_R), WHITE )
              elif player.mode_down == 2 or player.keydown == 2 :
              #elif player.key_pressed[pygame.K_RIGHT] :
                  Material.draw_text( screen, "So so Slip!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(80*Material.COMMOM_R), WHITE )
              elif player.mode_down == 3 or player.keydown == 0 :
                  Material.draw_text( screen, "Bad Slip!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(80*Material.COMMOM_R), WHITE )
                  
              if player.mode_attack == 1 or player.keyattack == 1 :
              #if player.key_pressed[pygame.K_UP] :
                  Material.draw_text( screen, "Good Attack!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(120*Material.COMMOM_R), WHITE )
              elif player.mode_attack == 2 or player.keyattack == 2 :
              #elif player.key_pressed[pygame.K_RIGHT] :
                  Material.draw_text( screen, "So so Attack!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(120*Material.COMMOM_R), WHITE )
              elif player.mode_attack == 3 or player.keyattack == 0 :
                  Material.draw_text( screen, "Bad Attack!" , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(120*Material.COMMOM_R), WHITE )
              
              Material.draw_text( screen, str(len(obstacles)) , int(40*Material.COMMOM_R), Material.S_WIDTH/2, Material.BAR_HEIGHT + int(160*Material.COMMOM_R), WHITE )
              
              pygame.sprite.groupcollide(attackObstacles, bullets, True, True)
              hits = pygame.sprite.spritecollide(player, obstacles, True, pygame.sprite.collide_mask) # 注意碰撞範圍
              for hit in hits :               
                  #player.health -= hit.energy
                  if player.health <= 0 : # death
                      screen.blit(Material.background1_img, (0,0))
                      pygame.display.update()   
                      MoviePlay( Material.lose_mp4 )
                      all_sprites.clear(screen, screen)
                      grounds.clear(screen, screen)
                      a_player.clear(screen, screen)
                      back_sprites.clear(screen, screen)
                      show_init = True
              
              hits = pygame.sprite.groupcollide(attackObstacles_down, attackObstacles_up, False, False)
              if len(attackObstacles_up) > len(hits) :
                for i in range ( len(attackObstacles_up) - len(hits) )  :
                    if attackObstacles_up.get_sprite(i).type == 2:
                        attackObstacles_up.get_sprite(i).type = 3
                        attackObstacles_up.get_sprite(i).size = 0.7
                        attackObstacles_up.get_sprite(i).change_y = 0
                  
              # successful
              if len(obstacles) == 0 and time > GAME_TIME and player.health > 0:
                    end_animate() 
                    screen.blit(Material.background1_img, (0,0))
                    pygame.display.update()   
                    MoviePlay( Material.win_mp4 ) 
                    all_sprites.clear(screen, screen)
                    grounds.clear(screen, screen)
                    back_sprites.clear(screen, screen)
                    show_init = True

              pygame.display.update()

      
      pygame.quit()


if __name__ == '__main__':
    run()