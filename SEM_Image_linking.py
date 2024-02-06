import cv2
import numpy as np
from PIL import Image
import os

# 画像ファイルが存在するディレクトリのパス
image_directory = '/Users/soumakousuke/Desktop/大学/卒論/ssk/1'

# 画像ファイルの拡張子
image_extension = '.tif'

# 画像ファイルを格納するリスト
image_list = []

# ファイル名の範囲を指定
start_number = 2
end_number = 3

# ファイル名のパターンに基づいて画像をトリミングしてリスト化
for i in range(start_number, end_number + 1):
    filename = f"20231112_{i:03d}{image_extension}"
    filepath = os.path.join(image_directory, filename)
    if os.path.exists(filepath):
        image = Image.open(filepath)
        
        # 画像をトリミング (左上の座標と右下の座標を指定)
        left = 0  # トリミング範囲の左上 x 座標
        upper = 0  # トリミング範囲の左上 y 座標
        right = 1280  # トリミング範囲の右下 x 座標
        lower = 960  # トリミング範囲の右下 y 座標
        cropped_image = image.crop((left, upper, right, lower))
        
        # トリミングした画像をリストに追加
        image_list.append(cropped_image)

#OpenCvのStitcherオブジェクトを作成        
stitcher = cv2.Stitcher.create()

# 画像をOpenCV形式に変換してRGB形式に変換
opencv_images = [cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) for img in image_list]
# 画像を結合
status, result = stitcher.stitch(opencv_images)

# 結合に成功した場合
if status == cv2.Stitcher_OK:
    # 結合結果を保存
    cv2.imwrite('ssk_for_scale.tif', result)
else:
    print("結合に失敗しました。")