# 嘉豪工具箱 3.0
# 开发者：Deepseek-R1 and woshiikun_1145

import os
import sys
import webbrowser
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import subprocess
from pathlib import Path
import datetime

class JiahaoToolbox:
    def __init__(self):
        """初始化工具箱"""
        
        # 基本版本信息
        self.version = "3.251129.240e.562a.240e.7d62.a07"
        self.developer = "Deepseek-R1 and woshiikun_1145"
        self.last_update = "25/11/29 19:07"
        self.bilibili_space = "https://space.bilibili.com/1767512352"
        self.development_channel = "Release" 
        #alpha or beta or release
        
        # 默认调试模式配置
        self.debug_mode = False
        
        # 默认制裁模式配置
        # 总开关：是否启用制裁模式（True or False）
        self.sanction_mode_enabled = True

        # 制裁时间段配置（按星期几分别设置）
        # 格式：{星期几: [("开始时间", "结束时间"), ...]}
        # 0=周一, 1=周二, 2=周三, 3=周四, 4=周五, 5=周六, 6=周日
        self.sanction_periods = {
            # 星期一：2个时间段
            0: [
                ("11:45", "12:25"),   # 1
                ("15:55", "16:35"),   # 2 
            ],
            
            # 星期二：2个时间段
            1: [
                ("11:55", "12:35"),   # 1
                ("15:00", "15:40")    # 2
            ],
            
            # 星期三：0个时间段
            2: [],
            
            # 星期四：1个时间段
            3: [
                ("14:10", "14:50")    # 1
            ],
            
            # 星期五：1个时间段-临时测试
            4: [
                ("22:00", "23:00")
            ],
            
            # 星期六：1个时间段-临时测试
            5: [
                ("00:01", "23:59")
            ],
            
            # 星期日：没有课，不设置或设为空列表
            6: []
        }
        
        # 日志系统配置
        self.log_dir = Path("D:/JiaHaoToolbox/Logs")
        self.log_file = self.log_dir / f"toolbox_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        self.setup_logging()
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title(f"嘉豪工具箱（#9112） - {self.version}_{self.development_channel}")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        
        # 设置样式和初始化界面
        self.setup_styles()
        self.setup_ui()
        
        # 记录启动日志
        self.log("INFO", f"嘉豪工具箱 {self.version} 启动成功")
        self.log("INFO", f"开发者: {self.developer}")
        self.log("INFO", f"制裁模式: {'开启' if self.sanction_mode_enabled else '关闭'}")

    def setup_logging(self):
        """设置日志系统"""
        try:
            # 创建日志目录（如果不存在）
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
            # 记录日志系统初始化
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"工具箱会话开始于: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*50}\n")
                
        except Exception as e:
            # 如果日志初始化失败，在状态栏显示警告但继续运行
            self.update_status("日志系统初始化失败，但工具箱仍可运行")
            print(f"日志初始化错误: {e}")  # 作为后备输出到控制台

    def log(self, level, message, user_action=None):
        """
        记录日志
        
        参数:
            level (str): 日志级别 (INFO, WARNING, ERROR, DEBUG)
            message (str): 日志消息
            user_action (str, optional): 用户执行的操作
        """
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] [{level}] {message}"
            
            if user_action:
                log_entry += f" | 用户操作: {user_action}"
                
            # 写入日志文件
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
                
            # 如果是错误级别，同时在控制台输出（用于调试）
            if level == "ERROR":
                print(f"错误日志: {log_entry}")
                
        except Exception as e:
            # 如果日志写入失败，静默处理，避免影响主程序
            pass

    def setup_styles(self):
        """设置界面样式"""
        self.root.configure(bg='#f0f0f0')
        # 可以在这里添加更多样式设置

    def setup_ui(self):
        """设置用户界面"""
        # 标题框架
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="嘉豪工具箱 Python版-3.0\n不需要再转过去拿键盘！更好的GUI界面，即使是傻子也能快速启动……", 
            font=('微软雅黑', 10, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        version_label = tk.Label(
            title_frame,
            text=f"版本: {self.version}_{self.development_channel}",
            font=('微软雅黑', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        version_label.pack()
        
        # 主功能框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 创建各个界面部分
        self.create_function_buttons(main_frame)
        self.create_hidden_commands_section(main_frame)
        self.create_status_bar()

    def create_function_buttons(self, parent):
        """创建基础功能按钮"""
        functions_frame = tk.LabelFrame(
            parent, 
            text="基础功能", 
            font=('微软雅黑', 12, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        functions_frame.pack(fill='x', pady=(0, 10))
        
        # 按钮配置
        # 注意：这里使用带制裁检查的启动方法
        buttons = [
            ("启动白板和展台", lambda: self.start_program_with_sanction_check("00.lnk")),
            ("仅启动白板", lambda: self.start_program_with_sanction_check("01.lnk")),
            ("仅启动展台", lambda: self.start_program_with_sanction_check("02.lnk")),
            ("启动希沃白板", lambda: self.start_program_with_sanction_check("03.lnk")),
            ("版本信息", self.show_version),
            ("帮助", self.show_help)
        ]
        
        # 创建按钮并排列
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                functions_frame,
                text=text,
                command=command,
                font=('微软雅黑', 10),
                bg="#128ada",
                fg='white',
                relief='raised',
                padx=20,
                pady=10,
                width=15
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
        
        # 设置列权重，使按钮均匀分布
        functions_frame.grid_columnconfigure(0, weight=1)
        functions_frame.grid_columnconfigure(1, weight=1)

    def create_hidden_commands_section(self, parent):
        """创建控制台输入区域"""
        hidden_frame = tk.LabelFrame(
            parent,
            text="控制台",
            font=('微软雅黑', 12, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        hidden_frame.pack(fill='x', pady=(0, 10))
        
        # 命令输入标签
        tk.Label(
            hidden_frame,
            text="输入命令:                                            \n... . . -.-- --- ..- - --- -- --- .-. .-. --- .--",
            font=('微软雅黑', 10),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        # 命令输入框
        self.command_entry = tk.Entry(
            hidden_frame,
            font=('微软雅黑', 10),
            width=40
        )
        self.command_entry.pack(fill='x', pady=5)
        # 绑定回车键执行命令
        self.command_entry.bind('<Return>', self.execute_hidden_command)
        
        # 按钮框架
        btn_frame = tk.Frame(hidden_frame, bg='#f0f0f0')
        btn_frame.pack(fill='x')
        
        # 执行命令按钮
        tk.Button(
            btn_frame,
            text="执行命令",
            command=self.execute_hidden_command,
            font=('微软雅黑', 9),
            bg='#e74c3c',
            fg='white'
        ).pack(side='left', padx=(0, 5))

    def create_status_bar(self):
        """创建底部状态栏"""
        status_frame = tk.Frame(self.root, bg='#34495e', height=25)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        # 制裁模式状态指示（调试模式下才显示）
        mode_text = "制裁模式: 开启" if self.sanction_mode_enabled else "制裁模式: 关闭"
        self.mode_label = tk.Label(
            status_frame,
            text=mode_text,
            font=('微软雅黑', 8),
            fg='#2ecc71' if self.sanction_mode_enabled else '#e74c3c',
            bg='#34495e'
        )
        # 初始状态下不显示，调试模式下才显示
        if self.debug_mode:
            self.mode_label.pack(side='left', padx=5)
        
        # 状态标签
        self.status_label = tk.Label(
            status_frame,
            text="就绪",
            font=('微软雅黑', 9),
            fg='#ecf0f1',
            bg='#34495e'
        )
        self.status_label.pack(side='left', padx=10)
        
        # 查看制裁时间表按钮（调试模式下才显示）
        self.schedule_button = tk.Button(
            status_frame,
            text="查看制裁时间表",
            command=self.show_sanction_schedule,
            font=('微软雅黑', 8),
            bg='#3498db',
            fg='white',
            relief='flat'
        )
        if self.debug_mode:
            self.schedule_button.pack(side='right', padx=5, pady=2)
        
        # 切换制裁模式按钮（调试模式下才显示）
        self.toggle_button = tk.Button(
            status_frame,
            text="切换制裁模式",
            command=self.toggle_sanction_mode,
            font=('微软雅黑', 8),
            bg='#e67e22',
            fg='white',
            relief='flat'
        )
        if self.debug_mode:
            self.toggle_button.pack(side='right', padx=5, pady=2)
        
        # 退出按钮（始终显示）
        tk.Button(
            status_frame,
            text="退出",
            command=self.root.quit,
            font=('微软雅黑', 8),
            bg='#e74c3c',
            fg='white',
            relief='flat'
        ).pack(side='right', padx=10, pady=2)

    def update_status(self, message):
        """更新状态栏显示"""
        self.status_label.config(text=message)
        self.root.update()

    def is_sanction_time(self):
        """
        检查当前是否在任意一个制裁时间段内
        
        返回:
            bool: True表示当前是制裁时间，False表示非制裁时间
        """
        # 如果制裁模式未启用，直接返回False
        if not self.sanction_mode_enabled:
            return False
            
        # 获取当前时间信息
        now = datetime.datetime.now()
        current_time = now.time()
        current_weekday = now.weekday()
        
        # 检查今天是否有制裁时间段配置
        if current_weekday not in self.sanction_periods:
            return False
            
        # 检查当前时间是否在今天的任何一个制裁时间段内
        for period in self.sanction_periods[current_weekday]:
            start_time = datetime.datetime.strptime(period[0], "%H:%M").time()
            end_time = datetime.datetime.strptime(period[1], "%H:%M").time()
            
            # 如果当前时间在某个时间段内，返回True
            if start_time <= current_time <= end_time:
                return True
                
        # 不在任何制裁时间段内
        return False

    def get_current_period_info(self):
        """
        获取当前所在的时间段信息
        
        返回:
            str: 描述当前时间段的字符串
        """
        now = datetime.datetime.now()
        current_time = now.time()
        current_weekday = now.weekday()
        
        # 星期映射
        day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        
        # 检查今天是否有制裁时间段配置
        if current_weekday not in self.sanction_periods:
            return f"{day_names[current_weekday]} - 无"
            
        # 遍历今天的所有时间段，找到当前所在的时间段
        for i, period in enumerate(self.sanction_periods[current_weekday]):
            start_time = datetime.datetime.strptime(period[0], "%H:%M").time()
            end_time = datetime.datetime.strptime(period[1], "%H:%M").time()
            
            if start_time <= current_time <= end_time:
                return f"{day_names[current_weekday]} 第{i+1}个时间段 {period[0]}-{period[1]}"
                
        return f"{day_names[current_weekday]} - 课间时间"

    def start_program(self, program_path):
        """
        启动外部程序
        
        参数:
            program_path (str): 要启动的程序路径
            
        返回:
            bool: 启动成功返回True，失败返回False
        """
        try:
            if os.path.exists(program_path):
                self.log("INFO", f"启动程序: {program_path}", "程序启动")
                # 使用os.startfile启动程序（Windows系统）
                os.startfile(program_path)
                return True
            else:
                error_msg = f"文件不存在: {program_path}"
                self.log("ERROR", error_msg, "程序启动失败")
                messagebox.showerror("发生错误！", f"发生了一个意外的错误，工具箱无法执行请求的命令\n\nPython脚本宿主找到了可能的错误：Missing file:{program_path}\n错误码：1x00\n子错误码：MISSING_FILES")
                return False
        except Exception as e:
            error_msg = f"启动程序异常: {str(e)}"
            self.log("ERROR", error_msg, "程序启动异常")
            messagebox.showerror("发生错误！", f"发生了一个意外的错误，工具箱无法执行请求的命令\n\nPython脚本宿主找到了可能的错误：{str(e)}\n错误码：1x01\n子错误码：null")
            return False

    def start_program_with_sanction_check(self, program_path, is_hidden_command=False):
        """
        带制裁模式检查的启动程序方法
        
        参数:
            program_path (str): 要启动的程序路径
            is_hidden_command (bool): 是否通过隐藏命令调用，True表示绕制裁限制
            
        返回:
            bool: 启动成功返回True，失败返回False
        """
        # 如果是隐藏命令调用或者不在制裁时间，直接启动程序
        if is_hidden_command or not self.is_sanction_time():
            self.log("INFO", f"允许启动程序: {program_path}", "正常启动")
            return self.start_program(program_path)
        else:
            # 制裁时间限制，获取当前时间段信息
            current_period = self.get_current_period_info()
            
            warning_msg = f"制裁时间阻止启动: {program_path}, 当前时段: {current_period}"
            self.log("INFO/WARNING", warning_msg, "- 若要关闭制裁模式，请打开调试页面")
            
            # 显示警告信息
            messagebox.showerror(
                "发生错误！", 
                f"发生了一个意外的错误，工具箱无法执行请求的命令\n\n"
                "错误码：2xf0\n"
                "子错误码：S_MODE_HAS_BEED_ENABLED"
            )
            # 只有在调试模式下才显示详细的制裁时间信息
            if self.debug_mode:
                self.update_status(f"制裁时间 ({current_period})，按钮功能已禁用")
            else:
                self.update_status("执行命令失败")
            return False

    def toggle_sanction_mode(self):
        """切换制裁模式总开关"""
        self.sanction_mode_enabled = not self.sanction_mode_enabled
        mode_text = "制裁模式: 开启" if self.sanction_mode_enabled else "制裁模式: 关闭"
        self.mode_label.config(
            text=mode_text,
            fg='#e74c3c' if self.sanction_mode_enabled else '#2ecc71'
        )
        
        action = "开启制裁模式" if self.sanction_mode_enabled else "关闭制裁模式"
        self.log("WARNING/INFO", f"制裁模式状态变更: {action}", "模式切换")
        status = "制裁模式已开启" if self.sanction_mode_enabled else "制裁模式已关闭"
        self.update_status(status)

    def show_sanction_schedule(self):
        """显示当前制裁时间表"""
        # 星期映射
        day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        
        # 构建时间表信息
        schedule_info = "当前制裁时间表:\n\n"
        
        # 添加所有日期的时间段信息
        for day in range(7):
            if day in self.sanction_periods and self.sanction_periods[day]:
                schedule_info += f"{day_names[day]}:\n"
                for i, period in enumerate(self.sanction_periods[day]):
                    schedule_info += f"  第{i+1}次: {period[0]} - {period[1]}\n"
                schedule_info += "\n"
            else:
                schedule_info += f"{day_names[day]}: 无\n\n"
                
        schedule_info += f"总开关: {'开启' if self.sanction_mode_enabled else '关闭'}"
        
        self.log("WARNING/INFO", "用户正在查看制裁时间表", "用户操作")
        # 显示时间表
        messagebox.showinfo("制裁时间表", schedule_info)

    def toggle_debug_mode(self):
        """切换调试模式"""
        self.debug_mode = not self.debug_mode
        
        # 根据调试模式状态显示或隐藏制裁模式相关控件
        if self.debug_mode:
            # 显示制裁模式相关控件
            self.mode_label.pack(side='left', padx=5)
            self.schedule_button.pack(side='right', padx=5, pady=2)
            self.toggle_button.pack(side='right', padx=5, pady=2)
            self.log("INFO/DEBUG", "调试模式已开启", "模式切换-用户操作")
            self.update_status("调试模式已开启")
        else:
            # 隐藏制裁模式相关控件
            self.mode_label.pack_forget()
            self.schedule_button.pack_forget()
            self.toggle_button.pack_forget()
            self.log("INFO/DEBUG", "调试模式已关闭", "模式切换-用户操作")
            self.update_status("调试模式已关闭")

    def show_logs(self):
        """显示日志内容在新窗口中"""
        try:
            if not self.log_file.exists():
                messagebox.showinfo("日志查看", "今日暂无日志文件")
                return
            
            # 创建新窗口
            log_window = tk.Toplevel(self.root)
            log_window.title(f"工具箱日志查看器 - {self.log_file.name}")
            log_window.geometry("900x600")
            log_window.configure(bg='#f0f0f0')
            
            # 标题
            title_label = tk.Label(
                log_window,
                text=f"日志文件: {self.log_file}",
                font=('微软雅黑', 12, 'bold'),
                bg='#2c3e50',
                fg='white',
                pady=10
            )
            title_label.pack(fill='x', padx=10, pady=10)
            
            # 日志内容区域
            log_frame = tk.Frame(log_window, bg='#f0f0f0')
            log_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            # 滚动文本框
            text_widget = scrolledtext.ScrolledText(
                log_frame,
                wrap=tk.WORD,
                font=('Consolas', 9),
                bg='#1e1e1e',
                fg='#d4d4d4',
                insertbackground='white',
                selectbackground='#264f78'
            )
            text_widget.pack(fill='both', expand=True)
            
            # 读取并显示日志内容
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            text_widget.insert('1.0', log_content)
            text_widget.config(state='disabled')  # 设为只读
            
            # 底部按钮框架
            button_frame = tk.Frame(log_window, bg='#f0f0f0')
            button_frame.pack(fill='x', padx=10, pady=10)
            
            # 刷新按钮
            def refresh_logs():
                try:
                    with open(self.log_file, 'r', encoding='utf-8') as f:
                        new_content = f.read()
                    text_widget.config(state='normal')
                    text_widget.delete('1.0', tk.END)
                    text_widget.insert('1.0', new_content)
                    text_widget.config(state='disabled')
                    text_widget.see(tk.END)  # 滚动到底部
                except Exception as e:
                    messagebox.showerror("错误", f"刷新日志失败: {str(e)}")
            
            refresh_btn = tk.Button(
                button_frame,
                text="刷新日志",
                command=refresh_logs,
                font=('微软雅黑', 9),
                bg='#3498db',
                fg='white'
            )
            refresh_btn.pack(side='left', padx=5)
            
            # 清空日志按钮
            def clear_logs():
                if messagebox.askyesno("确认", "确定要清空今日日志吗？"):
                    try:
                        with open(self.log_file, 'w', encoding='utf-8') as f:
                            f.write(f"日志清空于: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        refresh_logs()
                        self.log("INFO", "日志文件已被清空", "用户操作")
                    except Exception as e:
                        messagebox.showerror("错误", f"清空日志失败: {str(e)}")
            
            clear_btn = tk.Button(
                button_frame,
                text="清空日志",
                command=clear_logs,
                font=('微软雅黑', 9),
                bg='#e74c3c',
                fg='white'
            )
            clear_btn.pack(side='left', padx=5)
            
            # 关闭按钮
            close_btn = tk.Button(
                button_frame,
                text="关闭",
                command=log_window.destroy,
                font=('微软雅黑', 9),
                bg='#95a5a6',
                fg='white'
            )
            close_btn.pack(side='right', padx=5)
            
            # 自动滚动到底部
            text_widget.see(tk.END)
            
            self.log("INFO", "用户正在查看日志文件", "用户操作")
            
        except Exception as e:
            error_msg = f"打开日志窗口失败: {str(e)}"
            self.log("ERROR", error_msg, "系统错误")
            messagebox.showerror("错误", f"无法显示日志: {str(e)}")

    # === 基础功能方法 ===
    
    def show_version(self):
        """显示版本信息"""
        version_info = f"""版本号：{self.version}
开发者：{self.developer}
最后更新：{self.last_update}
作者个人bilibili主页：{self.bilibili_space}
频道：{self.development_channel}

如果需要打开作者的个人主页，请输入命令：space"""
        self.log("INFO", "用户正在查看版本信息", "用户操作")
        messagebox.showinfo("版本信息", version_info)

    def show_help(self):
        """显示帮助信息"""
        help_info = """嘉豪工具箱 - 部分功能说明：
debug - 调试模式
ver - 版本信息
help - 显示此帮助"""
        self.log("INFO/WARNING", "用户正在查看帮助信息", "用户操作")
        messagebox.showinfo("帮助信息", help_info)

    # === 隐藏命令处理 ===
    
    def execute_hidden_command(self, event=None):
        """
        执行隐藏命令
        
        参数:
            event: 事件对象（用于回车键绑定）
        """
        # 获取输入的命令并清除输入框
        command = self.command_entry.get().strip().lower()
        self.command_entry.delete(0, tk.END)
        
        # 空命令直接返回
        if not command:
            return
            
        # 记录命令执行
        self.log("INFO", f"执行命令: {command}", "控制台命令")
            
        # 命令映射表
        # 格式: '命令名称': 对应的函数
        command_map = {
            # 基础命令
            '91': self.start_dike,
            'debug': self.toggle_debug_mode,  # 改为切换调试模式
            'ver': self.show_version,
            'help': self.show_help,
            'huaqiang': self.huaqiang_buy_watermelon,
            'alan': self.alan_whatsup,
            'sr': self.star_rail,
            '饿啊': self.on_my_way,
            '昔涟': self.ripples_of_past_reverie,
            'command': self.show_command_list,
            'hajimi': self.hajimi,
            'space': self.open_space,
            'showwelcomemenu': lambda: messagebox.showinfo("菜单", "欢迎使用嘉豪工具箱！"),
            'jiahao666': self.jiahao_666,
            'galagame':self.senren_banka, #嘎啦给木里不是这样的！
            'xinjianya': self.jay_chou,
            'lixiaolong': self.li_xiaolong,
            'jiangjieshi':self.chiang_kai_shek,
            'luoziyu': self.luo_zi_yu,
            'eggy': self.yuan_meng_fei,
            'bomb':self.t_win,
            'yihetuan':self.boxer_rebellion,
            'showlog': self.show_logs,  # 新增日志查看命令
            
            # 制裁刘老师绕过命令
            'bypass_start_all': lambda: self.start_program_with_sanction_check("00.lnk", True),
            'bypass_whiteboard': lambda: self.start_program_with_sanction_check("01.lnk", True),
            'bypass_painter': lambda: self.start_program_with_sanction_check("02.lnk", True),
            'bypass_seewo': lambda: self.start_program_with_sanction_check("03.lnk", True),
            
            # 制裁时间表命令（调试模式下才有效）
            'schedule': lambda: self.show_sanction_schedule() if self.debug_mode else messagebox.showerror("发生错误！", "发生了一个意外的错误，工具箱无法执行请求的命令\n错误码：2xf1\n子错误码：INSUFFCIENT_PERMISSIONS"),
            
            # 摩尔斯电码彩蛋
            '... . . -.-- --- ..- - --- -- --- .-. .-. --- .--': self.see_you_tomorrow
        }
        
        # 执行对应的命令
        if command in command_map:
            self.update_status(f"执行命令: {command}")
            command_map[command]()
        else:
            error_msg = f"未知命令: {command}"
            self.log("INFO/ERROR", error_msg, "- 用户输入了无效的命令")
            messagebox.showerror("无效的命令", f"无效的命令: {command}\n请检查输入是否正确\n错误码：0x01\n子错误码：UNKNOWN_COMMAND")
            self.update_status("就绪")

    def show_command_list(self):
        """显示隐藏命令列表"""
        commands = """隐藏命令列表:

=== 基础命令 ===
sr - 打开视频：何 意 味 ？
91 - 打开视频：低调的黑客有多恐怖😱
alan - 打开视频：𝘼𝙡𝙖𝙣 𝙒𝙝𝙖𝙩'𝙨 𝙪𝙥 
huaqiang - 打开视频：⚡⚡石家庄电音节⚡⚡
饿啊 - 打开视频：⚡饿 My Way⚡
昔涟 - 打开视频：《崩坏：星穹铁道》动画短片：「你好，世界」
hajimi - 哈基迷单曲《昔涟》
lixiaolong - 打开音乐MV：周杰伦 - 《双截棍》
xinjianya - 打开音乐MV：周杰伦 - 《以父之名》
eggy - 打开视频：目击！笑奋31世
galagame - 打开视频：🍉千恋万瓜🍉
jiahao666 - 打开视频：666嘉豪这期在教学楼摸到专武了 秒开仙豪模式
space - 作者B站主页
luoziyu - 罗子瑜看到没被做进工具箱就受着呗
yihetuan - （666英语考了128怎么办 打开视频：[油管搬运]五十五天在北京丨义和团版(原作者重新制作)
bomb - 打开视频：大一小伙带霰弹枪和手搓C4炸弹上学，10分钟\n20杀70伤，教学楼炸成废墟，出勤特警差点团灭！\n
showlog - 查看工具箱日志
... . . -.-- --- ..- - --- -- --- .-. .-. --- .-- | See you tomorrow.

=== 系统命令 ===
debug - 切换调试模式（显示/隐藏制裁模式相关功能）
command - 显示此命令列表

=== 调试模式专属命令 ===
schedule - 查看制裁时间表（仅在调试模式下可用）

=== 绕过制裁刘老师模式命令 ===
bypass_start_all - 绕过限制启动白板+展台
bypass_whiteboard - 绕过限制启动白板
bypass_painter - 绕过限制启动展台
bypass_seewo - 绕过限制启动希沃白板"""
        self.log("WARNING/INFO", "执行命令:command", "用户操作")
        messagebox.showinfo("隐藏命令列表", commands)

    # === 隐藏命令具体实现 ===
    
    def start_dike(self):
        """低调的黑客有多恐怖😱"""
        self.log("INFO", "执行命令:91", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1C3HJzAETE")

    def huaqiang_buy_watermelon(self):
        """⚡⚡石家庄电音节⚡⚡"""
        self.log("INFO", "执行命令:huaqiang", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1u34y1D7v6")

    def alan_whatsup(self):
        """𝘼𝙡𝙖𝙣 𝙒𝙝𝙖𝙩'𝙨 𝙪𝙥"""
        self.log("INFO", "执行命令:alan", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1Zb4y127U4")

    def star_rail(self):
        """何 意 味 ？"""
        self.log("INFO", "执行命令:sr", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1hE2FBPE56/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=1")

    def on_my_way(self):
        """⚡饿 My Way⚡"""
        self.log("INFO", "执行命令:饿啊", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1ZBYnzXEgn")

    def ripples_of_past_reverie(self):
        """《崩坏：星穹铁道》动画短片：「你好，世界」"""
        self.log("INFO", "执行命令:昔涟", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV14G1kB5Evp/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=1")

    def hajimi(self):
        """哈基迷单曲《昔涟》"""
        self.log("INFO", "执行命令:hajimi", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1oCCeBAEC5/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=1")

    def open_space(self):
        """B站主页"""
        self.log("INFO", "打开B站主页", "用户操作")
        webbrowser.open(self.bilibili_space)

    def jiahao_666(self):
        """666嘉豪这期在教学楼摸到专武了 秒开仙豪模式"""
        self.log("INFO", "执行命令:jiahao666", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1t1pjzKEtE/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=1")

    def jay_chou(self):
        """周杰伦《以父之名》 by 5ph"""
        self.log("INFO", "执行命令:xinjianya", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1JK4y1u7KH/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=1")

    def li_xiaolong(self):
        """周杰伦《双截棍》"""
        self.log("INFO", "执行命令:lixiaolong", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1ht411J7c6/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=71")

    def yuan_meng_fei(self):
        """目击！笑奋31世"""
        self.log("INFO", "执行命令:eggy", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1UjCCBkEeo/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=1")

    def see_you_tomorrow(self):
        """See you tomorrow."""
        self.log("INFO", "执行命令:... . . -.-- --- ..- - --- -- --- .-. .-. --- .--", "用户操作")
        messagebox.showinfo("Star Rail", "See you tomorrow.")
        webbrowser.open("https://www.bilibili.com/opus/1131624617264283668")

    def luo_zi_yu(self):
        """S Blzy"""
        self.log("INFO", "执行命令：luoziyu", "用户操作")
        messagebox.showinfo("罗子瑜你看到没", "我还真把你做进工具箱里了")

    def chiang_kai_shek(self):
        """东南苦行山"""  #来自中原一群伙伴，结庐东南山…… #反对台独！台湾是中国不可分割的领土！
        self.log("INFO", "执行命令: ", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1MNy3BREsm/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=10")

    def senren_banka(self):
        """嘎啦给木里根本不是这样！"""
        self.log("INFO", "执行命令: galagame", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV13H4y1w7cK/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=1")
    
    def boxer_rebellion(self):
        """英语128分申请加入义和团"""
        self.log("INFO", "执行命令: yihetuan", "用户操作")
        messagebox.showinfo("英语128分怎么办","快滚去东交民巷吧")
        webbrowser.open("https://www.bilibili.com/video/BV1RV4y117BZ/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=8")
    
    def t_win(self):
        """666T阵营胜利""" #A college freshman brought a shotgun and a handmade C4 bomb to school, causing 20 kills and 70 injuries in 10 minutes. The teaching building was reduced to ruins, and the responding SWAT team was almost wiped out!
        self.log("INFO", "执行命令:bomb", "用户操作")
        webbrowser.open("https://www.bilibili.com/video/BV1z4USBZEcC/?share_source=copy_web&vd_source=4590346da3389db422656b1040e948b7&t=1")

    def run(self):
        """运行应用程序"""
        try:
            self.root.mainloop()
        except Exception as e:
            error_msg = f"主循环异常: {str(e)}"
            self.log("ERROR", error_msg, "系统错误")
            messagebox.showerror("发生错误！", f"发生了一个意外的错误，工具箱无法运行。\nPython脚本宿主找到了可能的错误： {str(e)} \n错误码：0x00\n子错误码：STARTUP_FAILED")
        finally:
            # 程序退出时记录
            self.log("INFO", "嘉豪工具箱正常退出")

# 程序入口
if __name__ == "__main__":
    try:
        # 创建工具箱实例并运行
        toolbox = JiahaoToolbox()
        toolbox.run()
    except Exception as e:
        # 捕获并显示启动错误
        messagebox.showerror("发生错误！", f"发生了一个意外的错误，工具箱无法运行。\nPython脚本宿主找到了可能的错误： {str(e)} \n错误码：0x00\n子错误码：STARTUP_FAILED")