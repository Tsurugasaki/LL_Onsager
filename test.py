import cv2
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import os

def save_results_to_excel(output_excel_path, red_area_pixels, non_red_area_pixels, areas):
    # DataFrameを作成
    df = pd.DataFrame({
        "領域": ["赤色領域", "赤色以外の領域"] + [f"クラスター{i + 1}" for i in range(len(areas))],
        "面積": [red_area_pixels, non_red_area_pixels] + areas
    })

    # Excelファイルに書き込み
    df.to_excel(output_excel_path, index=False)
    print(f"結果を {output_excel_path} に保存しました。")

def save_images(output_folder, image, red_mask, lab_image, clustered_image, result_image):
    os.makedirs(output_folder, exist_ok=True)

    cv2.imwrite(os.path.join(output_folder, "original_image.jpg"), image)
    cv2.imwrite(os.path.join(output_folder, "red_area_mask.jpg"), red_mask.astype(np.uint8) * 255)
    cv2.imwrite(os.path.join(output_folder, "lab_image.jpg"), lab_image)
    cv2.imwrite(os.path.join(output_folder, "clustered_image.jpg"), clustered_image)
    cv2.imwrite(os.path.join(output_folder, "result_image.jpg"), result_image)

def classify_and_visualize(image_path, output_excel_path="output.xlsx", output_folder="output_images"):
    # 画像の読み込み
    image = cv2.imread(image_path)

    # 画像が読み込めなかった場合のエラーハンドリング
    if image is None:
        print(f"Error: Unable to read the image at {image_path}")
        return

    # 赤い領域の面積を計算
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([50, 50, 255])
    red_mask = cv2.inRange(image, lower_red, upper_red)
    red_area_pixels = np.count_nonzero(red_mask)

    # 赤色以外の領域の面積を計算
    non_red_area_pixels = np.count_nonzero(~red_mask)

    # 赤色領域を黒で塗りつぶす
    result_image = cv2.bitwise_and(image, image, mask=~red_mask)
    result_image[red_mask] = 0

    # RGBからLab色空間に変換
    lab_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2Lab)

    # Lチャンネルを使用してクラスタリング
    l_channel = lab_image[:, :, 0].reshape((-1, 1))
    num_clusters = 4
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(l_channel)

   # クラスターごとに指定した色（RGB形式）を設定
    cluster_colors_rgb = [
        (255, 0, 0),  # 赤
        (0, 255, 0),  # 緑
        (0, 0, 255),  # 青
        (255, 255, 0),  # 黄
        (255, 255, 255)  # 白
    ]

    # 各ピクセルをクラスごとに色付け
    clustered_image = np.zeros_like(image)
    for i in range(num_clusters):
        mask = kmeans.labels_.reshape(image.shape[:2]) == i
        cluster_color_lab = cluster_colors_rgb[i]
        clustered_image[mask] = cluster_color_lab

    # 各クラスターの面積を計算
    areas = [np.sum(kmeans.labels_ == i) for i in range(num_clusters)]

    # 結果をExcelファイルに保存
    save_results_to_excel(output_excel_path, red_area_pixels, non_red_area_pixels, areas)

    # 生成した画像を保存
    save_images(output_folder, image, red_mask, lab_image, clustered_image, result_image)

    # 元画像、赤色領域、Lab画像、クラスターごとの着色画像、赤色を除く画像を表示
    cv2.imshow('Original Image', image)
    cv2.imshow('Red Area', red_mask)
    cv2.imshow('Lab Image', lab_image)
    cv2.imshow('Clustered Image', cv2.cvtColor(clustered_image, cv2.COLOR_Lab2BGR))
    cv2.imshow('Result Image', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 画像のパスを指定して処理を行う
image_path = "/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/corna1_jadeite_painted.tif"
classify_and_visualize(image_path, output_excel_path="/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/Jade_painted1_result_corona1.xlsx", output_folder="/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/output_images_corona1")
