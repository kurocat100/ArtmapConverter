# region:impots
# library(standard)
import os
import sys
from pathlib import Path

# library(third party)
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
import ctypes
from PIL import Image
from scipy.spatial import KDTree

# library(file)
import data
import pre_process
import method
import output
# endregion:imports

#region:global
VERSION = "Ver. 0.4"
FONT_TYPE = "meiryo"
colors_tree = KDTree(data.colors) # GUI上の処理で毎回生成すると重くなる気がしたので

# pyinstallerの時にアイコンのパスがバグるので...以下
def get_resource_path(relative_path):
    """PyInstallerの一時フォルダに対応したパスを返す関数"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

chibiki_icon_path = get_resource_path("chibiki.ico")

def get_download_path():
    # ユーザーのホームディレクトリ（C:\Users\ユーザー名）を取得
    home_dir = os.path.expanduser("~")
    # ダウンロードフォルダのパスを作成
    download_dir = os.path.join(home_dir, "Downloads")
    return download_dir
download_path = get_download_path()
#endregion:global



class ArtmapConverter(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("Artmap Converter🖌"+VERSION)
        self.iconbitmap(chibiki_icon_path)
        self.geometry("750x500")
        
        self.grid_columnconfigure(1, weight=1)  
        self.grid_columnconfigure(1, weight=1)  
        
        # region:widget
        self.fill_color_discription = ctk.CTkLabel(master=self, text="最背景色")
        self.fill_color_discription.grid(row=0, column=0, padx=20, pady=10)

        
        self.fill_color_entry_var = ctk.StringVar()
        self.fill_color_entry_var.trace_add("write", self.change_fill_color)
        self.fill_color_entry = ctk.CTkEntry(master=self, placeholder_text="gIDまたは#HEXで指定, 初期値:21(骨粉デフォルト)",textvariable=self.fill_color_entry_var)
        self.fill_color_entry.insert(0, "21")
        self.fill_color_entry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        
        self.method_var = ctk.StringVar(value="RGB_distance")
        self.method1 = ctk.CTkRadioButton(master=self, text="RGB近似", variable=self.method_var, value="RGB_distance")
        self.method1.grid(row=1, column=0, padx=10, pady=10)
        self.method2 = ctk.CTkRadioButton(master=self, text="L*a*b*近似", variable=self.method_var, value="Lab_distance")
        self.method2.grid(row=2, column=0, padx=10, pady=10)
        
        self.img_bg_path_button = ctk.CTkButton(master=self, text="背景png画像(*任意)", command=self.select_img_bg_path)
        self.img_bg_path_button.grid(row=3, column=0, padx=10, pady=10)
        
        self.img_bg_path_entry = ctk.CTkEntry(master=self, placeholder_text="背景画像の絶対パス")
        self.img_bg_path_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        self.img_path_button =ctk.CTkButton(master=self, text="変換するpng画像", command=self.select_img_path)
        self.img_path_button.grid(row=4, column=0, padx=10, pady=10)
        
        self.img_path_entry = ctk.CTkEntry(master=self, placeholder_text="変換する画像の絶対パス")
        self.img_path_entry.grid(row=4, column=1, padx=20, pady=10, sticky="ew")        
        
        self.output_option_ver = ctk.StringVar(value="excel")
        self.output_option1 = ctk.CTkRadioButton(master=self, text="Excel", variable=self.output_option_ver, value="excel")
        self.output_option1.grid(row=5, column=0, padx=10, pady=10)
        self.output_option2 = ctk.CTkRadioButton(master=self, text="Png(未実装)", variable=self.output_option_ver, value="png")
        self.output_option2.grid(row=6, column=0, padx=10, pady=10)
        
        self.convert_save_button = ctk.CTkButton(master=self, text="変換して保存", command=self.convert)
        self.convert_save_button.grid(row=7, column=0, padx=10, pady=10)
        
        self.info1 = ctk.CTkLabel(master=self, text="info:背景画像の不透明度は無視されます")
        self.info1.grid(row=8, column=1, padx=20, pady=5, sticky="w")
        
        self.info2 = ctk.CTkLabel(master=self, text="info:背景画像に対して、変換する画像をマスクした結果のRGBが採用されます")
        self.info2.grid(row=9, column=1, padx=20, pady=5, sticky="w")        
        
        self.info2 = ctk.CTkLabel(master=self, text="info:現時点では変換後の透明には対応しておりません")
        self.info2.grid(row=10, column=1, padx=20, pady=5, sticky="w")               
        # endregion:widget
    
    # region:events
    
    def change_fill_color(self,*args):
        text = self.fill_color_entry.get()
        
        if text and text.startswith("#") and len(text)== 7:
            text = text[1:]
            try:
                hex_color = [int(text[0:2], 16),int(text[2:4], 16),int(text[4:6], 16)]
                colors_tree = KDTree(data.colors)
                _, min_indices = colors_tree.query(hex_color)
                color = data.colors[min_indices]
                text = data.colors2gid[tuple(color.tolist())]
                self.fill_color_entry.delete(0, "end")
                self.fill_color_entry.insert(0, text)
                self.fill_color_discription.configure(text=f"最背景色＝{text}")
                self.user_fill_color = text
                self.user_fill_color_select = True
            except:()
        elif str(text) in data.gid:
            self.fill_color_discription.configure(text=f"最背景色＝{text}")
            self.user_fill_color = str(text)
            self.user_fill_color_select = True
        else :
            self.fill_color_discription.configure(text="未定義の色です")
            self.user_fill_color_select = False
        if text == "":self.fill_color_discription.configure(text="最背景色(gID/#HEX)")
    
    def select_img_bg_path(self):
        
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.ico;*.webp;*.gif;")])
        
        if file_path:
            # Entryの文字をクリア
            self.img_bg_path_entry.delete(0, tk.END)
            # パスをEntryに挿入
            self.img_bg_path_entry.insert(0, file_path)
    
    def select_img_path(self):
        
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.ico;*.webp;*.gif;")])
        
        if file_path:
            # Entryの文字をクリア
            self.img_path_entry.delete(0, tk.END)
            # パスをEntryに挿入
            self.img_path_entry.insert(0, file_path)
    
    def convert(self):
        self.error_state = True
        
        if self.user_fill_color_select:
            self.fill_color = self.user_fill_color
        else:
            CTkMessagebox(title="コンバート失敗", message="最背景色を設定してください",icon="warning", option_1="閉じる",)
            self.error_state = False
        
        # パス取得
        img_bg_path = self.img_bg_path_entry.get()
        if img_bg_path != "":
            img_bg_path = Path(img_bg_path)
            if self.img_bg_path.exists():
                self.img_bg = Image.open(img_bg_path)
        else:
            self.img_bg = None
        
        img_path = self.img_path_entry.get()
        if img_path != "":
            self.img_path = Path(img_path)
            if self.img_path.exists():
                self.img = Image.open(img_path)
        else:
            if self.error_state:CTkMessagebox(title="コンバート失敗", message="変換する画像を設定してください",icon="warning", option_1="閉じる",)
            self.error_state = False
        
        # 以下プロセス用定義
        fill_color = data.gid2colors[self.fill_color]
        img_bg = self.img_bg
        img = self.img
        img_name = Path(self.img_path).name
        method_id = self.method_var.get()
        
        _pre_process = pre_process.pre_process(img,img_bg,fill_color)
        img = _pre_process["img"]
        bg_img = _pre_process["bg_img"]
        cam_y = _pre_process["cam_y"]
        cam_x = _pre_process["cam_x"]
        cam_arr= _pre_process["cam_arr"]
        
        # デバッグ:変換前pngのテスト出力
        # img = Image.fromarray(cam_arr, 'RGB')
        # img.save("変換前.png")
        
        
        if method_id == "RGB_distance":
            method.RGB_disatnce(cam_arr)
        if method_id == "Lab_distance":
            method.Lab_distance(cam_arr)
        
        # デバッグ:変換後pngのテスト出力
        # img = Image.fromarray(cam_arr, 'RGB')
        # img.save("変換後.png")
        converted_excel_name = "(AMC)"+img_name
        output.excel(cam_arr, cam_x, cam_y, download_path, converted_excel_name)
        CTkMessagebox(title="変換が成功しました！",message=converted_excel_name+"としてダウンロードに保存されました", icon="check", option_1="OK")
    
    
    # endregion:events
    def launch(self):
        self.mainloop()
    


def launch_error(error):
    messagebox.showerror("エラー：起動に失敗しました", str(error))
    

if __name__ == "__main__":
    try:
        app_id = "kuroneko100.Artmap Converter" + VERSION
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except (AttributeError, OSError):
        pass
    
    try:
        app = ArtmapConverter()
        app.launch()
    except (OSError, SyntaxError, ValueError, TypeError) as error:
        print("起動に失敗しました:", str(error))
        launch_error(error)
