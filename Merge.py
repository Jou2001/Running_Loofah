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
import numpy as np
import Set
from moviepy.editor import *
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_drawing_styles = mp.solutions.drawing_styles
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

all_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
attackObstacles = pygame.sprite.Group()

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
# define screen size
WIDTH = 960
HEIGHT = 600
# define player initial position
PLAYER_Y = 270
#define player continuous jump time
PLAYER_JUMP = 2
PLAYER_DOWN = 2
PLAYER_ATTACK = 2
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
ground_img = pygame.image.load(os.path.join("img", "ground01.png")).convert_alpha()
ground_img = pygame.transform.scale( ground_img, (960, 203) )
background1_img = pygame.image.load(os.path.join("img", "background01.png")).convert()
background1_img = pygame.transform.scale( background1_img, (960, 600) )
background2_img = pygame.image.load(os.path.join("img", "background02.png")).convert()
background2_img = pygame.transform.scale( background2_img, (960, 600) )
background3_img = pygame.image.load(os.path.join("img", "background03.png")).convert()
background3_img = pygame.transform.scale( background3_img, (960, 600) )
background4_img = pygame.image.load(os.path.join("img", "background04.png")).convert()
background4_img = pygame.transform.scale( background4_img, (960, 600) )

takephoto = pygame.image.load(os.path.join("img", "takephoto.png")).convert_alpha()
takephoto = pygame.transform.scale( takephoto, (WIDTH, HEIGHT) )

intro_attack = pygame.image.load(os.path.join("img", "intro_attack.png")).convert_alpha()
intro_attack = pygame.transform.scale( intro_attack, (210, 340) ) # 420*680
intro_jump = pygame.image.load(os.path.join("img", "intro_jump.png")).convert_alpha()
intro_jump = pygame.transform.scale( intro_jump, (170, 295) ) # 340*590
intro_slip_1 = pygame.image.load(os.path.join("img", "intro_slip_1.png")).convert_alpha()
intro_slip_1 = pygame.transform.scale( intro_slip_1, (280, 300) ) # 560*300
intro_slip_2 = pygame.image.load(os.path.join("img", "intro_slip_2.png")).convert_alpha()
intro_slip_2 = pygame.transform.scale( intro_slip_2, (280, 300) ) # 560*300
intro_handup_left = pygame.image.load(os.path.join("img", "intro_handup_left.png")).convert_alpha()
intro_handup_left = pygame.transform.scale( intro_handup_left, (234, 334) ) # 468*668
intro_handup_right = pygame.image.load(os.path.join("img", "intro_handup_right.png")).convert_alpha()
intro_handup_right = pygame.transform.scale( intro_handup_right, (234, 334) ) # 468*668

bullet = pygame.image.load(os.path.join("img", "bullet.png")).convert_alpha()
bullet = pygame.transform.scale( bullet, (50, 57) )

cloud = []
for i in range(0, 3) :
    image = pygame.image.load(os.path.join("img", "cloud0" + str(i+1) + ".png")).convert_alpha()
    if i+1 == 1:
        image = pygame.transform.scale( image, (174, 99) ) # 348*178
    if i+1 == 2:
        image = pygame.transform.scale( image, (109, 79) ) # 218*158
    if i+1 == 3 :
        image = pygame.transform.scale( image, (179, 104) ) # 358*208
    cloud.append( image )

tree = []
image = pygame.image.load(os.path.join("img", "grove.png")).convert_alpha()
image = pygame.transform.scale( image, (319, 239) ) # 638*478
tree.append( image )
image = pygame.image.load(os.path.join("img", "tree.png")).convert_alpha()
image = pygame.transform.scale( image, (244, 424) ) # 488*848
tree.append( image )

sun = pygame.image.load(os.path.join("img", "sun.png")).convert_alpha()
sun = pygame.transform.scale( sun, (100, 100) ) # 200*200

#load mp4
do_the_following_mp4 = VideoFileClip(os.path.join("video", "do_the_following.mp4")).resize((960,600))
start321_mp4 = VideoFileClip(os.path.join("video", "start321_mp3.mp4")).resize((960,600))
win_mp4 = VideoFileClip(os.path.join("video", "win_mp3.mp4")).resize((960,600))
lose_mp4 = VideoFileClip(os.path.join("video", "lose_mp3.mp4")).resize((960,600))

