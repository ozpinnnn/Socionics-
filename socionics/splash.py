"""GIF 启动闪屏：无边框置顶窗口 + 逐帧动画，指定时长后自动销毁。"""

import tkinter as tk

from PIL import Image, ImageTk


class GifSplash:
    """播放 GIF 启动页，结束后回调 on_finish。

    :param root: Tk 根窗口（保持隐藏）
    :param gif_path: GIF 文件路径
    :param on_finish: 关闭后的回调，用于显示主窗口
    :param duration: 展示时长（毫秒）
    """

    def __init__(self, root, gif_path, on_finish, duration=3000):
        self.root = root
        self.on_finish = on_finish
        self.duration = duration

        self.splash = tk.Toplevel(root)
        self.splash.overrideredirect(True)      # 无边框
        self.splash.attributes("-topmost", True)  # 置顶

        self.frames = []
        try:
            gif = Image.open(gif_path)
            self.delay = gif.info.get("duration", 100)
            img_w, img_h = gif.size

            # 居中显示
            sw = self.splash.winfo_screenwidth()
            sh = self.splash.winfo_screenheight()
            x = (sw - img_w) // 2
            y = (sh - img_h) // 2
            self.splash.geometry(f"{img_w}x{img_h}+{x}+{y}")

            # 提取所有帧
            try:
                while True:
                    self.frames.append(ImageTk.PhotoImage(gif.copy()))
                    gif.seek(len(self.frames))
            except EOFError:
                pass
        except Exception as e:
            print(f"启动图加载失败: {e}")
            self.close()
            return

        self.label = tk.Label(self.splash, image=self.frames[0], bd=0)
        self.label.pack()

        self.index = 0
        self.animate()
        self.splash.after(duration, self.close)

    def animate(self):
        if self.splash.winfo_exists():
            self.label.config(image=self.frames[self.index])
            self.index = (self.index + 1) % len(self.frames)
            self.splash.after(self.delay, self.animate)

    def close(self):
        if self.splash.winfo_exists():
            self.splash.destroy()
        self.on_finish()
