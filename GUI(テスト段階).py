import os
import tkinter as tk
import tkinter.filedialog
import ctypes
import darkdetect

#region:info
app_info= {"ver":"Ver 0.0",}
#endregion:info

try:
    app_id = "kuroneko100.Artmap Converter"+app_info["ver"]
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
except Exception:
    pass

class TkinterClass:
    def __init__(self):
        root = tk.Tk()
        root.title("Artmap Converter🖌"+app_info["ver"])
        root.iconbitmap("chibiki.ico")
        root.geometry("750x500")
        if darkdetect.isDark():
             bg_color = "#202020"
             fg_color = "#e0e0e0"
        else:
            bg_color = "#e0e0e0"
            fg_color = "#202020"
        root.configure(bg=bg_color) #背景色指定
        
        if darkdetect.isDark():
            label = tk.Label(root,text="現在のテーマ:ダークモード",bg=bg_color, fg=fg_color)
            label.pack()
        else:
            label = tk.Label(root,text="現在のテーマ:ライトモード",bg=bg_color, fg=fg_color)
            label.pack()

        
        root.mainloop() 


if __name__ == '__main__':
    TkinterClass()