#load music mp3
camera_mp3 = pygame.mixer.Sound(os.path.join("mp3", "cameraMusic.mp3"))
jump_mp3 = pygame.mixer.Sound(os.path.join("mp3", "jumpMusic.mp3"))
good_mp3 = pygame.mixer.Sound(os.path.join("mp3", "Good.mp3"))


load_image = []
player_slip_img = pygame.image.load(os.path.join("img", "player_slip.png")).convert_alpha()
healthstate_head = pygame.image.load(os.path.join("img", "healthstate_head.png")).convert_alpha()
# load into txt
fout_txt = os.path.join( "Handwriting.ttf" )


obstacle = []
for i in range(0, 4) :
    image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
    if i+1 == 1:
        image = pygame.transform.scale( image, (101, 140) ) # 蟲蟲 202*279
    if i+1 == 2:
        image = pygame.transform.scale( image, (140, 151) ) # 老鼠 281*303
    if i+1 == 3 :
        image = pygame.transform.scale( image, (300, 300) ) # 飛天雞 2048*2048
    if i+1 == 4 :
        image = pygame.transform.scale( image, (204, 204) ) # 球 408*408
    obstacle.append( image )



def ReadVideo(videoName, txt, txtSize) :
    video = cv2.VideoCapture(videoName)
    video_fps = video.get(cv2.CAP_PROP_FPS)
    while True :
        timer.tick(video_fps)
        ret, frame = video.read()
        if ret == True :
            frame = cv2.resize(frame,(960,600))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame, -1)
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.flip(frame, False, True)
            screen.blit(frame, ( 0, 0 ) ) 
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()
            if ( txt != "" ):        
              draw_text( screen, txt, txtSize, WIDTH/2, HEIGHT/10 ) # 60
            pygame.display.flip()
        else : 
            break

def draw_text( surf, text, size, x, y ) :
    font = pygame.font.Font( fout_txt, size )
    # font = pygame.font.SysFont( "arial", size )
    text_surface = font.render( text, True, WHITE )
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit( text_surface, text_rect )

def draw_start() :
    global cap

    screen.blit(background1_img, (0,0))
    # screen.blit(startgame_word, (0,0))
    # screen.blit(button_start, (380,300))
    pygame.display.update()
    time = 0
    past = pygame.time.get_ticks()

    while time != 3 :
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

        for event in pygame.event.get() :
          if event.type == pygame.QUIT :
            pygame.quit()

        pygame.display.update()

