import os

# リネームしたいディレクトリのパスを指定
directory_path = "/Users/soumakousuke/Desktop/大学/卒論/試料/20231006"

# リネームしたいファイルの拡張子を指定
file_extension = ".txt"

# ディレクトリ内の.tifファイルのみをリストアップ
file_list = [f for f in os.listdir(directory_path) if f.endswith(file_extension)]

# ファイルをリネームする
for old_name in file_list:
    # ファイル名を分割して、番号部分と拡張子を取得
    filename, ext = os.path.splitext(old_name)
    
    # ファイル名の番号部分をゼロ埋めの3桁に変換
    parts = filename.split('-')
    if len(parts) == 2:
        try:
            number = int(parts[1])
            new_number = f"{number:03d}"
            new_name = f"{parts[0]}-{new_number}{ext}"
            
            # 新しいファイルのフルパスを生成
            old_path = os.path.join(directory_path, old_name)
            new_path = os.path.join(directory_path, new_name)
            
            # ファイルをリネーム
            os.rename(old_path, new_path)
            print(f"リネーム: {old_name} -> {new_name}")
        except ValueError:
            print(f"エラー: {old_name} の番号部分が整数ではありません。")
    else:
        print(f"エラー: {old_name} のフォーマットが不正です。")