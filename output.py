import os
from pathlib import Path

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter # ← 列番号を文字に変換するツール
from openpyxl.worksheet.errors import IgnoredError

import data

def excel(cam_arr, cam_x, cam_y, download_path, converted_excel_name):
    wb = Workbook()
    ws = wb.active
    ws.title = "PixelArt"

    # Excelのセルサイズ (高さ 33.4, 幅 5.83 の正方形)
    ROW_HEIGHT = 32.4
    COL_WIDTH = 5.83

    # 全列の幅を固定
    for col_idx in range(1, cam_x + 1):
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = COL_WIDTH

    # 全行の高さを固定 (データをいじる前にあらかじめ枠を作っておく)
    for row_idx in range(1, cam_x + 1):
        ws.row_dimensions[row_idx].height = ROW_HEIGHT


    # スタイルオブジェクトの事前生成 (使い回し用)
    cell_font_black = Font(name="游ゴシック", size=20, color="000000")
    cell_font_white = Font(name="游ゴシック", size=20, color="afafaf")
    cell_alignment = Alignment(horizontal="center", vertical="center")

    color_palette = {}
    for rgb_tuple, text_key in data.colors2gid.items():
        hex_color = f"{rgb_tuple[0]:02X}{rgb_tuple[1]:02X}{rgb_tuple[2]:02X}"
        color_palette[text_key] = PatternFill(patternType="solid", fgColor=hex_color)


    # 確定した枠（セル）に対して、NumPyデータを直接流し込む
    # ws.append ではなく、既存のセル(row, col)にアクセスして値を上書きします
    for y in range(cam_y):
        for x in range(cam_x):
            # 1始まりのExcel座標に変換
            row_idx = y + 1
            col_idx = x + 1

            cell = ws.cell(row=row_idx, column=col_idx)

            # NumPy配列からRGBを取得して2文字に変換
            rgb_tuple = tuple(cam_arr[y, x])
            text_value = data.colors2gid.get(rgb_tuple, "")

            # セルへの書き込みとスタイル設定
            cell.value = text_value
            if rgb_tuple[0] > 40 and rgb_tuple[1] > 40 and rgb_tuple[2] > 40:
                cell.font = cell_font_black
            else:cell.font = cell_font_white
            cell.alignment = cell_alignment
            cell.data_type = 's'  # 文字列として扱う

            if text_value in color_palette:
                cell.fill = color_palette[text_value]


    # Excelファイルの保存
    save_path = os.path.join(download_path,converted_excel_name+".xlsx")
    wb.save(save_path) 
    print(f"{"\033[32m"+"App"+"\033[0m"+":"}変換後のファイルを{"\033[33m"+converted_excel_name+".xlsx"+"\033[0m"}として保存しました")