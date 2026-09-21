# Socionics 类间关系计算器

输入一个 Socionics 类型（16 型之一），再点一串「类间关系」，就能算出最终落到哪个类型；
不指定起点时，还能做纯关系的复合推演（如 `对偶 -> 激活 = 镜像`）。

界面刻意做成计算器的样子：关系即算子，`=` 把结果固化为新的基准类型，可继续往下推。

## 运行

```bash
pip install -r requirements.txt

python main.py          # 完整版：GIF 启动动画 + 1.2 倍界面缩放
python main_clear.py    # 纯净版：无启动动画，不依赖 Pillow
```

## 打包

```bash
python -m PyInstaller packaging/soc.spec        # -> dist/Socionics类间关系计算器.exe
python -m PyInstaller packaging/socClear.spec   # -> dist/Soc类间关系计算器纯净版.exe
```

## 目录结构

```
.
├── main.py                 完整版入口
├── main_clear.py           纯净版入口
├── socionics/
│   ├── relations.py        16 类型定义 + 16x16 关系矩阵 + 查表算法（纯逻辑）
│   ├── calculator.py       Tkinter 计算器界面
│   ├── splash.py           GIF 启动闪屏
│   ├── paths.py            开发 / 打包两种模式下的资源路径解析
│   └── platform.py         Windows 高 DPI 适配
├── assets/                 图标、启动图等静态资源
├── packaging/              PyInstaller 打包配置
└── legacy/                 重构前的单文件旧版本，仅作留档，可随时删除
```

> `legacy/` 里的 `soc.py`、`socClear.py`、`1.py` 是重构前的重复脚本，逻辑已完整迁移到
> `socionics/` 包中（关系矩阵逐字一致），确认无误后可删除。

## 实现原理

核心是一张 16×16 的**类间关系矩阵** `socionics/relations.py::RELATION_MATRIX`：

```
RELATION_MATRIX[基准类型ID][目标类型ID] = 关系名
```

- 16 个类型按 `TYPES` 的顺序编号 0~15；
- 每一行都是 16 个关系名的一个排列（拉丁方），因此「已知关系反查类型」是可逆的；
- 对角线恒为「相等」，是关系复合的单位元；
- 矩阵沿对角线对称，但 `+有益/有益+`、`+监督/监督+` 是有向关系对，互为反向。

**运算**就是查表 + 链式复合，没有任何数学推导：

```python
resolve(base_id, ["对偶", "激活"])     # ILE ->(对偶) SEI ->(激活) LII
```

因为关系集合对复合**封闭**（任意两个关系复合后仍是这 16 个关系之一），且复合结果
**与所选基准类型无关**，所以还能做**纯关系推演**：不指定起点时，拿 `ILE(0)` 当傀儡基底
跑一遍复合，再用它与原基底的关系名把结果翻译回关系：

```python
compose_relations(["对偶", "激活"])     # -> "镜像"
```

⚠️ 复合**与顺序有关**（`约等于 -> 亲族` 与 `亲族 -> 约等于` 结果不同），界面按点击顺序依次复合。
