import numpy as np
from PIL import Image

def pre_process(img,img_bg=None,bg_color=(220,217,211)):
    # 正則化:RGBAモデル/RGBモデル
    img = img.convert("RGBA")
    if img_bg is not None:
        img_bg = img_bg.convert("RGB")
    # Numpy配列へ変換
    img_arr = np.array(img)
    if img_bg is not None:
        img_bg_arr = np.array(img_bg)
    # 配列のサイズを取得
    img_y = img_arr.shape[0]
    img_x = img_arr.shape[1]
    if img_bg is not None:
        img_bg_y = img_bg_arr.shape[0]
        img_bg_x = img_bg_arr.shape[1]
    else:
        img_bg_y = 0
        img_bg_x = 0

    # キャンバスを定義
    cam_y = 32*(1+(max(img_y,img_bg_y)-1)//32)
    cam_x = 32*(1+(max(img_x,img_bg_x)-1)//32)

    init_color = [bg_color[0],bg_color[1],bg_color[2]]
    cam_arr = np.full((cam_y,cam_x, 3), fill_value=init_color, dtype=np.uint8)

    # 後でログ記入に変えるprint
    print("\033[32m"+"App"+"\033[0m"+":"+"キャンバスは"+str(cam_arr.shape)+"の型になりました")

    # キャンバスへの貼り付けを行う(img_bf)
    if img_bg is not None:
        h, w = img_bg_arr.shape[:2]
        cam_arr[0:h, 0:w] = img_bg_arr

    # キャンバスへの貼り付けを行う(img)
    # 配列:img_arrのサイズを取得
    h, w = img_arr.shape[:2]

    # 前面（small）のカラー(RGB)とアルファ(A)を分離・正則化
    # アルファ値を 0.0 ~ 1.0 の浮動小数点数にする
    img_rgb = img_arr[:, :, :3].astype(np.float32)
    alpha = (img_arr[:, :, 3:].astype(np.float32)) / 255.0  # shape: (h, w, 1)

    # 背景（large）の該当するスライス部分を浮動小数点数に変換
    cam_rgb = cam_arr[0:h, 0:w].astype(np.float32)

    # アルファブレンドの計算 (ブロードキャスト)
    blended = cam_rgb + (img_rgb - cam_rgb) * alpha

    # 元の配列のメモリ実体に型を戻して書き戻す
    cam_arr[0:h, 0:w] = np.clip(blended, 0, 255).astype(np.uint8)
    
    # データ引き渡し用辞書
    _pre_process_ = {
        "img": img,
        "bg_img": img_bg,
        "cam_y": cam_y,
        "cam_x": cam_x,
        "cam_arr": cam_arr
    }
    return _pre_process_
