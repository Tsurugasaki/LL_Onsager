import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def find_colored_pixels(image, target_color):
    # 指定した色と一致するピクセルの座標を検出
    colored_pixels = np.column_stack(np.where(np.all(image == target_color, axis=-1)))
    return colored_pixels

def calculate_distance(x1, y1, x2, y2):
    # 2つの座標点間の距離を計算
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def calculate_particle_size(contours):
    # 各輪郭の面積を計算
    particle_sizes = [cv2.contourArea(contour) for contour in contours]
    return particle_sizes

def visualize_particles(image, contours):
    # 粒子にカウントされた部分を緑色で表示
    image_with_particles = image.copy()
    cv2.drawContours(image_with_particles, contours, -1, (0, 255, 0), thickness=2)
    return image_with_particles

def remove_large_particles(contours_orig, max_area, min_area):
    # ある面積以上の粒子を取り除く
    filtered_contours = [contour for contour in contours_orig if min_area <= cv2.contourArea(contour) <= max_area]
    return filtered_contours

def analyze_particle_size_distribution(image_path, particle_threshold, target_color, max_area):
    # 画像を読み込む
    image = cv2.imread(image_path)

    # 指定した色と一致するピクセルの座標を取得
    colored_pixel_coordinates = find_colored_pixels(image, target_color)

    # 画像をグレースケールに変換し、粒子として認識するための二値画像を作成
    gray_orig = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_orig = cv2.threshold(gray_orig, particle_threshold, 255, cv2.THRESH_BINARY)

    # 輪郭を検出
    contours_orig, _ = cv2.findContours(binary_orig, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 除外する大きな粒子を取り除く
    contours_filtered = remove_large_particles(contours_orig, max_area, min_area)

    # 粒子の特性データを保存するリスト
    particle_data = []

    # 各粒子の中心座標、面積、基準点からの最小距離を計算
    for contour in contours_filtered:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            area = cv2.contourArea(contour)
            distances_from_ref = [calculate_distance(cx, cy, ref_point[0], ref_point[1]) for ref_point in colored_pixel_coordinates]
            min_distance = min(distances_from_ref)
            particle_data.append((cx, cy, area, min_distance))

    # 特性データをDataFrameに変換
    df = pd.DataFrame(particle_data, columns=["Centroid_X", "Centroid_Y", "Particle_Area", "Distance_From_Ref"])

    # DataFrameをExcelファイルに保存
    df.to_excel("/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/赤輪郭_result.xlsx", index=False)

    # 粒子がカウントされた画像を可視化
    plt.subplot(122)
    image_without_scale_bar_visualized = visualize_particles(image, contours_filtered)
    plt.imshow(image_without_scale_bar_visualized, cmap="gray")
    plt.title("Original Image with Particle Count")
    plt.show()

if __name__ == "__main__":
    target_color = np.array([0, 0, 255])  # Jadeite輪郭の色
    image_path = "/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/輪郭.tif"  # 解析したい画像のパスを指定
    particle_threshold = 50  # 粒子として認識する明るさの閾値を指定（0から255の範囲で値を調整してください）
    max_area = 150000  # カウントする粒子の最大面積
    min_area = 50 #カウントする粒子の最小面積

    # 粒度分布の解析を行う
    analyze_particle_size_distribution(image_path, particle_threshold, target_color, max_area)
