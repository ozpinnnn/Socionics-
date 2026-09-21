"""Socionics 类间关系计算器。

模块划分：
    relations  -- 16 类型与类间关系的核心数据、查表算法（纯逻辑，无 UI 依赖）
    calculator -- Tkinter 计算器界面
    splash     -- GIF 启动闪屏
    paths      -- 开发/打包两种模式下的资源路径解析
    platform   -- Windows 高 DPI 适配
"""

from .relations import (
    TYPES,
    NAME_TO_ID,
    RELATIONS,
    RELATION_MATRIX,
    apply_relation,
    get_relation_name,
    resolve,
    compose_relations,
)

__version__ = "1.0.0"

__all__ = [
    "TYPES",
    "NAME_TO_ID",
    "RELATIONS",
    "RELATION_MATRIX",
    "apply_relation",
    "get_relation_name",
    "resolve",
    "compose_relations",
]
