import tkinter as tk
from detection_module import start_detection


def exit_program():
    root.destroy()


# 创建主窗口
root = tk.Tk()
root.title("欢迎来到윷놀이/尤茨游戏/掷柶游戏")

# 创建标签
label = tk.Label(root, text="欢迎来到윷놀이/尤茨游戏/掷柶游戏", font=("Arial", 20))
label.pack(pady=20)

# 创建开始投掷按钮
start_button = tk.Button(root, text="开始投掷", command=start_detection, font=("Arial", 16))
start_button.pack(pady=10)

# 创建退出程序按钮
exit_button = tk.Button(root, text="退出程序", command=exit_program, font=("Arial", 16))
exit_button.pack(pady=10)

# 运行主循环
root.mainloop()