def draw_intro() :
    global cap

    #ReadVideo(do_the_following_mp4, "PLEASE DO THE FOLLOWING", 50)
    do_the_following_mp4.preview()
   
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

        if time % 2 == 0 and p != time :
            count += 1
            p = time

        if not ret:
          print("Cannot receive frame")
          exit()
      
        timer.tick(fps)
        screen.blit(background1_img, (0,0))

        if active == 1 :
            screen.blit(intro_jump, (100,200))
            draw_text( screen, "HOW TO JUMP", 50, WIDTH/2, HEIGHT/10 ) # 60
        elif active == 2 :
            screen.blit(intro_slip_1, (100,200))
            draw_text( screen, "HOW TO SLIP No.1", 50, WIDTH/2, HEIGHT/10 ) # 60
        elif active == 3 :
            screen.blit(intro_slip_2, (100,200))
            draw_text( screen, "HOW TO SLIP No.2", 50, WIDTH/2, HEIGHT/10 ) # 60
        elif active == 4 :
            screen.blit(intro_attack, (100,170))
            draw_text( screen, "HOW TO ATTACK", 50, WIDTH/2, HEIGHT/10 ) # 60
        elif active == 5 :
            if count % 2 == 0 :
                screen.blit(intro_handup_left, (100,170))
            else :
                screen.blit(intro_handup_right, (100,170))
            draw_text( screen, "HOW TO SKIP", 50, WIDTH/2, HEIGHT/10 ) # 60
        else :
            waiting = False

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
            # if event.type == pygame.KEYDOWN :
            #    if event.key == pygame.K_UP :
            #        active += 1
        preview = img.copy() 
        
        # img = cv2.resize(img,(int(img.shape[1]*0.6),int(img.shape[0]*0.6)))
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = np.rot90(img)
        # img = pygame.surfarray.make_surface(img)
        # screen.blit(img, ( 450, 200 ) )

        
        rgbframe = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        
        results = pose.process(rgbframe) # 從影像增測姿勢
       
        # mp_drawing.draw_landmarks(preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # mp_drawing.draw_landmarks(preview, results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS) 
        # cv2.imshow( "AAAA", cv2.flip(preview, 1)) 
      
        preview = cv2.resize(preview,(int(preview.shape[1]*0.6),int(preview.shape[0]*0.6)))

        
        preview = np.rot90(preview)   
        preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        preview = pygame.surfarray.make_surface(preview)
        screen.blit(preview, ( 450, 200 ) )

        key_pressed = pygame.key.get_pressed() 

        if (mode_jump == 1 or key_pressed[pygame.K_UP] ) and active == 1 :
            active += 1
            good_mp3.play()
            draw_text( screen, "Good!" , 50, WIDTH/2, BAR_HEIGHT + 100 )
            pygame.display.update()
            pygame.time.wait(500) 
        elif (mode_down == 1 or key_pressed[pygame.K_DOWN]) and ( active == 2 or active == 3 ) :
            active += 1
            good_mp3.play()
            draw_text( screen, "Good!" , 50, WIDTH/2, BAR_HEIGHT + 100 ) 
            pygame.display.update()
            pygame.time.wait(500) 
        elif (mode_attack == 1 or key_pressed[pygame.K_LEFT]) and active == 4 :
            active += 1
            good_mp3.play()
            draw_text( screen, "Good!" , 50, WIDTH/2, BAR_HEIGHT + 100 )
            pygame.display.update()
            pygame.time.wait(500) 
        elif (mode_next == 1 or key_pressed[pygame.K_RETURN]) and active == 5 :
            active += 1
            good_mp3.play()
            draw_text( screen, "Good!" , 50, WIDTH/2, BAR_HEIGHT + 100 )
            pygame.display.update()
            pygame.time.wait(500) 
        else :
            draw_text( screen, "Bad!" , 50, WIDTH/2, BAR_HEIGHT + 100 )
            pygame.display.update()
        
    
def draw_init() :
    global player_slip_img, healthstate_head, load_image, cap
    screen.blit(background1_img, (0,0))
    pygame.display.update()
    time = 0
    past = pygame.time.get_ticks()


    while time != 3 :
        timer.tick(fps)
        time, past = times_1(time, past)
        screen.blit(background1_img, (0,0))
        draw_text( screen, 'align your head with the circle', 50, WIDTH/2, HEIGHT/5 )
        draw_text( screen, 'please raise your hand', 50, WIDTH/2, HEIGHT/5+50 )

        for event in pygame.event.get() :
          if event.type == pygame.QUIT :
            pygame.quit()

        pygame.display.update()


    screen.blit(background1_img, (0,0))
    pygame.display.update()
    faceOK = HeadPlusBody.Photograph( screen, fps, timer, cap ) 


    start321_mp4.preview()

    load_image = []
    for i in range( 16 ) :
      image = pygame.image.load(os.path.join("picture", "player" , "RUN_" + str(i+1) + ".png")).convert_alpha()
      image = pygame.transform.scale( image, (178, 215) )
      load_image.append( image )
      
    player_slip_img = pygame.image.load(os.path.join("picture", "player", "player_slip_1.png")).convert_alpha()
    player_slip_img = pygame.transform.scale( player_slip_img, (235, 128) )
    healthstate_head = pygame.image.load(os.path.join("picture","player" , "HEALTHHEAD_1.png")).convert_alpha()
    healthstate_head = pygame.transform.scale( healthstate_head, (58, 53) )
    # for i in range( 3 ) :
    #  image = pygame.image.load(os.path.join("img", "obstacle" + str(i+1) + ".png")).convert_alpha()
    #  obstacle.append( image )


