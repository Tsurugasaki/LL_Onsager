import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_particle_size(contours):
    # 粒度計算
    particle_sizes = [cv2.contourArea(contour) for contour in contours]
    return particle_sizes

def remove_scale_bar(image, scale_bar_threshold, scale_bar_area_threshold):
    # グレースケールに変換
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 明るさがスケールバーの閾値以上の領域を特定
    _, binary_image = cv2.threshold(gray_image, scale_bar_threshold, 255, cv2.THRESH_BINARY)

    # 輪郭を抽出
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # スケールバーの輪郭を削除
    for contour in contours:
        area = cv2.contourArea(contour)
        if area <= scale_bar_area_threshold:
            cv2.drawContours(binary_image, [contour], -1, 0, thickness=cv2.FILLED)

    # スケールバーを除外した画像を作成
    image_without_scale_bar = cv2.bitwise_and(image, image, mask=~binary_image)

    return image_without_scale_bar

def remove_noise(image, noise_threshold):
    # ノイズ除去
    kernel = np.ones((3, 3), np.uint8)
    cleaned_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=noise_threshold)

    return cleaned_image

def visualize_particles(image, contours):
    # 粒子にカウントされた部分を赤色で表示
    image_with_particles = image.copy()
    cv2.drawContours(image_with_particles, contours, -1, (255, 0, 0), thickness=2)

    return image_with_particles

def fourier_transform(image):
    # グレースケールに変換
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # フーリエ変換を行う
    fft_image = np.fft.fft2(gray_image)
    fft_shifted_image = np.fft.fftshift(fft_image)
    magnitude_spectrum = np.abs(fft_shifted_image)

    # 逆フーリエ変換を行う
    ifft_shifted_image = np.fft.ifftshift(fft_shifted_image)
    ifft_image = np.fft.ifft2(ifft_shifted_image)
    ifft_image = np.abs(ifft_image)

    return magnitude_spectrum, ifft_image

