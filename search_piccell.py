from PIL import Image

# 画像を読み込む
image = Image.open('20230905-001.tif')

# 画像の幅と高さ（ピクセル数）を取得
width, height = image.size

# 幅と高さを表示
print("画像の幅（ピクセル数）:", width)
print("画像の高さ（ピクセル数）:", height)