def times_1(time, past) :
    now = pygame.time.get_ticks()
    if ( int(( now - past ) / 1000) == 1 ) :
        past = now
        time += 1
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
    global cap, jump_mp3, all_sprites

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
        self.countdown = PLAYER_DOWN
        self.countattack = PLAYER_ATTACK
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

    def update(self) :
        self.mode_jump = RecognitionSquat.main(cap)
        self.mode_down = RecognitionSquatDown.main(cap)
        self.mode_attack = RecognitionAttack.main(cap)
        self.change_post()
        
        self.jump()
        self.down()
        self.shoot()
 
    def change_post(self) :
        self.run_time += 1
        if self.run_time == 16 :
            self.run_time = 0
        self.image = load_image[self.run_time]

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
            if self.rect.y == PLAYER_Y :
              jump_mp3.play()   

            self.change_y = 60
            self.countJump = PLAYER_JUMP

        elif self.change_y > 0 or self.rect.y < PLAYER_Y : 
            self.rect.y -= self.change_y
            self.change_y -= gravity
            if (self.countJump > 0 and self.change_y < 0 and ( self.mode_jump == 1 and self.mode_jump == 2 ) ) or \
               (self.countJump > 0 and self.change_y < 0 and ( key_pressed[pygame.K_UP] or key_pressed[pygame.K_RIGHT] )) :
                self.rect.y += self.change_y
                self.change_y += gravity
            if (self.countJump > 0 and self.change_y < 0 and ( self.mode_jump == 3 or self.mode_jump == None ) ) or \
               (self.countJump > 0 and self.change_y < 0 and ( not key_pressed[pygame.K_UP] and not key_pressed[pygame.K_RIGHT] )) :
                self.countJump = 0

        # keep height and low
        if self.rect.y >= PLAYER_Y : 
            self.rect.y = PLAYER_Y
            self.countJump = PLAYER_JUMP
        if self.rect.y < 50 :
            self.rect.y = 50
        
        if self.rect.y == PLAYER_Y and self.change_y < 0 :
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
            self.countdown = PLAYER_DOWN
            self.image = player_slip_img     
            self.rect.y = PLAYER_Y + 85

        elif (self.countdown > 0 and self.mode_down == 1 and self.mode_down == 2 ) or \
             (self.countdown > 0 and ( key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_LEFT] )) :
            self.image = player_slip_img 
            self.rect.y = PLAYER_Y + 85
            
        elif (self.countdown > 0 and ( self.mode_down == 3 or self.mode_down == None ) ) or \
             (self.countdown > 0 and ( not key_pressed[pygame.K_DOWN] and not key_pressed[pygame.K_LEFT] )) :
            self.countdown = 0
            self.image = load_image[0]
            self.run_time = 0 
            self.rect.y = PLAYER_Y
            self.isGoodDown = 0

    def shoot(self) :
        key_pressed = pygame.key.get_pressed()
        if self.mode_attack == 1:
            self.isGoodAttack += 1
        if self.mode_attack == 3:
            self.isGoodAttack = 0

        if (self.mode_attack == 1 and self.countattack >= 0 and self.isGoodAttack >= 2) or \
           (key_pressed[pygame.K_LEFT]) :
            bullet = Bullet(self.rect.right, ((self.rect.y+self.rect.bottom)/2+10))
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.countattack = PLAYER_ATTACK
            
        elif (self.countattack > 0 and (self.mode_attack == 1 and self.mode_attack == 2) ) or \
             (self.countattack > 0 and ( key_pressed[pygame.K_LEFT] ) ):
            self.countattack -= 1
            bullet = Bullet(self.rect.right, ((self.rect.y+self.rect.bottom)/2+10))
            all_sprites.add(bullet)
            bullets.add(bullet)

