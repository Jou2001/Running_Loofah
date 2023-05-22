import cv2
import numpy as np
from rembg import remove

cap = cv2.VideoCapture(0)

from PIL import Image


path_input = "./picture/head_body"
path_output = "./picture/player"
a = 0
n = 0

def CompositePicture(input_head, input_body):
  img_head = Image.open( input_head )
  img_body = Image.open( path_input + input_body )
  img_body = img_body.convert("RGBA") 
  
  widthB , heightB = img_body.size
  widthA , heightA = img_head.size
  new_img_head  = img_head.resize((int(widthA*0.75),int(heightA*0.75)), Image.LANCZOS)
  new_img_body  = img_body.resize(img_body.size,Image.LANCZOS)
  new_img_head = new_img_head.rotate(10)  
  
  resultPicture = Image.new('RGBA', img_body.size, (0, 0, 0, 0))   

  resultPicture.paste(new_img_head, (90,40), new_img_head)
  resultPicture.paste(new_img_body, (0,0), new_img_body )
  resultPicture.save( path_output + input_body )


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
  cv2.imwrite( path_input +'head.png', img_new)
  return path_input +'head.png' 


# 定義加入文字的函式
def putText(source, x, y, text, scale=2.5, color=(255,255,255)):
    org = (x,y)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = scale
    thickness = 5
    lineType = cv2.LINE_AA
    cv2.putText(source, text, org, fontFace, fontScale, color, thickness, lineType)

def main():
  global a, n 

  if not cap.isOpened():
      print("Cannot open camera")
      exit()
  while True:
      ret, img = cap.read()
      if not ret:
          print("Cannot receive frame")
          break
      x1, y1, x2, y2 = [int(img.shape[1]*0.5)+120, int(img.shape[0]*0.5)+120, int(img.shape[1]*0.5)-120, int(img.shape[0]*0.5)-120 ]
      # cv2.rectangle( img, (x1, y1), (x2, y2), (0,0,255), 5 )
      cv2.circle(img, (int(img.shape[1]//2), int(img.shape[0]//2)), 121, 255, 5)
      img = cv2.flip(img, 1) #矩陣左右翻轉
      img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
      w = int(img.shape[1])
      h = int(img.shape[0])    
      img = cv2.resize(img,(w,h))
  
      white = 255 - np.zeros((h,w,4), dtype='uint8')


      key = cv2.waitKey(1)
      if key == 32:
          a = 1
          sec = 4  # 加入倒數秒數
      elif key == ord('q'):
          break
      if a == 0:
          output = img.copy()
      else:
          output = img.copy()  # 設定 output 和 photo 變數
          photo = img.copy()
          sec = sec - 0.05     # sec 不斷減少 0.05 ( 根據個人電腦效能設定，使其搭配 while 迴圈看起來像倒數一秒 )
          putText(output, 10, 70, str(int(sec)))  # 加入文字
          # 如果秒數小於 1
          if sec < 1:
              output = cv2.addWeighted(white, a, photo, 1-a, 0)
              a = a - 0.1
              if a<0:
                  a = 0
                  n = n + 1
                  # 裁切圖片
                  photo = photo[y2+5:y1-5, x2+5:x1-5]

                  cv2.imwrite( path_input +'/head.jpg', photo)
                  break
              
      cv2.imshow('takePicture', output)


  cap.release()
  cv2.destroyWindow('takePicture')

  # 裁切成圓型
  head = imge_cut_Circle(path_input +'/head.jpg')

  RunArr = [ '/RUN_01.png', '/RUN_02.png', '/RUN_03.png', '/RUN_04.png']

  for i in range(len(RunArr)):
    print(path_output)
    print(RunArr[i])
    CompositePicture(head,  RunArr[i] )

  
  img = cv2.imread(path_output + RunArr[0])
  # 顯示圖片
  cv2.imshow('My Image', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


if __name__ == "__main__":
   main()