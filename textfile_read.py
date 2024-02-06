import re
import os

# テキストファイルが存在するディレクトリのパス
text_directory = '/Users/soumakousuke/vscode_anaconda3'

# テキストファイルの拡張子
text_extension = '.txt'

# 画像ファイルが存在するディレクトリのパス
image_directory = '/Users/soumakousuke/vscode_anaconda3'

# 画像ファイルの拡張子
image_extension = '.tif'

# 座標情報を格納するリスト
coordinates_list = []

# ファイル名の範囲を指定
start_number = 1
end_number = 179

#テキストファイルを開いて座標情報の取得
for i in range(start_number, end_number + 1):
    textfilename = f"20230905-{i:03d}{text_extension}"
    textfilepath = os.path.join(text_directory, textfilename)
    # テキストファイルを開いて中身を読み込む
    with open(textfilepath, 'r') as file:
        content = file.read()

    # 正規表現を使用して座標情報を抽出
    pattern = r'\$CM_STAGE_POS\s+([0-9.-]+)\s+([0-9.-]+)'  # 座標情報の正規表現パターン
    matches = re.findall(pattern, content)

    # 座標情報を取得しリストに格納
    for match in matches:
        x, y = map(float, match)

    #画像ファイルのパス
    imagefilename = f"20230905-{i:03d}{image_extension}"
    imagefilepath = os.path.join(image_directory, imagefilename)

    # 中心座標と画像ファイルのパスを関連付けてリストに追加
    coordinates_list.append((x, y, imagefilepath))
 
# 座標情報を表示
for x, y, imagefilepath in coordinates_list:
    print(f'座標: ({x}, {y}), 画像ファイル: {imagefilepath}')
