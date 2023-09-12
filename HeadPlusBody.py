import os
import cv2
import numpy as np
from PIL import Image
import pygame
import RecongnitionNext
import Material

PURPLE = (77, 97, 255)
WHITE = (255, 255, 255)
pygame.mixer.init()
#load music mp3
camera_mp3 = pygame.mixer.Sound(os.path.join("mp3", "cameraMusic.mp3"))

path_input = "./picture"

def CompositePicture(input_head, input_body, path_output, index, minify):
  if os.path.isfile(input_head) and os.path.isfile(input_body):
    img_head = Image.open( input_head )
    img_body = Image.open( input_body )
    img_body = img_body.convert("RGBA") 

    widthB , heightB = img_body.size
    widthA , heightA = img_head.size
    new_img_head  = img_head.resize((int((widthA/(Material.COMMOM_R*2))*minify[0]),int((heightA/(Material.COMMOM_R*2))*minify[0])), Image.LANCZOS)
    new_img_body  = img_body.resize(img_body.size,Image.LANCZOS)
    new_img_head = new_img_head.rotate(minify[3])  
    
    resultPicture = Image.new('RGBA', img_body.size, (0, 0, 0, 0))   

    resultPicture.paste(new_img_head, (minify[1],minify[2]), new_img_head)
    resultPicture.paste(new_img_body, (0,0), new_img_body )
    resultPicture.save( path_output + str(index) + ".png" )

    return True
  
  else:
     return False