def analyze_particle_size_distribution(image_path, particle_threshold, scale_bar_threshold, scale_bar_area_threshold, noise_threshold):
    # 画像を読み込む
    image = cv2.imread(image_path)

    # スケールバーを除外
    image_without_scale_bar = remove_scale_bar(image, scale_bar_threshold, scale_bar_area_threshold)

    # ノイズ除去
    cleaned_image = remove_noise(image_without_scale_bar, noise_threshold)

    # グレースケールに変換
    gray_image = cv2.cvtColor(cleaned_image, cv2.COLOR_BGR2GRAY)

    # 明るさが粒子の閾値以上の領域を特定
    _, binary_image = cv2.threshold(gray_image, particle_threshold, 255, cv2.THRESH_BINARY)

    # 画像処理後の輪郭を抽出
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # グレースケールに変換
    gray_image_orig = cv2.cvtColor(image_without_scale_bar, cv2.COLOR_BGR2GRAY)

    # 明るさが粒子の閾値以上の領域を特定
    _, binary_image_orig = cv2.threshold(gray_image_orig, particle_threshold, 255, cv2.THRESH_BINARY)

    # 画像処理前の輪郭を抽出
    contours_orig, _ = cv2.findContours(binary_image_orig, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 粒子の面積を計算
    particle_sizes = calculate_particle_size(contours)

    # 外れ値を除外
    mean_size = np.mean(particle_sizes)
    std_size = np.std(particle_sizes)
    filtered_particle_sizes = [size for size in particle_sizes if (mean_size - 2 * std_size) < size < (mean_size + 2 * std_size)]

    # 元画像に対する粒度解析を行い、粒度分布を取得
    gray_orig = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_orig = cv2.threshold(gray_orig, particle_threshold, 255, cv2.THRESH_BINARY)
    contours_orig, _ = cv2.findContours(binary_orig, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    particle_sizes_orig = calculate_particle_size(contours_orig)
    mean_size_orig = np.mean(particle_sizes_orig)
    std_size_orig = np.std(particle_sizes_orig)
    filtered_particle_sizes_orig = [size for size in particle_sizes_orig if (mean_size_orig - 2 * std_size_orig) < size < (mean_size_orig + 2 * std_size_orig)]

    

    # 通常軸での粒度分布をプロット
    plt.figure(figsize=(10, 5))
    plt.subplot(241)
    plt.hist(filtered_particle_sizes, bins=20, range=(0, max(filtered_particle_sizes)))
    plt.xlabel("Particle Size")
    plt.ylabel("Frequency")
    plt.title("Particle Size Distribution (Linear Scale)")

    # 対数軸での粒度分布をプロット
    plt.subplot(242)
    plt.hist(filtered_particle_sizes, bins=np.logspace(np.log10(0.1), np.log10(max(filtered_particle_sizes)), 20))
    plt.xscale("log")
    plt.xlabel("Particle Size")
    plt.ylabel("Frequency")
    plt.title("Particle Size Distribution (Log Scale)")

    # 元画像に対する粒度分布を通常軸でプロット
    plt.subplot(243)
    plt.hist(filtered_particle_sizes_orig, bins=20, range=(0, max(filtered_particle_sizes)))
    plt.xlabel("Particle Size (Log Scale)")
    plt.ylabel("Frequency")
    plt.title("Particle Size Distribution (Linear Scale)")

    # 元画像に対する粒度分布を通常軸でプロット
    plt.subplot(244)
    plt.hist(filtered_particle_sizes_orig, bins=np.logspace(np.log10(0.1), np.log10(max(filtered_particle_sizes)), 20))
    plt.xscale("log")
    plt.xlabel("Particle Size")
    plt.ylabel("Frequency")
    plt.title("Particle Size Distribution (Linear Scale)")

    plt.tight_layout()
    plt.show()

    # 元画像のフーリエ変換と逆フーリエ変換
    magnitude_spectrum_orig, ifft_image_orig = fourier_transform(image_without_scale_bar)
    # 画像処理後のフーリエ変換と逆フーリエ変換
    magnitude_spectrum_proc, ifft_image_proc = fourier_transform(cleaned_image)

    # フーリエ変換後と逆フーリエ変換後の結果を可視化
    plt.figure(figsize=(15, 6))
    plt.subplot(241)
    plt.imshow(np.log(1 + magnitude_spectrum_orig), cmap="gray")
    plt.title("Original Fourier Transform (Log Scale)")
    plt.subplot(242)
    plt.imshow(np.log(1 + magnitude_spectrum_proc), cmap="gray")
    plt.title("Processed Fourier Transform (Log Scale)")
    plt.subplot(243)
    plt.imshow(image, cmap="gray")
    plt.title("Original Image")
    plt.subplot(244)
    plt.imshow(ifft_image_proc, cmap="gray")
    plt.title("Processed Inverse Fourier Transform")
    plt.subplot(245)
    plt.imshow(np.log(1 + magnitude_spectrum_orig), cmap="gray")
    plt.title("Original Fourier Transform (Log Scale)")
    plt.subplot(246)
    plt.imshow(np.log(1 + magnitude_spectrum_proc), cmap="gray")
    plt.title("Processed Fourier Transform (Log Scale)")
    plt.subplot(247)
    plt.imshow(ifft_image_orig, cmap="gray")
    plt.title("Original Inverse Fourier Transform")
    plt.subplot(248)
    plt.imshow(cleaned_image, cmap="gray")
    plt.title("Processed Image")
    plt.tight_layout()
    plt.show()

    # 画像処理後の粒子にカウントされた部分を画像に表示
    plt.subplot(121)
    image_with_particles = visualize_particles(binary_image, contours)
    plt.imshow(image_with_particles, cmap="gray")
    plt.title("Filtered Image with Particle Count")

    # 元画像に対する粒度解析を可視化
    plt.subplot(122)
    image_without_scale_bar_visualized = visualize_particles(image_without_scale_bar, contours_orig)
    plt.imshow(image_without_scale_bar_visualized, cmap="gray")
    plt.title("Original Image with Particle Count")
    plt.show()

if __name__ == "__main__":
    image_path = "Si.png"  # 解析したい画像のパスを指定
    particle_threshold = 210  # 粒子として認識する明るさの閾値を指定（0から255の範囲で値を調整してください）
    scale_bar_threshold = 255  # スケールバーを除外するための明るさの閾値を指定（0から255の範囲で値を調整してください）
    scale_bar_area_threshold = 1  # スケールバーと判定する輪郭の面積の閾値（適宜調整してください）
    noise_threshold = 1  # ノイズ除去のための繰り返し回数を指定（ノイズが残る場合は値を増やしてください）

    # 粒度分布とフーリエ変換の解析を行う
    analyze_particle_size_distribution(image_path, particle_threshold, scale_bar_threshold, scale_bar_area_threshold, noise_threshold)
