# region:import(standard)
import os
import sys
from pathlib import Path
from collections import defaultdict # デフォ値の辞書を作るためのライブラリ
# endregion:import(standard)

# region:import(library)
from PIL import Image
# endregion:import(library)

# region:import(_file)
import _data
import _pre_process
import _method
import _output
# endregion:import(_file)

# setting
img_name = "HBK128" # 変換したい画像の名前を指定してください(拡張子は不要)
img_bg_name = "背景画像" # 不透明度は参照されません
fill_color = "21" # _data.gidで指定してください(21がデフォルトで骨粉になります)
converted_excel_name = "AMC-"+img_name

def get_download_path():
    
    # ユーザーのホームディレクトリ（C:\Users\ユーザー名）を取得
    home_dir = os.path.expanduser("~")

    # ダウンロードフォルダのパスを作成
    download_dir = os.path.join(home_dir, "Downloads")

    return download_dir

download_path = get_download_path()


# スクリプトカラー(GUIを作ったらスクリプトは見ないので不要になる)
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
END = "\033[0m"
App = GREEN+"App"+END+":"
Error = RED+"Error"+END+":"

# 旧系式のエラーハンドリング
error_state = False

# 同ディレクトリ内のPNGファイルパス
img_bg_path = Path(img_bg_name+".png")
img_path = Path(img_name+".png")

# ファイルが存在するかどうかを判定
if img_bg_path.exists():
    img_bg = Image.open(img_bg_name+".png")
    bg_state = True
    print(App+f"背景画像{YELLOW+img_bg_name+END}が選択されました")
else:
    print(App+"背景画像は選択されていません")
    img_bg = None
    bg_state = False

if img_path.exists():
    img = Image.open(img_name+".png")
    print(App+f"変換したい画像{YELLOW+img_name+".png"+END}が正常に読み込まれました")
else:
    print(Error+"変換したいファイルをが見つかりません")
    error_state = True

if fill_color in _data.gid:
    bg_color = _data.gid[fill_color]
    print(f"{App}背景色を{fill_color}(#{hex(_data.gid[fill_color][0])[2:]}{hex(_data.gid[fill_color][1])[2:]}{hex(_data.gid[fill_color][2])[2:]})に指定しました")
else:
    print(Error+"背景色が定義されていないか、見つかりません")
    error_state = True

# 定義ミスの場合に強制終了    
if error_state:sys.exit()

# 前処理を行う
_pre_process_ = _pre_process.pre_process(img,img_bg,bg_color)
img = _pre_process_["img"]
bg_img = _pre_process_["bg_img"]
cam_y = _pre_process_["cam_y"]
cam_x = _pre_process_["cam_x"]
cam_arr= _pre_process_["cam_arr"]

# デバッグ:変換前pngのテスト出力
# img = Image.fromarray(cam_arr, 'RGB')
# img.save("変換前.png")

_method.RGB_disatnce(cam_arr)

# デバッグ:変換後pngのテスト出力
# img = Image.fromarray(cam_arr, 'RGB')
# img.save("変換後.png")

_output.excel(cam_arr, cam_x, cam_y, download_path, converted_excel_name)



