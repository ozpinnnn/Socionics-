import tkinter as tk
from tkinter import ttk


# ==========================================
# 数据
# ==========================================
TYPES = [
    "ILE", "SEI", "ESE", "LII", "EIE", "LSI", "SLE", "IEI",
    "SEE", "ILI", "LIE", "ESI", "LSE", "EII", "IEE", "SLI"
]
NAME_TO_ID = {name: idx for idx, name in enumerate(TYPES)}
# 16x16 关系矩阵
# 每一行代表“基准类型”，每一列代表“目标类型”，交点就是关系。
# 例如 RELATION_MATRIX[0][6] 代表 ILE(0) 和 SLE(6) 的关系 -> "合作"
RELATION_MATRIX = [
    ["相等", "对偶", "激活", "镜像", "+有益", "+监督", "合作", "幻想", "超我", "消失", "约等于", "冲突", "有益+",
     "监督+", "亲族", "半对偶"],  # ILE
    ["对偶", "相等", "镜像", "激活", "+监督", "+有益", "幻想", "合作", "消失", "超我", "冲突", "约等于", "监督+",
     "有益+", "半对偶", "亲族"],  # SEI
    ["激活", "镜像", "相等", "对偶", "亲族", "半对偶", "有益+", "监督+", "约等于", "冲突", "超我", "消失", "合作",
     "幻想", "+有益", "+监督"],  # ESE
    ["镜像", "激活", "对偶", "相等", "半对偶", "亲族", "监督+", "有益+", "冲突", "约等于", "消失", "超我", "幻想",
     "合作", "+监督", "+有益"],  # LII
    ["有益+", "监督+", "亲族", "半对偶", "相等", "对偶", "激活", "镜像", "+有益", "+监督", "合作", "幻想", "超我",
     "消失", "约等于", "冲突"],  # EIE
    ["监督+", "有益+", "半对偶", "亲族", "对偶", "相等", "镜像", "激活", "+监督", "+有益", "幻想", "合作", "消失",
     "超我", "冲突", "约等于"],  # LSI
    ["合作", "幻想", "+有益", "+监督", "激活", "镜像", "相等", "对偶", "亲族", "半对偶", "有益+", "监督+", "约等于",
     "冲突", "超我", "消失"],  # SLE
    ["幻想", "合作", "+监督", "+有益", "镜像", "激活", "对偶", "相等", "半对偶", "亲族", "监督+", "有益+", "冲突",
     "约等于", "消失", "超我"],  # IEI
    ["超我", "消失", "约等于", "冲突", "有益+", "监督+", "亲族", "半对偶", "相等", "对偶", "激活", "镜像", "+有益",
     "+监督", "合作", "幻想"],  # SEE
    ["消失", "超我", "冲突", "约等于", "监督+", "有益+", "半对偶", "亲族", "对偶", "相等", "镜像", "激活", "+监督",
     "+有益", "幻想", "合作"],  # ILI
    ["约等于", "冲突", "超我", "消失", "合作", "幻想", "+有益", "+监督", "激活", "镜像", "相等", "对偶", "亲族",
     "半对偶", "有益+", "监督+"],  # LIE
    ["冲突", "约等于", "消失", "超我", "幻想", "合作", "+监督", "+有益", "镜像", "激活", "对偶", "相等", "半对偶",
     "亲族", "监督+", "有益+"],  # ESI
    ["+有益", "+监督", "合作", "幻想", "超我", "消失", "约等于", "冲突", "有益+", "监督+", "亲族", "半对偶", "相等",
     "对偶", "激活", "镜像"],  # LSE
    ["+监督", "+有益", "幻想", "合作", "消失", "超我", "冲突", "约等于", "监督+", "有益+", "半对偶", "亲族", "对偶",
     "相等", "镜像", "激活"],  # EII
    ["亲族", "半对偶", "有益+", "监督+", "约等于", "冲突", "超我", "消失", "合作", "幻想", "+有益", "+监督", "激活",
     "镜像", "相等", "对偶"],  # IEE
    ["半对偶", "亲族", "监督+", "有益+", "冲突", "约等于", "消失", "超我", "幻想", "合作", "+监督", "+有益", "镜像",
     "激活", "对偶", "相等"]  # SLI
]


def apply_relation(base_id, rel_name):
    """根据基准类型ID和关系名称，在矩阵中找到目标类型的ID"""
    row = RELATION_MATRIX[base_id]
    if rel_name in row:
        return row.index(rel_name)
    return base_id


def get_relation_name(base_id, target_id):
    """查表获取两个类型ID之间的关系名称"""
    return RELATION_MATRIX[base_id][target_id]


