import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import threading
from detection_module import start_detection, play_sound

# 全局变量
cap = None
root = None
frame = None
detection_thread = None

# 定义界面场景一
def scene_one():
    global root
    root = tk.Tk()
    root.title("欢迎来到윷놀이/尤茨游戏/掷柶游戏")

    # 加载图片（请替换为实际图片路径）
    try:
        img = Image.open("./img/welcome.png")
        img = img.resize((400, 300))
        photo = ImageTk.PhotoImage(img)
        label_img = tk.Label(root, image=photo)
        label_img.image = photo
        label_img.pack(pady=20)
    except FileNotFoundError:
        messagebox.showerror("错误", "未找到图片文件")

    # 创建开始游戏按钮
    start_button = tk.Button(root, text="开始游戏", command=lambda: switch_to_scene_two(), font=("Arial", 16))
    start_button.pack(pady=10)

    # 创建退出程序按钮
    exit_button = tk.Button(root, text="退出程序", command=root.destroy, font=("Arial", 16))
    exit_button.pack(pady=10)

    root.mainloop()

# 切换到界面场景二
def switch_to_scene_two():
    global root, cap, frame, detection_thread
    root.destroy()
    root = tk.Tk()
    root.title("游戏进行中")

    # 打开摄像头
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # 创建左侧摄像头画面显示区域
    frame = tk.Label(root)
    frame.pack(side=tk.LEFT, padx=10, pady=10)

    # 创建右侧按钮区域
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # 创建重置按钮
    reset_button = tk.Button(button_frame, text="重置", command=reset_program, font=("Arial", 16))
    reset_button.pack(pady=10)

    # 创建退出按钮
    exit_button = tk.Button(button_frame, text="退出", command=lambda: switch_back_to_scene_one(), font=("Arial", 16))
    exit_button.pack(pady=10)

    # 启动检测线程
    detection_thread = threading.Thread(target=start_detection)
    detection_thread.start()

    # 开始更新摄像头画面
    update_frame()

    root.mainloop()

# 更新摄像头画面
def update_frame():
    global cap, frame
    ret, img = cap.read()
    if ret:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        frame.config(image=img)
        frame.image = img
    frame.after(10, update_frame)

# 重置程序
def reset_program():
    global cap, detection_thread
    if cap:
        cap.release()
    if detection_thread and detection_thread.is_alive():
        detection_thread.join()
    switch_to_scene_two()

# 切换回界面场景一
def switch_back_to_scene_one():
    global cap, root, detection_thread
    if cap:
        cap.release()
    if detection_thread and detection_thread.is_alive():
        detection_thread.join()
    root.destroy()
    scene_one()

if __name__ == "__main__":
    scene_one()