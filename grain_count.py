import cv2
import numpy as np

def remove_large_particles(contours, max_area):
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area <= max_area:
            filtered_contours.append(contour)
    return filtered_contours

# 画像を読み込む
image = cv2.imread("test.tiff")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 画像の二値化
_, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)
# 画像を表示
cv2.imshow("binary_image", binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 輪郭を抽出
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# ある面積以上の粒子を除外
max_particle_area = 5000  # 例: 5000ピクセル
filtered_contours = remove_large_particles(contours, max_particle_area)

# 輪郭ごとに重心位置を計算して表示
for contour in filtered_contours:
    # 輪郭のモーメントを計算
    M = cv2.moments(contour)

    # 重心位置を計算
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        print(f"Centroid of contour: ({cx}, {cy})")

# カウントした粒子の位置を元画像に描画
image_with_counted_particles = image.copy()
for contour in filtered_contours:
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.circle(image_with_counted_particles, (cx, cy), 10, (0, 0, 255), -1)

# 画像を表示
cv2.imshow("Counted Particles", image_with_counted_particles)
cv2.waitKey(0)
cv2.destroyAllWindows()

# カウントした粒子の面積を計測して表示
for i, contour in enumerate(filtered_contours):
    area = cv2.contourArea(contour)
    print(f"Particle {i+1}: Area = {area}")
