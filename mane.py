import customtkinter as ctk
from tkinter import messagebox, colorchooser, simpledialog
import time
import random
import json
import os
import psutil  # 用于获取系统信息
import requests  # 用于获取天气信息（需要安装requests模块）


class DesktopWidget:
    def __init__(self, root, master, config=None):
        self.root = root
        self.master = master  # 主界面引用
        self.root.title("桌面组件")
        self.root.geometry("300x200")  # 设置窗口大小
        self.root.attributes("-topmost", True)  # 使窗口始终在最上层
        self.root.overrideredirect(True)  # 去掉窗口边框
        self.root.attributes("-alpha", 1.0)  # 初始透明度为完全不透明

        # 初始化功能模式
        self.display_mode = config.get("display_mode", "time") if config else "time"
        self.note_text = config.get("note_text", "") if config else ""  # 笔记内容
        self.countdown_seconds = config.get("countdown_seconds", 0) if config else 0  # 倒计时秒数
        self.quotes = [
            "生活就像一盒巧克力，你永远不知道下一颗是什么味道。",
            "成功是跌倒九次，爬起来十次。",
            "今天的努力是为了明天的自由。",
            "test",
            "11111222",
        ]  # 随机名言列表
        self.reminders = config.get("reminders", []) if config else []  # 任务提醒列表

        # 设置窗口背景颜色
        self.root.configure(bg="#2b2b2b")

        # 添加标签
        self.label = ctk.CTkLabel(root, text="这是一个桌面组件", font=("Arial", 12))
        self.label.pack(pady=10)

        # 添加按钮
        self.button = ctk.CTkButton(root, text="切换功能", command=self.toggle_display)
        self.button.pack(pady=5)

        # 添加笔记输入框
        self.note_entry = ctk.CTkEntry(root)
        self.note_entry.pack(pady=5)

        # 添加保存笔记按钮
        self.save_note_button = ctk.CTkButton(root, text="保存笔记", command=self.save_note)
        self.save_note_button.pack(pady=5)

        # 添加设置倒计时按钮
        self.set_countdown_button = ctk.CTkButton(root, text="设置倒计时", command=self.set_countdown)
        self.set_countdown_button.pack(pady=5)

        # 添加任务提醒按钮
        self.add_reminder_button = ctk.CTkButton(root, text="添加任务提醒", command=self.add_reminder)
        self.add_reminder_button.pack(pady=5)

        # 绑定鼠标事件以实现拖拽
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.on_motion)

        # 绑定鼠标右键事件以实现透明度切换
        self.root.bind("<Button-3>", self.toggle_transparency)  # 右键点击

        self._offsetx = 0
        self._offsety = 0

        # 开始更新显示
        self.update_display()

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def stop_move(self, event):
        self._offsetx = 0
        self._offsety = 0

    def on_motion(self, event):
        x = self.root.winfo_x() + (event.x - self._offsetx)
        y = self.root.winfo_y() + (event.y - self._offsety)
        self.root.geometry(f"+{x}+{y}")

    def toggle_transparency(self, event):
        """右键点击时切换窗口透明度和鼠标穿透"""
        current_alpha = self.root.attributes("-alpha")
        if current_alpha == 1.0:
            self.root.attributes("-alpha", 0.5)  # 设置为半透明
            self.root.attributes("-transparentcolor", "#2b2b2b")  # 启用鼠标穿透
        else:
            self.root.attributes("-alpha", 1.0)  # 恢复为完全不透明
            self.root.attributes("-transparentcolor", "")  # 禁用鼠标穿透

    def toggle_display(self):
        """切换功能模式"""
        modes = [
            "time",  # 时间
            "calendar",  # 日历
            "note",  # 笔记
            "countdown",  # 倒计时
            "quote",  # 随机名言
            "reminder",  # 任务提醒
        ]
        current_index = modes.index(self.display_mode)
        next_index = (current_index + 1) % len(modes)
        self.display_mode = modes[next_index]
        self.update_display()

    def update_display(self):
        """更新显示内容"""
        if self.display_mode == "time":
            current_time = time.strftime("%H:%M:%S")  # 获取当前时间
            self.label.configure(text=f"当前时间: {current_time}")
        elif self.display_mode == "calendar":
            current_date = time.strftime("%Y-%m-%d")  # 获取当前日期
            self.label.configure(text=f"当前日期: {current_date}")
        elif self.display_mode == "note":
            self.label.configure(text=f"笔记内容:\n{self.note_text}")
        elif self.display_mode == "countdown":
            self.label.configure(text=f"倒计时: {self.countdown_seconds}秒")
            if self.countdown_seconds > 0:
                self.countdown_seconds -= 1
        elif self.display_mode == "quote":
            random_quote = random.choice(self.quotes)  # 随机选择名言
            self.label.configure(text=f"随机名言:\n{random_quote}")
        elif self.display_mode == "reminder":
            reminders_text = "\n".join(self.reminders)
            self.label.configure(text=f"任务提醒:\n{reminders_text}")

        # 每隔1秒更新一次显示
        self.root.after(1000, self.update_display)

    def save_note(self):
        """保存笔记"""
        self.note_text = self.note_entry.get()
        messagebox.showinfo("提示", "笔记已保存！")

    def set_countdown(self):
        """设置倒计时"""
        seconds = simpledialog.askinteger("设置倒计时", "请输入倒计时秒数：", minvalue=1, maxvalue=3600)
        if seconds:
            self.countdown_seconds = seconds

    def add_reminder(self):
        """添加任务提醒"""
        reminder = simpledialog.askstring("添加任务提醒", "请输入任务内容：")
        if reminder:
            self.reminders.append(reminder)
            self.update_display()

    def show_system_info(self):
        """显示系统信息"""
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        messagebox.showinfo("系统信息", f"CPU使用率: {cpu_usage}%\n内存使用: {memory_info.percent}%")

    def get_weather_info(self):
        """获取天气信息"""
        api_key = "你的API密钥"  # 替换为有效的API密钥
        city = simpledialog.askstring("输入城市", "请输入城市名称：")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temperature = data['main']['temp']
                weather_description = data['weather'][0]['description']
                messagebox.showinfo("天气信息", f"{city} 的温度为: {temperature}°C\n天气情况: {weather_description}")
            else:
                messagebox.showerror("错误", "无法获取天气信息，请检查城市名称。")

    def start_timer(self):
        """开始计时器"""
        self.timer_running = True

    def stop_timer(self):
        """停止计时器"""
        self.timer_running = False

    def destroy(self):
        """销毁组件"""
        self.root.destroy()
        self.master.remove_widget(self)  # 通知主界面移除该组件

    def get_config(self):
        """获取组件配置"""
        return {
            "display_mode": self.display_mode,
            "note_text": self.note_text,
            "countdown_seconds": self.countdown_seconds,
            "reminders": self.reminders,
        }


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("主界面")
        self.root.geometry("800x600")  # 调整主界面大小

        # 存储所有桌面组件
        self.widgets = []

        # 创建主界面布局
        self.create_ui()

        # 加载保存的组件状态
        self.load_widgets()

        # 保存组件状态
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        """创建主界面 UI"""
        # 顶部标题栏
        title_label = ctk.CTkLabel(self.root, text="桌面组件管理器", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # 主内容区域
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # 左侧组件列表
        self.widget_listbox = ctk.CTkTextbox(main_frame, font=("Arial", 12), wrap=ctk.NONE, state="disabled")
        self.widget_listbox.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0, 10))

        # 右侧功能按钮区域
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(side=ctk.RIGHT, fill=ctk.Y)

        # 添加功能按钮
        buttons = [
            ("创建新组件", self.create_widget),
            ("销毁选中组件", self.destroy_selected_widget),
            ("清空所有组件", self.clear_all_widgets),
            ("保存所有组件状态", self.save_all_widgets),
            ("加载所有组件状态", self.load_all_widgets),
            ("显示当前时间", self.show_current_time),
            ("显示随机名言", self.show_random_quote),
            ("显示任务提醒", self.show_reminders),
            ("退出程序", self.root.destroy),
        ]

        for text, command in buttons:
            button = ctk.CTkButton(button_frame, text=text, command=command)
            button.pack(fill=ctk.X, pady=5)

        # 底部状态栏
        self.status_label = ctk.CTkLabel(self.root, text="就绪", anchor=ctk.W)
        self.status_label.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=10)

        # 更新状态栏时间
        self.update_status_bar()

    def update_status_bar(self):
        """更新状态栏时间"""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.status_label.configure(text=f"当前时间: {current_time}")
        self.root.after(1000, self.update_status_bar)

    def create_widget(self):
        """创建新的桌面组件"""
        widget_root = ctk.CTkToplevel()  # 创建一个新的顶级窗口
        widget = DesktopWidget(widget_root, self)  # 创建桌面组件
        self.widgets.append(widget)  # 添加到组件列表
        self.update_widget_list()  # 更新组件列表显示

    def destroy_selected_widget(self):
        """销毁选中的组件"""
        try:
            # 获取当前选中的行号（从 1 开始）
            selected_line = self.widget_listbox.index(ctk.INSERT).split(".")[0]
            selected_index = int(selected_line) - 1  # 转换为列表索引（从 0 开始）

            if 0 <= selected_index < len(self.widgets):
                widget = self.widgets[selected_index]  # 获取选中的组件
                widget.destroy()  # 销毁组件
            else:
                messagebox.showwarning("警告", "未选中有效的组件！")
        except Exception as e:
            messagebox.showerror("错误", f"销毁组件时发生错误: {e}")

    def clear_all_widgets(self):
        """清空所有组件"""
        for widget in self.widgets:
            widget.destroy()  # 销毁所有组件
        self.widgets.clear()  # 清空组件列表
        self.update_widget_list()  # 更新组件列表显示

    def save_all_widgets(self):
        """保存所有组件状态"""
        configs = [widget.get_config() for widget in self.widgets]
        with open("widgets_config.json", "w") as f:
            json.dump(configs, f)
        messagebox.showinfo("提示", "所有组件状态已保存！")

    def load_all_widgets(self):
        """加载所有组件状态"""
        if os.path.exists("widgets_config.json"):
            with open("widgets_config.json", "r") as f:
                configs = json.load(f)
            for config in configs:
                widget_root = ctk.CTkToplevel()
                widget = DesktopWidget(widget_root, self, config)
                self.widgets.append(widget)
            self.update_widget_list()
            messagebox.showinfo("提示", "所有组件状态已加载！")
        else:
            messagebox.showwarning("警告", "未找到保存的组件状态文件！")

    def show_current_time(self):
        """显示当前时间"""
        current_time = time.strftime("%H:%M:%S")
        messagebox.showinfo("当前时间", f"当前时间: {current_time}")

    def show_random_quote(self):
        """显示随机名言"""
        quotes = [
            "生活就像一盒巧克力，你永远不知道下一颗是什么味道。",
            "成功是跌倒九次，爬起来十次。",
            "今天的努力是为了明天的自由。",
        ]
        random_quote = random.choice(quotes)
        messagebox.showinfo("随机名言", random_quote)

    def show_reminders(self):
        """显示任务提醒"""
        reminders = []
        for widget in self.widgets:
            reminders.extend(widget.reminders)
        if reminders:
            reminders_text = "\n".join(reminders)
            messagebox.showinfo("任务提醒", reminders_text)
        else:
            messagebox.showinfo("任务提醒", "没有任务提醒。")

    def remove_widget(self, widget):
        """从列表中移除组件"""
        if widget in self.widgets:
            self.widgets.remove(widget)  # 从列表中移除
            self.update_widget_list()  # 更新组件列表显示

    def update_widget_list(self):
        """更新组件列表显示"""
        self.widget_listbox.configure(state="normal")  # 临时启用编辑
        self.widget_listbox.delete("1.0", ctk.END)  # 清空列表
        for i, widget in enumerate(self.widgets):
            self.widget_listbox.insert(ctk.END, f"组件 {i + 1}\n")  # 添加组件到列表
        self.widget_listbox.configure(state="disabled")  # 恢复为只读模式

    def on_close(self):
        """关闭主界面时保存组件状态"""
        configs = [widget.get_config() for widget in self.widgets]
        with open("widgets_config.json", "w") as f:
            json.dump(configs, f)
        self.root.destroy()

    def load_widgets(self):
        """加载保存的组件状态"""
        if os.path.exists("widgets_config.json"):
            with open("widgets_config.json", "r") as f:
                configs = json.load(f)
            for config in configs:
                widget_root = ctk.CTkToplevel()  # 使用customtkinter创建窗口
                widget = DesktopWidget(widget_root, self, config)
                self.widgets.append(widget)  # 添加加载的组件
            self.update_widget_list()


if __name__ == "__main__":
    root = ctk.CTk()  # 使用customtkinter的主窗口
    app = MainApp(root)  # 初始化主应用
    root.mainloop()  # 运行应用
