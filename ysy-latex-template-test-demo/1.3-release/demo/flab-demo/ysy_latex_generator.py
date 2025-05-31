import tkinter as tk
from tkinter import ttk, messagebox
import os

# -- 配置选项数据 --
COLOR_OPTIONS = [
    'CatppuccinLatte', 'LiuYin', 'SPA', 'Elegant', 'OhMyPaper',
    'StarFieldRed', 'StarFieldBlue', 'SkyPinkBlue', 'SkyScarlet',
    'SkyRelax', 'Mondrian', 'DunHuang'
]
DEFAULT_COLOR = 'CatppuccinLatte'

# 文档类型显示名称到内部标识符的映射
DOC_TYPE_OPTIONS_DISPLAY = ['通用笔记', '近代物理实验报告', '基础物理实验报告', '学术论文']
DOC_TYPE_OPTIONS_INTERNAL = ['note', 'mplab', 'flab', 'paper']
DEFAULT_DOC_TYPE_DISPLAY = '通用笔记'

# 默认值
DEFAULT_CHINESE = True
DEFAULT_COVER = False # 默认不包含封面
DEFAULT_TOC = False   # 默认不包含目录
DEFAULT_REFS = False  # 默认不包含参考文献
DEFAULT_APPENDIX = False # 默认不包含附录

class LatexGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("LaTeX 主控文件生成器")
        master.geometry("500x650") # 调整窗口大小以容纳所有控件

        # -- Tkinter 变量 --
        self.color_var = tk.StringVar(value=DEFAULT_COLOR)
        self.chinese_var = tk.BooleanVar(value=DEFAULT_CHINESE)
        self.doc_type_display_var = tk.StringVar(value=DEFAULT_DOC_TYPE_DISPLAY)
        self.cover_var = tk.BooleanVar(value=DEFAULT_COVER)
        self.toc_var = tk.BooleanVar(value=DEFAULT_TOC)
        self.references_var = tk.BooleanVar(value=DEFAULT_REFS)
        self.appendix_var = tk.BooleanVar(value=DEFAULT_APPENDIX)

        # -- GUI 控件创建 --
        self.create_widgets()

        # -- 初始化提示 --
        self.update_warnings()

    def create_widgets(self):
        # 使用 frame 来更好地组织布局
        main_frame = ttk.Frame(self.master, padding="10 10 10 10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        current_row = 0

        # 选项标记1: 颜色
        ttk.Label(main_frame, text="颜色 (ycolor):").grid(column=0, row=current_row, sticky=tk.W, pady=5)
        color_combo = ttk.Combobox(main_frame, textvariable=self.color_var, values=COLOR_OPTIONS, state="readonly", width=25)
        color_combo.grid(column=1, row=current_row, sticky=tk.EW, padx=5, pady=5)
        current_row += 1

        # 选项标记2: 中文
        ttk.Label(main_frame, text="语言 (chinese):").grid(column=0, row=current_row, sticky=tk.W, pady=5)
        chinese_check = ttk.Checkbutton(main_frame, text="使用中文 (true/false)", variable=self.chinese_var, command=self.update_warnings)
        chinese_check.grid(column=1, row=current_row, sticky=tk.W, padx=5, pady=5)
        current_row += 1
        self.chinese_warning_label = ttk.Label(main_frame, text="", foreground="red")
        self.chinese_warning_label.grid(column=0, row=current_row, columnspan=2, sticky=tk.W, padx=5)
        current_row += 1

        # 选项标记3: 模式 (文档类型)
        ttk.Label(main_frame, text="文档类型 (type):").grid(column=0, row=current_row, sticky=tk.W, pady=5)
        doc_type_combo = ttk.Combobox(main_frame, textvariable=self.doc_type_display_var, values=DOC_TYPE_OPTIONS_DISPLAY, state="readonly", width=25)
        doc_type_combo.grid(column=1, row=current_row, sticky=tk.EW, padx=5, pady=5)
        doc_type_combo.bind("<<ComboboxSelected>>", self.update_warnings)
        current_row += 1
        self.mode_warning_label = ttk.Label(main_frame, text="", foreground="blue")
        self.mode_warning_label.grid(column=0, row=current_row, columnspan=2, sticky=tk.W, padx=5)
        current_row += 1

        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(column=0, row=current_row, columnspan=2, sticky='ew', pady=10)
        current_row += 1
        
        ttk.Label(main_frame, text="包含以下部分:").grid(column=0, row=current_row, columnspan=2, sticky=tk.W, pady=5)
        current_row +=1

        # 选项标记6: 封面
        cover_check = ttk.Checkbutton(main_frame, text="封面 (YsyCoverPage)", variable=self.cover_var)
        cover_check.grid(column=0, row=current_row, columnspan=2, sticky=tk.W, padx=15, pady=2)
        current_row += 1

        # 选项标记7: 目录
        toc_check = ttk.Checkbutton(main_frame, text="目录 (tableofcontents)", variable=self.toc_var)
        toc_check.grid(column=0, row=current_row, columnspan=2, sticky=tk.W, padx=15, pady=2)
        current_row += 1

        # 选项标记8: 参考文献
        references_check = ttk.Checkbutton(main_frame, text="参考文献 (YsyReferencesPage)", variable=self.references_var)
        references_check.grid(column=0, row=current_row, columnspan=2, sticky=tk.W, padx=15, pady=2)
        current_row += 1

        # 选项标记9: 附录
        appendix_check = ttk.Checkbutton(main_frame, text="附录 (YsyAppendixPage)", variable=self.appendix_var)
        appendix_check.grid(column=0, row=current_row, columnspan=2, sticky=tk.W, padx=15, pady=2)
        current_row += 1
        
        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(column=0, row=current_row, columnspan=2, sticky='ew', pady=10)
        current_row += 1

        # 生成按钮
        generate_button = ttk.Button(main_frame, text="生成 console.tex 文件", command=self.generate_file, width=30)
        generate_button.grid(column=0, row=current_row, columnspan=2, pady=20)
        current_row +=1

        main_frame.columnconfigure(1, weight=1) # 让第二列控件可以扩展

    def get_current_doc_type_internal(self):
        # 获取当前选择的文档类型的内部标识符
        selected_display_name = self.doc_type_display_var.get()
        try:
            idx = DOC_TYPE_OPTIONS_DISPLAY.index(selected_display_name)
            return DOC_TYPE_OPTIONS_INTERNAL[idx]
        except ValueError:
            # 理论上不应发生，因为Combobox是只读的
            return DOC_TYPE_OPTIONS_INTERNAL[DOC_TYPE_OPTIONS_DISPLAY.index(DEFAULT_DOC_TYPE_DISPLAY)]


    def update_warnings(self, event=None): # event 参数是为了兼容 ComboboxSelected 事件
        # 更新提示信息
        # 【选项标记2】的提示: "请不要在论文模式以外的模式用英文。"
        doc_type_internal = self.get_current_doc_type_internal()
        is_chinese = self.chinese_var.get()

        if doc_type_internal != 'paper' and not is_chinese:
            self.chinese_warning_label.config(text="提示: 请不要在论文模式以外的模式用英文。")
        else:
            self.chinese_warning_label.config(text="")

        # 【选项标记3】的提示: "选用论文模式时推荐采用黑白主题配色。"
        if doc_type_internal == 'paper':
            self.mode_warning_label.config(text="提示: 选用论文模式时推荐采用黑白主题配色。")
        else:
            self.mode_warning_label.config(text="")


    def generate_file(self):
        # 1. 获取所有选项的值
        ycolor_val = self.color_var.get()
        chinese_val_bool = self.chinese_var.get()
        chinese_val_str = "true" if chinese_val_bool else "false" # LaTeX 需要 'true' 或 'false'

        doc_type_internal = self.get_current_doc_type_internal()

        # 2. 根据文档类型确定documentclass的type, 个人信息, 和拓展项
        if doc_type_internal == 'note': # 通用笔记
            cls_type_val = 'universal'
            personal_info_val = """\\renewcommand{\\TitleName}{}
\\renewcommand{\\AuthorName}{}
\\renewcommand{\\Address}{}
\\renewcommand{\\Preface}{}
\\renewcommand{\\CoverIllustration}{}"""
            extension_val = 'YsyNote'
        elif doc_type_internal == 'mplab': # 近代物理实验报告
            cls_type_val = 'universal' # 假设近代物理实验也用 universal type
            personal_info_val = """\\renewcommand{\\TitleName}{近代物理实验II实验报告}
\\renewcommand{\\AuthorName}{作者1，作者2，其它作者}
\\renewcommand{\\Address}{}
\\renewcommand{\\Preface}{}
\\renewcommand{\\CoverIllustration}{}"""
            extension_val = 'YsyLab'
        elif doc_type_internal == 'flab': # 基础物理实验报告
            cls_type_val = 'flab'
            personal_info_val = """\\renewcommand{\\TitleName}{}
\\renewcommand{\\AuthorName}{}
\\renewcommand{\\Grade}{}
\\renewcommand{\\LabTime}{}
\\renewcommand{\\SchoolNumber}{}"""
            extension_val = 'FundamentalLab'
        elif doc_type_internal == 'paper': # 学术论文
            cls_type_val = 'paper'
            personal_info_val = """\\renewcommand{\\TitleName}{}
\\renewcommand{\\AuthorName}{作者1\\textsuperscript{1}, 作者2\\textsuperscript{2}, 作者3\\textsuperscript{1}}
\\renewcommand{\\Address}{\\textsuperscript{1}~地址1}
\\renewcommand{\\AddInfo}{}
\\renewcommand{\\Abstract}{}"""
            extension_val = 'YsyPaper'
        else: # 后备，理论上不会执行到
            cls_type_val = 'universal'
            personal_info_val = ""
            extension_val = "YsyNote" # 默认一个

        # 3. 根据选择确定可选部分
        cover_val = "\\YsyCoverPage" if self.cover_var.get() else ""
        toc_val = "\\tableofcontents" if self.toc_var.get() else ""
        
        references_val = ""
        if self.references_var.get():
            references_val = ("\\clearpage\n"
                              "\\YsyReferencesPage{\\input{contents/ref}}")

        appendix_val = ""
        if self.appendix_var.get():
            appendix_val = ("\\clearpage\n"
                            "\\YsyAppendixPage{\\input{contents/appendix}}")

        # 4. 构建 LaTeX 内容字符串
        # 使用 f-string。注意 LaTeX 中的花括号需要转义为 {{ 和 }}
        # 但这里是直接插入变量，所以 {variable} 是正确的。
        # 只有当你想在 f-string 中表示字面上的花括号时才用 {{ 或 }}。
        # 例如 \documentclass[...]{{{ysy-latex/YsyClass}}} -> 表示 {ysy-latex/YsyClass}
        # 这里，大括号内的内容是参数，所以不需要双重花括号
        latex_content = f"""% 主控文件

% 加载类
%!TEX program = xelatex
\\documentclass[ycolor={ycolor_val},chinese={chinese_val_str},type={cls_type_val}]{{ysy-latex/YsyClass}}

% 个人信息
{personal_info_val}
% 拓展
\\input{{ysy-latex/extension/{extension_val}}} 

% 主控部分
\\begin{{document}}        
	% 封面
        {cover_val}
        % 目录
        {toc_val}
        % 主要内容
        \\include{{contents/main}}
        % 参考文献
        {references_val}
        % 附录
        {appendix_val}
\\end{{document}}
"""
        # 5. 写入文件
        try:
            filepath = os.path.join(os.getcwd(), "console.tex")
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(latex_content)
            messagebox.showinfo("成功", f"文件 console.tex 已成功生成在:\n{filepath}")
        except IOError as e:
            messagebox.showerror("错误", f"无法写入文件 console.tex:\n{e}")
        except Exception as e:
            messagebox.showerror("未知错误", f"发生错误:\n{e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = LatexGeneratorApp(root)
    root.mainloop()