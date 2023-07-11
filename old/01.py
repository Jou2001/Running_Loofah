from rembg import remove

def Photo(name):
  #待处理的图片路径
  input_path = name
  print(type(input_path))
  #处理后存储的图片路径
  output_path = 'output.png'

  with open(input_path, 'rb') as i:
      with open(output_path, 'wb') as o:
          input = i.read()
          output = remove(input)
          o.write(output)

name = "AA.png"
Photo(name)


'''
import cv2

# 讀取圖檔
name = "windows-bg.jpg"
img = cv2.imread(name)
# 裁切圖片
img = cv2.resize(img,(640,480))
cv2.imwrite(name, img)
# 顯示圖片
cv2.imshow("cropped", img)
cv2.waitKey(0)
'''