import cv2
import numpy as np

def find_colored_pixels(image, target_color):
    colored_pixels = []
    height, width, _ = image.shape

    for y in range(height):
        for x in range(width):
            pixel_color = image[y, x]
            if np.array_equal(pixel_color, target_color):
                colored_pixels.append((x, y))

    return colored_pixels

# 画像の読み込み
image = cv2.imread("輪郭のコピー.tif")

# 指定した色（BGR形式）
target_color = np.array([0, 0, 255])  # 例として赤色

# 指定した色と一致するピクセルの座標を取得
colored_pixel_coordinates = find_colored_pixels(image, target_color)

# 結果を表示
for coord in colored_pixel_coordinates:
    print(f"Colored pixel at: {coord}")
