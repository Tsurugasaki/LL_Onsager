import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calculate_distance(x1, y1, x2, y2):
    # 2つの座標点間の距離を計算
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_colored_pixels(image, target_color):
    # 指定した色と一致するピクセルの座標を検出
    colored_pixels = np.column_stack(np.where(np.all(image == target_color, axis=-1)))
    return colored_pixels

def extract_pixels_within_distance(image, colored_pixels, max_distance):
    # 基準線からの距離が一定以下のピクセルを抽出
    extracted_pixels = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            distance = min(calculate_distance(x, y, ref_point[0], ref_point[1]) for ref_point in colored_pixel_coordinates) 
            if distance >= 0 and distance <= max_distance:
                extracted_pixels.append((x, y))
    return extracted_pixels

def create_mask(image_shape, extracted_pixels):
    # 画像サイズとピクセル座標からマスクを作成
    mask = np.zeros(image_shape[:2], dtype=np.uint8)  # マスクのデータ型を np.uint8 に変更
    for pixel in extracted_pixels:
        x, y = pixel
        mask[y, x] = 255  # ピクセルを白色に設定
    return mask

def save_image(output_path, image):
    # 画像を保存
    cv2.imwrite(output_path, image)
    print(f"新しい画像を {output_path} に保存しました。")

if __name__ == "__main__":
    # 画像を読み込む
    image_path = "/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/輪郭のコピー.tif"  # 画像のパスを指定
    image = cv2.imread(image_path)
    target_color = np.array([0, 0, 255])  # Jadeite輪郭の色

    # 指定した色と一致するピクセルの座標を取得
    colored_pixel_coordinates = find_colored_pixels(image, target_color)

    # 距離が一定以下のピクセルを抽出
    max_distance = 1800  # 距離の閾値を設定
    extracted_pixels = extract_pixels_within_distance(image, colored_pixel_coordinates, max_distance)

    # マスクを作成
    mask = create_mask(image.shape, extracted_pixels)

    # マスクを用いて抽出したピクセルの部分だけを抽出
    extracted_roi = cv2.bitwise_and(image, image, mask=mask)

    # 新しい画像を保存
    output_path = "/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/extracted_test2.tif"  # 保存先のパスを指定
    save_image(output_path, extracted_roi)

