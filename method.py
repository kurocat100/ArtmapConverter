import data
import numpy as np
from scipy.spatial import KDTree
from skimage import color as skimage_color # colorとか絶対使われてる変数

def RGB_disatnce(cam_arr):
    # 最小ノルム探索
    tree = KDTree(data.colors)
    _, min_indices = tree.query(cam_arr)
    cam_arr[...] = data.colors[min_indices]
    
    # データ引き渡し用辞書
    _method = {
        "cam_arr":cam_arr
    }


def Lab_distance(cam_arr):
    height, width, _ = cam_arr.shape
    
    rgb_float = cam_arr.astype(np.float32) / 255.0
    lab_array = skimage_color.rgb2lab(rgb_float)
    
    colors_float = data.colors.astype(np.float32) / 255.0
    colors_lab = skimage_color.rgb2lab(colors_float)
    
    tree = KDTree(colors_lab)
    lab_flat = lab_array.reshape(-1, 3)
    _, min_indices = tree.query(lab_flat)
    
    matched_lab_flat = colors_lab[min_indices]
    matched_lab_array = matched_lab_flat.reshape(height, width, 3)
    result_rgb_float = skimage_color.lab2rgb(matched_lab_array)
    cam_arr = np.clip(result_rgb_float * 255.0, 0, 255).astype(np.uint8)
    
    # 微妙にずれてるので型にはめなおすため
    tree = KDTree(data.colors)
    _, min_indices = tree.query(cam_arr)
    cam_arr[...] = data.colors[min_indices]
    
    # データ引き渡し用辞書
    _method = {
        "cam_arr":cam_arr
    }