import cv2
import numpy as np
from tkinter import messagebox
from playsound import playsound
import threading

# 缩小红色的定义范围
red_lower = np.array([0, 150, 150])
red_upper = np.array([10, 255, 255])
red_lower2 = np.array([160, 150, 150])
red_upper2 = np.array([180, 255, 255])

# 缩小蓝色的定义范围
blue_lower = np.array([200, 30, 55])
blue_upper = np.array([240, 50, 75])

# 调试开关
DEBUG = True
# 最小区域面积阈值，可根据实际情况调整
MIN_AREA_THRESHOLD = 500


def play_sound(sound_file):
    try:
        playsound(sound_file)
    except Exception as e:
        print(f"播放声音时出错: {e}")


def start_detection():
    # 打开摄像头，指定使用DirectShow后端
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 转换为HSV颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 创建红色和蓝色的掩码
        mask_red1 = cv2.inRange(hsv, red_lower, red_upper)
        mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)

        # 查找红色和蓝色区域的轮廓
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 过滤掉小的轮廓
        red_contours_filtered = [cnt for cnt in contours_red if cv2.contourArea(cnt) > MIN_AREA_THRESHOLD]
        blue_contours_filtered = [cnt for cnt in contours_blue if cv2.contourArea(cnt) > MIN_AREA_THRESHOLD]

        # 计算红色和蓝色区域的数量
        red_dice = len(red_contours_filtered)
        blue_dice = len(blue_contours_filtered)

        # 根据结果显示信息
        result_text = ""
        sound_file = ""
        if red_dice == 1 and blue_dice == 3:
            result_text = "结果为“猪”，移动1步"
            sound_file = "sound/1.MP3"
        elif red_dice == 2 and blue_dice == 2:
            result_text = "结果为“狗”，移动2步"
            sound_file = "sound/2.MP3"
        elif red_dice == 3 and blue_dice == 1:
            result_text = "结果为“羊”，移动3步"
            sound_file = "sound/3.MP3"
        elif red_dice == 4 and blue_dice == 0:
            result_text = "结果为“牛”，移动4步，并奖励一次投掷"
            sound_file = "sound/4.MP3"
        elif red_dice == 0 and blue_dice == 4:
            result_text = "结果为“马”，移动5步，并奖励一次投掷"
            sound_file = "sound/5.MP3"

        if result_text:
            # 创建一个线程来播放声音
            sound_thread = threading.Thread(target=play_sound, args=(sound_file,))
            sound_thread.start()
            # 弹出弹窗显示结果
            messagebox.showinfo("检测结果", result_text)

        # 调试模式下显示轮廓
        if DEBUG:
            cv2.drawContours(frame, red_contours_filtered, -1, (0, 0, 255), 2)
            cv2.drawContours(frame, blue_contours_filtered, -1, (255, 0, 0), 2)

        # 显示图像
        cv2.imshow('Dice Result', frame)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()
