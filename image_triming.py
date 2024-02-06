from PIL import Image

# 画像を読み込む
image = Image.open('20230905-001.tif')

# トリミング範囲を指定 (left, upper, right, lower)
# 例: 左上隅から幅100ピクセル、高さ150ピクセルをトリミング
left = 0
upper = 0
right = 1280
lower = 960

# 画像をトリミング
cropped_image = image.crop((left, upper, right, lower))

# トリミング後の画像を保存
cropped_image.save('cropped_image.tif')
