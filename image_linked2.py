import re
import os
from PIL import Image

# テキストファイルが存在するディレクトリのパス
text_directory = '/Users/soumakousuke/Desktop/大学/卒論/試料/20231006'

# テキストファイルの拡張子
text_extension = '.txt'

# 画像ファイルが存在するディレクトリのパス
image_directory = '/Users/soumakousuke/Desktop/大学/卒論/試料/20231006'

# 画像ファイルの拡張子
image_extension = '.tif'

# 座標情報を格納するリスト
datalist = []

# ファイル名の範囲を指定
start_number = 1
end_number = 100

# 倍率を入力
scale = 150

# 1枚目の座標を取得
### 日付部分を入力 ###
textfilename_1 = f"20231006-{start_number:03d}{text_extension}"
textfilepath_1 = os.path.join(text_directory, textfilename_1)

with open(textfilepath_1, 'r') as file_1:
    content_1 = file_1.read()

    pattern_1 = r'\$CM_STAGE_POS\s+([0-9.-]+)\s+([0-9.-]+)'  # 座標情報の正規表現パターン
    match_1 = re.search(pattern_1, content_1)

    x_1 = float(match_1.group(1))
    y_1 = float(match_1.group(2))

# テキストファイルを開いて座標情報の取得
### 日付部分を入力 ###
for i in range(start_number, end_number + 1):
    textfilename = f"20231006-{i:03d}{text_extension}"
    textfilepath = os.path.join(text_directory, textfilename)
    
    # テキストファイルを開いて中身を読み込む
    with open(textfilepath, 'r') as file:
        content = file.read()

        # 正規表現を使用して座標情報を抽出
        pattern = r'\$CM_STAGE_POS\s+([0-9.-]+)\s+([0-9.-]+)'  # 座標情報の正規表現パターン
        matches = re.findall(pattern, content)

        # 座標情報を取得し、補正を行う ×150が基準なので、倍率に合わせて()内を適宜調整してください。
        for match in matches:
            x, y = map(float, match)
            x = (x - x_1) * -1580 * (scale/150)
            y = (y - y_1) * 1580 * (scale/150)
    
    # 画像ファイルのパスを生成
    ### 日付部分を入力 ###
    imagefilename = f"20231006-{i:03d}{image_extension}"
    imagefilepath = os.path.join(image_directory, imagefilename)

    # 画像ファイルの読み込み
    img = Image.open(imagefilepath)
    # 画像をトリミング (左上の座標と右下の座標を指定)
    left = 0  # トリミング範囲の左上 x 座標
    upper = 0  # トリミング範囲の左上 y 座標
    right = 1280  # トリミング範囲の右下 x 座標
    lower = 960  # トリミング範囲の右下 y 座標
    cropped_image = img.crop((left, upper, right, lower))

    # 座標情報をリスト化
    datalist.append((x, y, cropped_image))

# 画像の結合を行う
output_image = None

# 出力画像のサイズを計算
min_x = min([x for x, _, _ in datalist])
max_x = max([x for x, _, _ in datalist])
min_y = min([y for _, y, _ in datalist])
max_y = max([y for _, y, _ in datalist])
output_width = int(max_x - min_x + cropped_image.width)
output_height = int(max_y - min_y + cropped_image.height)

for x, y, img in datalist:
    if output_image is None:
        # 出力画像の初期化
        output_image = Image.new('RGB', (output_width, output_height))
    
    # 座標を補正して画像を中心座標に配置
    left = int(x - min_x + img.width / 2)
    top = int(y - min_y + img.height / 2)
    output_image.paste(img, (left, top))

# 結合された画像を保存
### 画像名を入力 ###
output_image.save('output_image1.tif')