import cv2
import numpy as np
from gtts import gTTS
import os
import time

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 颜色范围（示例，可根据实际情况调整）
color_ranges = {
    'red': ([0, 120, 70], [10, 255, 255]),
    'green': ([35, 120, 70], [85, 255, 255]),
    'blue': ([100, 120, 70], [130, 255, 255]),
    'yellow': ([20, 120, 70], [30, 255, 255])
}


def detect_colors(frame):
    detected_colors = []
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            detected_colors.append(color)
    return detected_colors


def speak_result(result):
    tts = gTTS(text=result, lang='ko')
    tts.save("result.mp3")
    os.system("mpg321 result.mp3")
    os.remove("result.mp3")


while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Camera Feed', frame)

    key = cv2.waitKey(1)
    if key == ord(' '):  # 按空格键表示投掷完成
        colors = detect_colors(frame)
        result = f"검출된 색상: {', '.join(colors)}"
        print(result)
        speak_result(result)

    if key == ord('q'):  # 按 'q' 键退出
        break

cap.release()
cv2.destroyAllWindows()
    