class Bullet(pygame.sprite.Sprite) :
    def __init__(self, x, y) :
        pygame.sprite.Sprite.__init__(self)
        self.img_ori = bullet
        self.image = self.img_ori
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange( x, x+40 )
        self.rect.bottom = y
        self.radius = 23
        self.speedx = 50  
        self.rot_degree = random.randrange( 20, 40 )
        self.total_degree = 0  

    def update(self) :
        self.rotate()
        self.rect.x += self.speedx
        if self.rect.left >= WIDTH:
            self.kill()

    def rotate(self) :
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate( self.img_ori, self.total_degree )

class Ground(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_img
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.bottom = HEIGHT + 30
        self.speed_X = 10

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right <= 0 :
            self.rect.x = WIDTH

class Cloud(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = cloud[random.randrange( 0, 3 )]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH # 960
        self.rect.y = random.randrange( 0, 200 )
        self.speed_X = random.randrange( 10, 15 )

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right <= 0:
            self.kill()

class Tree(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randrange( 0, 2 )
        self.image = tree[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH # 960
        self.rect.bottom = 530 
        self.speed_X = 10

    def update(self) :
        self.rect.x -= self.speed_X
        if self.rect.right <= 0:
            self.kill()

class Sun(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.img_ori = sun
        self.image = self.img_ori
        self.rect = self.image.get_rect()
        self.rect.x = 720 # 960
        self.rect.y = 50
        self.speed_X = 10
        self.rot_degree = 5
        self.total_degree = 0  

    def update(self) :
        self.rotate()

    def rotate(self) :
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate( self.img_ori, self.total_degree )


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

def show_hint(action):
    if action == "attack":
        attack_action = pygame.transform.scale( intro_attack, (42, 68) ) # 420*680
        screen.blit(attack_action, (145,60))
        draw_text( screen, "Attack!", 50, 95, 60 )
    elif action == "slip":
        slip_action = pygame.transform.scale( intro_slip_1, (56, 30) ) # 560*300
        screen.blit(slip_action, (135,60))
        draw_text( screen, "Slip!", 50, 80, 60 )
    elif action == "jump":
        jump_action = pygame.transform.scale( intro_jump, (50, 70) ) # 340*590
        screen.blit(jump_action, (135,60))
        draw_text( screen, "Jump!", 50, 80, 60 )


def run():
    global cap, all_sprites, attackObstacles

    show_init = True
    running = True
    changeTime = True
    pretime = 60

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    else :
      pygame.mixer_music.load(os.path.join("mp3", "startMusic.mp3"))
      pygame.mixer_music.play()
      # draw_start()
      # draw_intro()

      while running :       
          # get input
          timer.tick(fps)
          
          if show_init :
                # open camera
                if not pygame.mixer.music.get_busy() :
                    pygame.mixer_music.load(os.path.join("mp3", "startMusic.mp3"))
                    pygame.mixer_music.play()

                draw_init()
                
                pygame.mixer_music.load(os.path.join("mp3", "game_music.mp3"))
                pygame.mixer_music.play()
                # init timer
                time = 60
                now = pygame.time.get_ticks()
                past = now


                show_init = False
                all_sprites = pygame.sprite.Group()
                obstacles = pygame.sprite.Group()

                ground01 = Ground()
                all_sprites.add(ground01)
                ground02 = Ground()
                ground02.rect.x = WIDTH
                all_sprites.add(ground02)

                o = Sun()
                back_sprites.add(o)

                count = random.randrange( 1, 3 )
                for i in range( 0, count ) :
                    o = Cloud()
                    o.rect.x = random.randrange( 20, WIDTH )
                    back_sprites.add(o)

                count = random.randrange( 1, 3 )
                for i in range( 0, count ) :
                    o = Tree()
                    o.rect.x = random.randrange( 20, WIDTH )
                    back_sprites.add(o)

                player = Player()
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
              #frame = cv2.resize(frame, (150, 100))
              #frame = np.rot90(frame)
              #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
              #frame = pygame.surfarray.make_surface(frame) 
              ### cv2.imshow( "AAAA", cv2.flip(frame, 1)) 
              rgbframe = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
              results = pose.process(rgbframe) # 從影像增測姿勢  
              mp_drawing.draw_landmarks(preview, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
              preview = cv2.resize(preview, (150, 100))
              preview = np.rot90(preview)
              preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
              preview = pygame.surfarray.make_surface(preview) 

              # Create obstacle
              functions = [(Set.Set1), (Set.Set2), (Set.Set3), (Set.Set4), (Set.Set5)]
              
              if changeTime:
                  # 隨機選擇並調用一個函數
                  #if time % 30 == 0:
                      #func = random.choice(functions)
                  #func(time, all_sprites, obstacles)
                  Set.Set1(time, all_sprites, obstacles, attackObstacles)

              # update game
              back_sprites.update()
              all_sprites.update()
              pygame.display.update()
             
              # display
              screen.blit(background4_img, (0,0))
              backornot = random.randrange( 0, 60 )
              if backornot == 4 :
                o = Cloud()
                back_sprites.add(o)
              if backornot == 20 :
                o = Tree()
                back_sprites.add(o)
              
              back_sprites.draw(screen)
              all_sprites.draw(screen)
              screen.blit(preview, ( 0, 500 ) )
              #screen.blit(frame, ( 0, 500 ) )
              draw_health(screen, player.health, 60, 32 )
              screen.blit(healthstate_head, (10,10))
              
              # timer
              time, past = times_2(time, past, player)

              if time != pretime:
                  pretime = time
                  changeTime = True
              else:
                  changeTime = False

              if ( time == -1 ) :
                  show_init = True  

              # print( "now: ", now, " past: ", past, "now-past: ", ( now - past ) / 1000 )

              player.key_pressed = pygame.key.get_pressed()
              if player.mode_jump == 1 or player.keyjump == 1 :
              #if player.key_pressed[pygame.K_UP] :
                  draw_text( screen, "Good Jump!" , 20, WIDTH/2, BAR_HEIGHT + 20 )
              elif player.mode_jump == 2 or player.keyjump == 2 :
              #elif player.key_pressed[pygame.K_RIGHT] :
                  draw_text( screen, "So so Jump!" , 20, WIDTH/2, BAR_HEIGHT + 20 )
              elif player.mode_jump == 3 or player.keyjump == 0 :
                  draw_text( screen, "Bad Jump!" , 20, WIDTH/2, BAR_HEIGHT + 20 )
                  
              if player.mode_down == 1 or player.keydown == 1 :
              #if player.key_pressed[pygame.K_UP] :
                  draw_text( screen, "Good Slip!" , 20, WIDTH/2, BAR_HEIGHT + 40 )
              elif player.mode_down == 2 or player.keydown == 2 :
              #elif player.key_pressed[pygame.K_RIGHT] :
                  draw_text( screen, "So so Slip!" , 20, WIDTH/2, BAR_HEIGHT + 40 )
              elif player.mode_down == 3 or player.keydown == 0 :
                  draw_text( screen, "Bad Slip!" , 20, WIDTH/2, BAR_HEIGHT + 40 )
                  
              if player.mode_attack == 1 or player.keyattack == 1 :
              #if player.key_pressed[pygame.K_UP] :
                  draw_text( screen, "Good Attack!" , 20, WIDTH/2, BAR_HEIGHT + 60 )
              elif player.mode_attack == 2 or player.keyattack == 2 :
              #elif player.key_pressed[pygame.K_RIGHT] :
                  draw_text( screen, "So so Attack!" , 20, WIDTH/2, BAR_HEIGHT + 60 )
              elif player.mode_attack == 3 or player.keyattack == 0 :
                  draw_text( screen, "Bad Attack!" , 20, WIDTH/2, BAR_HEIGHT + 60 )

              pygame.sprite.groupcollide(attackObstacles, bullets, True, True)
              hits = pygame.sprite.spritecollide(player, obstacles, True, pygame.sprite.collide_mask) # 注意碰撞範圍
              for hit in hits :               
                  player.health -= hit.energy
                  if player.health <= 0 :
                      lose_mp4.preview()
                      show_init = True
    

              if time == 0 and  player.health > 0:
                  win_mp4.preview()
                  show_init = True

            #   pygame.display.update()

      pygame.quit()


if __name__ == '__main__':
    run()