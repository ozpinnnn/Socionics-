"""纯净版入口：无启动动画、原始尺寸，依赖更少（不需要 Pillow）。

运行：
    python main_clear.py
"""

import tkinter as tk

from socionics.calculator import SocionicsCalculator
from socionics.platform import enable_dpi_awareness


def run_app():
    enable_dpi_awareness()

    root = tk.Tk()
    SocionicsCalculator(root, scale=1.0, title="Socionics 类间关系计算器（纯净版）")
    root.mainloop()


if __name__ == "__main__":
    run_app()
