"""平台相关适配：Windows 高 DPI。"""

import sys


def enable_dpi_awareness() -> bool:
    """让 Tkinter 窗口在高分屏上不被系统拉伸模糊。

    优先使用 Per-Monitor DPI Awareness（Win8.1+），失败时退回系统级 DPI 感知。
    """
    if sys.platform != "win32":
        return False

    import ctypes

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        return True
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
            return True
        except Exception:
            return False
