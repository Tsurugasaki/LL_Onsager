import numpy as np
import cv2

# 画像をグレースケールで読み込む
img = cv2.imread('output_image.tif', 0)

# CLAHEオブジェクトを作成（引数はオプション）
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
cl1 = clahe.apply(img)

# 画像を保存
cv2.imwrite('clahe_output_image.tif', cl1)