# ==========================================
# 计算器 UI
# ==========================================
class SocionicsCalculator:

    def __init__(self, root):

        self.root = root

        self.root.title("Socionics 类间关系计算器")

        self.root.geometry("500x750")

        self.root.configure(bg="#202020")

        self.history = []  # 记录按下的关系按钮流

        self.setup_ui()

    def setup_ui(self):

        # 顶部：类型选择器

        top_frame = tk.Frame(self.root, bg="#202020", pady=10, padx=10)

        top_frame.pack(fill="x")

        tk.Label(top_frame, text="≡  标准", font=('Microsoft YaHei UI', 12), bg="#202020", fg="white").pack(
            side="left")

        self.type_combo = ttk.Combobox(top_frame, values=["未选择(自动推导)"] + TYPES, width=15,
                                       state="readonly")

        self.type_combo.set("未选择(自动推导)")

        self.type_combo.pack(side="right")

        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_changed)

        # 显示屏区域

        display_frame = tk.Frame(self.root, bg="#202020", padx=15, pady=10)

        display_frame.pack(fill="x", expand=True)

        # 算式过程

        self.lbl_formula = tk.Label(

            display_frame,

            text="",

            font=('Microsoft YaHei UI', 11),

            bg="#202020",

            fg="#AAAAAA",

            anchor="e",

            justify="right",  # 确保换行后多行文本依然靠右对齐

            wraplength=460  # 设置换行宽度（像素），超出这个宽度自动换行

        )

        self.lbl_formula.pack(fill="x")

        # 计算结果

        self.lbl_result = tk.Label(display_frame, text="None", font=('Microsoft YaHei UI', 32, 'bold'),

                                   bg="#202020", fg="white", anchor="e")

        self.lbl_result.pack(fill="x")

        # 按钮网格

        btn_frame = tk.Frame(self.root, bg="#202020")

        btn_frame.pack(fill="both", expand=True, padx=3, pady=4)

        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        # 按钮布局：功能键 + 16个精确匹配图表的关系

        buttons = [

            ('C', '#323232', 'white'), ('CE', '#323232', 'white'), ('⌫', '#323232', 'white'),

            ('相等', '#3b3b3b', 'white'),

            ('约等于', '#3b3b3b', 'white'), ('亲族', '#3b3b3b', 'white'), ('幻想', '#3b3b3b', 'white'),

            ('半对偶', '#3b3b3b', 'white'),

            ('超我', '#3b3b3b', 'white'), ('消失', '#3b3b3b', 'white'), ('合作', '#3b3b3b', 'white'),

            ('镜像', '#3b3b3b', 'white'),

            ('冲突', '#3b3b3b', 'white'), ('+监督', '#3b3b3b', 'white'), ('监督+', '#3b3b3b', 'white'),

            ('激活', '#3b3b3b', 'white'),

            ('+有益', '#3b3b3b', 'white'), ('有益+', '#3b3b3b', 'white'), ('对偶', '#3b3b3b', 'white'),

            ('=', '#4CC2FF', 'black')

        ]

        row, col = 0, 0

        for (text, bg_color, fg_color) in buttons:

            cmd = lambda t=text: self.on_button_click(t)

            btn = tk.Button(btn_frame, text=text, font=('Microsoft YaHei UI', 15), bg=bg_color, fg=fg_color,

                            activebackground="#4c4c4c" if bg_color != "#4CC2FF" else "#28a8ea",

                            relief="flat", borderwidth=0, command=cmd)

            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

            col += 1

            if col > 3:
                col = 0

                row += 1

    def on_type_changed(self, event):

        self.update_display()

    def on_button_click(self, char):

        if char in ('C', 'CE'):

            self.history.clear()

        elif char == '⌫':

            if self.history:
                self.history.pop()

        elif char == '=':

            self.evaluate_to_base()

        else:

            self.history.append(char)

        self.update_display()

    def evaluate_to_base(self):

        """按下等号时，把运算结果固化为新的基底并清空公式"""

        selected_type = self.type_combo.get()

        if not self.history: return

        if selected_type != "未选择(自动推导)":

            base_id = NAME_TO_ID[selected_type]

            current_id = base_id

            for rel in self.history:
                current_id = apply_relation(current_id, rel)

            final_type = TYPES[current_id]

            self.type_combo.set(final_type)

            self.history.clear()

    def update_display(self):

        selected_type = self.type_combo.get()

        has_base = selected_type != "未选择(自动推导)"

        # 默认使用 ILE(0) 作为傀儡基底来推导纯关系

        base_id = NAME_TO_ID[selected_type] if has_base else 0

        current_id = base_id

        # 显示公式文本

        formula_text = (selected_type + " ") if has_base else ""

        if self.history:

            formula_text += " -> ".join(self.history) + " ="

            for rel in self.history:
                current_id = apply_relation(current_id, rel)

        self.lbl_formula.config(text=formula_text)

        # 计算当前大字结果

        if not self.history:

            self.lbl_result.config(text=selected_type if has_base else "等待输入...")

            self.lbl_result.config(font=('Microsoft YaHei UI', 24, 'bold'))

        else:

            if has_base:

                # 显示具体的 16 人格类型

                self.lbl_result.config(text=TYPES[current_id])

                self.lbl_result.config(font=('Microsoft YaHei UI', 36, 'bold'))

            else:

                # 显示纯关系推演的结果

                final_rel_name = get_relation_name(0, current_id)

                self.lbl_result.config(text=final_rel_name)

                self.lbl_result.config(font=('Microsoft YaHei UI', 32, 'bold'))


if __name__ == "__main__":
    root = tk.Tk()
    try: import ctypes; ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    app = SocionicsCalculator(root)
    root.mainloop()