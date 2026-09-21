"""完整版入口：带 GIF 启动动画、界面按 1.2 倍缩放。

运行：
    python main.py
"""

import os
import tkinter as tk

from socionics.calculator import SocionicsCalculator
from socionics.paths import asset_path
from socionics.platform import enable_dpi_awareness
from socionics.splash import GifSplash

SPLASH_GIF = "start1.gif"
SPLASH_DURATION = 3000
SCALE = 1.2


def run_app():
    enable_dpi_awareness()

    root = tk.Tk()
    root.withdraw()  # 启动时先隐藏主窗口

    def show_main():
        SocionicsCalculator(root, scale=SCALE)
        root.deiconify()

    gif_file = asset_path(SPLASH_GIF)
    if os.path.exists(gif_file):
        GifSplash(root, gif_file, show_main, duration=SPLASH_DURATION)
    else:
        show_main()

    root.mainloop()


if __name__ == "__main__":
    run_app()
