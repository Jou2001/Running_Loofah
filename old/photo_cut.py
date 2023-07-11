import cv2
import numpy as np
from rembg import remove

cap = cv2.VideoCapture(0)

from PIL import Image

def CompositePicture():
  imageA = Image.open('cut.png')
  imageB = Image.open('SS02.png')
  imageB = imageB.convert("RGBA") 
  
  widthB , heightB = imageB.size
  widthA , heightA = imageA.size
  newimageA  = imageA.resize((int(widthA*0.75),int(heightA*0.75)), Image.LANCZOS)
  newimageB  = imageB.resize(imageB.size,Image.LANCZOS)
  newimageA = newimageA.rotate(10)  
  
  resultPicture = Image.new('RGBA', imageB.size, (0, 0, 0, 0))   

  resultPicture.paste(newimageA,(210,30), newimageA)
  resultPicture.paste(newimageB, (0,0), newimageB )
  resultPicture.save("result.png")


# 去除背景
def DeleteBG( name ) :  
  #待处理的图片路径
  input_path = name

  #处理后存储的图片路径
  output_path = 'cut.png'

  with open(input_path, 'rb') as i:
      with open(output_path, 'wb') as o:
          input = i.read()
          output = remove(input)
          o.write(output)


# 定義加入文字的函式
def putText(source, x, y, text, scale=2.5, color=(255,255,255)):
    org = (x,y)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = scale
    thickness = 5
    lineType = cv2.LINE_AA
    cv2.putText(source, text, org, fontFace, fontScale, color, thickness, lineType)

a = 0
n = 0

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, img = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
    x1, y1, x2, y2 = [int(img.shape[1]*0.70), int(img.shape[0]*4/5), int(img.shape[1]*0.30), int(img.shape[0]*1/5) ]
    cv2.rectangle( img, (x1, y1), (x2, y2), (0,0,255), 5 )
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

                cv2.imwrite(f'photo-{n}.jpg', photo)
                DeleteBG( f'photo-{n}.jpg')
                break
            
    cv2.imshow('oxxostudio', output)

cap.release()
cv2.destroyWindow('oxxostudio')

RunArr = ['01_RUN.png','02_RUN.png','03_RUN.png', '04_RUN.png']
for i in range(len(RunArr)):
  CompositePicture(RunArr[0])

img = cv2.imread("result.png")
# 顯示圖片
cv2.imshow('My Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

