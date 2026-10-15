import _data
from scipy.spatial import KDTree

def RGB_disatnce(cam_arr):
    # 最小ノルム探索
    tree = KDTree(_data.colors)
    _, min_indices = tree.query(cam_arr)
    cam_arr[...] = _data.colors[min_indices]
    
    # データ引き渡し用辞書
    _method_ = {
        "cam_arr":cam_arr
    }