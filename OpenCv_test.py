import cv2
import numpy as np
import matplotlib.pyplot as plt

# カラーで読み込んだ画像をcvtColorを用いてhsvに変更 
file_path = "tapioka_drink.jpg"
img_cl = cv2.imread(file_path, 6)
img_hsv = cv2.cvtColor(img_cl, cv2.COLOR_BGR2HSV)  

## 赤色の範囲を定義 ##
hsv_min = np.array([150, 64, 0])
hsv_max = np.array([180, 255, 255])
 
## 赤色をマスクする ##   
mask = cv2.inRange(img_hsv, hsv_min, hsv_max)
mask = cv2.bitwise_not(mask)
img_hsv = cv2.bitwise_and(img_hsv, img_hsv, mask = mask)
 
## 背景の黒い部分などを白くする ##
img_hsv[:, :, 2] = np.where(img_hsv[:, :, 2] < 10, 255 * np.ones_like(img_hsv[:, :, 2]), img_hsv[:, :, 2])
 
## HSVからBGRを経由して白黒に変更する ##
img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
img_bw  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
 
## ごみを取るためのブラシ処理 ##
img_bw_b = cv2.blur(img_bw, (3, 3))

## 暗い部分のみ残してみる ##
img_bw_b = np.where(img_bw_b < 90, 255, 0)
 
## 画像を表示 ##
plt.imshow(img_bw_b)
plt.show()