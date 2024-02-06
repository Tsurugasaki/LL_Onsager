import cv2
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

def classify_and_visualize(image_path, output_excel_path="output.xlsx"):
    # 画像の読み込み
    image = cv2.imread(image_path)

    # 画像が読み込めなかった場合のエラーハンドリング
    if image is None:
        print(f"Error: Unable to read the image at {image_path}")
        return

    # BGRからRGBに変換
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 赤い領域の面積を計算（RGBの範囲を広げる）
    lower_red = np.array([100, 0, 0])
    upper_red = np.array([255, 0, 0])
    red_mask = cv2.inRange(image_rgb, lower_red, upper_red)
    red_area = np.sum(red_mask > 0)
    print(red_area)

    # 赤い領域を画像から取り除く
    image_rgb[red_mask > 0] = 0

    # RGBからLab色空間に変換
    lab_image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2Lab)

    # Lチャンネルを使用してクラスタリング
    l_channel = lab_image[:, :, 0].reshape((-1, 1))
    num_clusters = 2
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(l_channel)

    # 各ピクセルをクラスごとに色付け
    clustered_image = np.zeros_like(image)
    for i in range(num_clusters):
        mask = kmeans.labels_.reshape(image.shape[:2]) == i
        cluster_color = np.random.randint(0, 256, size=(1, 1, 3))
        clustered_image[mask] = cluster_color

    # クラスタリング結果の表示
    cv2.imshow("Clustered Image", clustered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 各クラスターの面積を計算
    areas = []
    for i in range(num_clusters):
        area = np.sum(kmeans.labels_ == i)
        areas.append(area)

    # 結果をDataFrameに追加
    df = pd.DataFrame({"Cluster": range(1, num_clusters + 1), "Area": areas})

    # 結果をExcelファイルに書き込み
    df.to_excel(output_excel_path, index=False)
    print(f"Cluster area information saved to {output_excel_path}")

# 画像のパスを指定して処理を行う
image_path = "/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/test.jpg"
classify_and_visualize(image_path, output_excel_path="/Users/soumakousuke/Desktop/大学/卒論/試料/結合画像/pixel_test.xlsx")