def imge_cut_Circle(input_img):
  # 取得cv2.IMREAD_UNCHANGED,讀取帶透明(Alpha)通道的圖片數據
  img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
  height, width, channel = img.shape
  # 創建一個4通道的新圖片ㄝ包含透明通道，初始化是透明的
  img_new = np.zeros((height, width, 4 ), np.uint8)
  img_new[:, :, 0:3] = img[:, :, 0:3]
  # 創建一個1通道的新圖片，設置最大內接圓不透明
  img_circle = np.zeros((height, width, 1 ), np.uint8)
  # 設為全透明
  img_circle[:, :, :] = 0
  # 設置最大內接圓不透明
  img_circle = cv2.circle(img_circle, (width//2, width//2), int(min(height, width)/2), 255, -1 )
  # 圖片融合
  img_new[:, :, 3] = img_circle[:, :, 0]
  cv2.imwrite( path_input +'/head_body/head.png', img_new)
  return path_input + '/head_body/head.png' 

'''
# 定義加入文字的函式
def putText(source, x, y, text, scale=2.5, color=(0,0,0)):
    org = (x,y)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = scale
    thickness = 5
    lineType = cv2.LINE_AA
    cv2.putText(source, text, org, fontFace, fontScale, color, thickness, lineType)
'''

def Photograph(screen, fps, timer, cam):

  a = 0 
  sec = 0
  if not cam.isOpened():
      print("Cannot open camera")
      exit()
  while True:
    ret, img = cam.read()
    if not ret:
        print("Cannot receive frame")
        break
    
  
    # cv2.rectangle( img, (x1, y1), (x2, y2), (0,0,255), 5 )
    #img = cv2.flip(img, 1) #矩陣左右翻轉
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img = cv2.resize(img,(int(img.shape[1]*1.4*Material.COMMOM_R),int(img.shape[0]*1.4*Material.COMMOM_R)))
    
    w = int(img.shape[1])
    h = int(img.shape[0])      
    white = 255 - np.zeros((h,w,4), dtype='uint8')

    #cv2.circle(img, (int(w*0.5), int(h*0.5)), int(240*Material.COMMOM_R), 255, 5)
    x1, y1, x2, y2 = [(int(w*0.5)+240*Material.COMMOM_R), (int(h*0.5)+240*Material.COMMOM_R), (int(w*0.5)-240*Material.COMMOM_R), (int(h*0.5)-240*Material.COMMOM_R) ]


    mode_next = RecongnitionNext.main(cam)
    if a == 0:
        output = img.copy()
    else:
        output = img.copy()  # 設定 output 和 photo 變數
        photo = img.copy()
        sec = sec - 0.05     # sec 不斷減少 0.05 ( 根據個人電腦效能設定，使其搭配 while 迴圈看起來像倒數一秒 )
        #putText(output, 10, 70, str(int(sec)))  # 加入文字
        # 如果秒數小於 1
        if sec < 1:
            output = cv2.addWeighted(white, a, photo, 1-a, 0)
            a = a - 0.1
            if a < 0:
                a = 0
                # 裁切圖片
                photo = photo[int(y2):int(y1), int(x2):int(x1)]

                cv2.imwrite( path_input + '/head_body/head.jpg', cv2.flip(photo, 1))
                break


    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    output = np.rot90(output)
    output = pygame.surfarray.make_surface(output)
    screen.blit(Material.background1_img, (0,0))
    cnt = ""
    if str(int(sec)) != "0" :
      for i in range(50) :
        cnt = cnt + str(int(sec))
      for i in range(15) :
        Material.draw_text( screen, cnt, int(100*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT*(i)/15, PURPLE )
    screen.blit(output, ( (Material.S_WIDTH-w)/2, Material.S_HEIGHT/3 ) )
    screen.blit(Material.takephoto, ((Material.S_WIDTH-Material.WIDTH)/2,0))
    Material.draw_text( screen, 'running loofah', int(130*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/10, WHITE )
    Material.draw_text( screen, 'align your head with the circle', int(60*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/5, WHITE )
    Material.draw_text( screen, 'please raise your hand', int(60*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/5+int(60*Material.COMMOM_R), WHITE )
    '''
    if str(int(sec)) != "0" :
      Material.draw_text( screen, str(int(sec)), int(200*Material.COMMOM_R), Material.S_WIDTH/2, Material.S_HEIGHT/1.2 )   
    '''

    pygame.display.update()
    
    timer.tick(fps)
    for event in pygame.event.get() :
      if event.type == pygame.QUIT :
        pygame.quit()
      #elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
      #  if a == 0 and sec == 0:
      #    a = 1
      #    sec = 4  # 加入倒數秒數

    key_pressed = pygame.key.get_pressed()
    if mode_next == 1 or key_pressed[pygame.K_DOWN]:
      if a == 0 and sec == 0:
        a = 1
        sec = 4  # 加入倒數秒數             

  pygame.mixer.music.fadeout(4)
  camera_mp3.play()
  #cam.release()
  pygame.display.update()
  
  # 裁切成圓型   
  head = imge_cut_Circle(path_input  + '/head_body/head.jpg')


  # run
  RunArr = []
  path_output_RUN = "./picture/player/RUN_"
  for i in range(16):
    RunArr.append('./img/player'+ str(i+1) + '.png' )
  minify = [0.75, 90, 40, 10] # 縮放 x軸 y軸 旋轉
  print(0.75*Material.COMMOM_R, Material.COMMOM_R)
  for i in range(16):
    if ( not CompositePicture(head,  RunArr[i], path_output_RUN, i+1, minify ) ) :
       return False



  #healthState_head 
  minify = [0.6, 25, 50, 10]
  img_HeathHead = "./img/healthstate_head.png"
  path_output_HeathHead = "./picture/player/HEALTHHEAD_"
  if ( not CompositePicture(head,  img_HeathHead, path_output_HeathHead, 1, minify ) ):
      return False
  

  # slip
  img_slip = "./img/player_slip.png" 
  img_slip_output = "./picture/player/player_slip_" 
  minify = [0.75, 80, 25, 90]
  if ( not CompositePicture(head,  img_slip, img_slip_output, 1, minify ) ) :
     return False



  return True 
  

if __name__ == "__main__":
   Photograph()