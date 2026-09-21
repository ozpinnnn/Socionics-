"""Tkinter 计算器界面。

交互模型刻意模仿实体计算器：
    * 顶部下拉框 = 基准类型（留空则进入「纯关系推演」模式）
    * 关系按钮    = 算子，依次追加进 history 形成算式
    * `=`         = 把当前结果固化为新的基准类型并清空算式
"""

import tkinter as tk
from tkinter import ttk

from .relations import TYPES, NAME_TO_ID, RELATIONS, resolve, get_relation_name

#: 未指定基准类型时的占位文案
NO_BASE = "未选择(自动推导)"

#: 深色主题配色
BG = "#202020"
FG = "white"
FG_SUB = "#AAAAAA"
BTN_FUNC_BG = "#323232"
BTN_REL_BG = "#3b3b3b"
BTN_EQ_BG = "#4CC2FF"
BTN_ACTIVE_BG = "#4c4c4c"
BTN_EQ_ACTIVE_BG = "#28a8ea"


class SocionicsCalculator:
    """类间关系计算器主界面。

    :param root: Tk 根窗口
    :param scale: 全局缩放系数（1.0 = 纯净版尺寸，1.2 = 完整版尺寸）
    :param title: 窗口标题
    """

    def __init__(self, root, scale: float = 1.0, title: str = "Socionics 类间关系计算器"):
        self.root = root
        self.scale = scale
        self.base_font = "Microsoft YaHei UI"

        self.history = []          # 记录按下的关系按钮流
        self.type_combo = None
        self.lbl_formula = None
        self.lbl_result = None

        self.root.title(title)
        self.root.geometry(f"{int(500 * scale)}x{int(750 * scale)}")
        self.root.configure(bg=BG)

        self.setup_ui()

    # ------------------------------------------------------------ UI

    def setup_ui(self):
        font_small = (self.base_font, int(11 * self.scale))
        font_medium = (self.base_font, int(12 * self.scale))
        font_button = (self.base_font, int(15 * self.scale))

        # 顶部：类型选择器
        top_frame = tk.Frame(self.root, bg=BG, pady=int(10 * self.scale), padx=int(10 * self.scale))
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="≡  标准", font=font_medium, bg=BG, fg=FG).pack(side="left")

        self.type_combo = ttk.Combobox(
            top_frame, values=[NO_BASE] + TYPES, width=15, state="readonly"
        )
        self.type_combo.set(NO_BASE)
        self.type_combo.pack(side="right")
        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_changed)

        # 显示屏区域
        display_frame = tk.Frame(self.root, bg=BG, padx=15, pady=10)
        display_frame.pack(fill="x", expand=True)

        # 算式过程
        self.lbl_formula = tk.Label(
            display_frame,
            text="",
            font=font_small,
            bg=BG,
            fg=FG_SUB,
            anchor="e",
            justify="right",                       # 换行后多行文本依然靠右对齐
            wraplength=int(460 * self.scale),      # 超出这个宽度自动换行
        )
        self.lbl_formula.pack(fill="x")

        # 计算结果
        self.lbl_result = tk.Label(
            display_frame, text=NO_BASE, font=(self.base_font, int(32 * self.scale), "bold"),
            bg=BG, fg=FG, anchor="e",
        )
        self.lbl_result.pack(fill="x")

        # 按钮网格：3 个功能键 + 16 个关系 + 等号 = 20 个，5 行 4 列
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(fill="both", expand=True, padx=3, pady=4)

        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        buttons = (
            [("C", BTN_FUNC_BG, FG), ("CE", BTN_FUNC_BG, FG), ("⌫", BTN_FUNC_BG, FG)]
            + [(rel, BTN_REL_BG, FG) for rel in RELATIONS]
            + [("=", BTN_EQ_BG, "black")]
        )

        for index, (text, bg_color, fg_color) in enumerate(buttons):
            active_bg = BTN_EQ_ACTIVE_BG if bg_color == BTN_EQ_BG else BTN_ACTIVE_BG
            btn = tk.Button(
                btn_frame, text=text, font=font_button, bg=bg_color, fg=fg_color,
                activebackground=active_bg, relief="flat", borderwidth=0,
                command=lambda t=text: self.on_button_click(t),
            )
            btn.grid(row=index // 4, column=index % 4, sticky="nsew", padx=2, pady=2)

    # ------------------------------------------------------------ 事件

    def on_type_changed(self, event=None):
        self.update_display()

    def on_button_click(self, char):
        if char in ("C", "CE"):
            self.history.clear()
        elif char == "⌫":
            if self.history:
                self.history.pop()
        elif char == "=":
            self.evaluate_to_base()
        else:
            self.history.append(char)
        self.update_display()

    def evaluate_to_base(self):
        """按下等号时，把运算结果固化为新的基底并清空公式。"""
        selected_type = self.type_combo.get()
        if not self.history or selected_type == NO_BASE:
            return

        final_id = resolve(NAME_TO_ID[selected_type], self.history)
        self.type_combo.set(TYPES[final_id])
        self.history.clear()

    # ------------------------------------------------------------ 渲染

    def update_display(self):
        selected_type = self.type_combo.get()
        has_base = selected_type != NO_BASE

        # 未指定类型时用 ILE(0) 作为傀儡基底来推导纯关系
        base_id = NAME_TO_ID[selected_type] if has_base else 0
        current_id = resolve(base_id, self.history)

        # 算式文本
        formula_text = (selected_type + " ") if has_base else ""
        if self.history:
            formula_text += " -> ".join(self.history) + " ="
        self.lbl_formula.config(text=formula_text)

        # 大字结果
        if not self.history:
            self.lbl_result.config(text=selected_type if has_base else "等待输入...")
            self.lbl_result.config(font=(self.base_font, int(24 * self.scale), "bold"))
        elif has_base:
            self.lbl_result.config(text=TYPES[current_id])
            self.lbl_result.config(font=(self.base_font, int(36 * self.scale), "bold"))
        else:
            # 纯关系推演：把结果类型 ID 翻译回关系名
            self.lbl_result.config(text=get_relation_name(0, current_id))
            self.lbl_result.config(font=(self.base_font, int(32 * self.scale), "bold"))
