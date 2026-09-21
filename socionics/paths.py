"""开发模式 / PyInstaller 打包模式下的资源路径解析。"""

import os
import sys
from pathlib import Path

#: 项目根目录（socionics/ 的上一级）
PROJECT_ROOT = Path(__file__).resolve().parent.parent

#: 图片、图标等静态资源目录
ASSETS_DIR = PROJECT_ROOT / "assets"


def _is_frozen() -> bool:
    """是否被 PyInstaller 打包（此时资源解压在 sys._MEIPASS）。"""
    return bool(getattr(sys, "frozen", False)) and hasattr(sys, "_MEIPASS")


def resource_path(relative_path: str) -> str:
    """按项目根目录解析相对路径，打包后自动切换到临时解压目录。"""
    if _is_frozen():
        return os.path.join(sys._MEIPASS, relative_path)
    return str(PROJECT_ROOT / relative_path)


def asset_path(name: str) -> str:
    """解析 assets/ 下的资源文件；打包后资源被拍平到根目录。"""
    if _is_frozen():
        return os.path.join(sys._MEIPASS, name)
    return str(ASSETS_DIR / name)
