import tkinter as tk
from tkinter import ttk

# 数据定义保持不变...
TYPES = ["ILE", "SEI", "ESE", "LII", "EIE", "LSI", "SLE", "IEI", "SEE", "ILI", "LIE", "ESI", "LSE", "EII", "IEE", "SLI"]
NAME_TO_ID = {name: idx for idx, name in enumerate(TYPES)}
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
    row = RELATION_MATRIX[base_id]
    return row.index(rel_name) if rel_name in row else base_id


def get_relation_name(base_id, target_id):
    return RELATION_MATRIX[base_id][target_id]


class SocionicsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Socionics 关系计算器")
        self.root.geometry("360x580")  # 稍微加宽加高，给换行留空间
        self.root.configure(bg="#202020")
        self.history = []
        self.setup_ui()

    def setup_ui(self):
        # 顶部：类型选择器
        top_frame = tk.Frame(self.root, bg="#202020", pady=10, padx=10)
        top_frame.pack(fill="x")
        self.type_combo = ttk.Combobox(top_frame, values=["未选择(自动推导)"] + TYPES, width=15, state="readonly")
        self.type_combo.set("未选择(自动推导)")
        self.type_combo.pack(side="right")
        self.type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_display())

        # 显示屏区域
        display_frame = tk.Frame(self.root, bg="#202020", padx=15, pady=5)
        display_frame.pack(fill="x", minsize=120)  # 最小高度防止跳动

        # 算式过程 (关键点：使用 wraplength 实现自动换行)
        self.lbl_formula = tk.Label(
            display_frame, text="", font=('Microsoft YaHei UI', 10),
            bg="#202020", fg="#AAAAAA", anchor="e", justify="right",
            wraplength=320  # 自动换行宽度
        )
        self.lbl_formula.pack(fill="x", pady=5)

        # 计算结果
        self.lbl_result = tk.Label(display_frame, text="等待输入...", font=('Microsoft YaHei UI', 32, 'bold'),
                                   bg="#202020", fg="white", anchor="e")
        self.lbl_result.pack(fill="x")

        # 按钮网格保持不变...
        btn_frame = tk.Frame(self.root, bg="#202020")
        btn_frame.pack(fill="both", expand=True, padx=2, pady=2)
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
        for i, (text, bg, fg) in enumerate(buttons):
            btn = tk.Button(btn_frame, text=text, font=('Microsoft YaHei UI', 11), bg=bg, fg=fg, relief="flat",
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=i // 4, column=i % 4, sticky="nsew", padx=2, pady=2)
        for i in range(5): btn_frame.rowconfigure(i, weight=1)
        for i in range(4): btn_frame.columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char in ('C', 'CE'):
            self.history.clear()
        elif char == '⌫':
            (self.history.pop() if self.history else None)
        elif char == '=':
            self.evaluate_to_base()
        else:
            self.history.append(char)
        self.update_display()

    def evaluate_to_base(self):
        selected_type = self.type_combo.get()
        if not self.history or selected_type == "未选择(自动推导)": return
        base_id = NAME_TO_ID[selected_type]
        for rel in self.history: base_id = apply_relation(base_id, rel)
        self.type_combo.set(TYPES[base_id])
        self.history.clear()

    def update_display(self):
        selected_type = self.type_combo.get()
        has_base = (selected_type != "未选择(自动推导)")
        base_id = NAME_TO_ID[selected_type] if has_base else 0
        current_id = base_id

        # 更新公式
        formula_text = (selected_type + " ") if has_base else ""
        if self.history:
            formula_text += " → ".join(self.history) + " ="
            for rel in self.history: current_id = apply_relation(current_id, rel)
        self.lbl_formula.config(text=formula_text)

        # 更新结果
        if not self.history:
            res_text = selected_type if has_base else "等待输入..."
        else:
            res_text = TYPES[current_id] if has_base else get_relation_name(0, current_id)
        self.lbl_result.config(text=res_text)


if __name__ == "__main__":
    root = tk.Tk()
    try:
        import ctypes; ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    app = SocionicsCalculator(root)
    root.mainloop()