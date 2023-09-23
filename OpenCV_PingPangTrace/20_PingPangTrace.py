import cv2
import numpy as np
import math

def draw_mark_X(img, x, y, width=6, color=(0, 0, 255), penWid=2):
    cv2.line(img, (int(x - width), int(y - width)), (int(x + width), int(y + width)), color, penWid)
    cv2.line(img, (int(x - width), int(y + width)), (int(x + width), int(y - width)), color, penWid)

# 使用测试视频
video_path = './PingPangPics/PingPangMove2.mp4'
# video_path = 0   # 使用本机摄像头
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
while cap.isOpened():
    ret, frame = cap.read()

    if ret == False:
        break
    # 设置HSV跟踪颜色范围
    min_pipa_hsv = np.array([5, 95, 145])
    max_pipa_hsv = np.array([25, 255, 255])
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 提取颜色范围内图像区域
    PingPangMask = cv2.inRange(img_hsv, min_pipa_hsv, max_pipa_hsv)
    img_pipa = cv2.bitwise_and(frame, frame, mask=PingPangMask)

    # 二值化
    kernel = np.ones((6, 6), np.uint8)
    img_kai = cv2.morphologyEx(img_pipa, cv2.MORPH_OPEN, kernel)
    # img_kai_gray = cv2.cvtColor(img_kai, cv2.COLOR_HSV)
    img_kai_chv = img_kai[:, :, 2]
    thr, img_bin = cv2.threshold(img_kai_chv, 63, 255, cv2.THRESH_BINARY)
    print('thr:', thr)
    #  提取轮廓
    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) < 1:
        continue
    # There should be at least 5 points to fit the ellipse
    if len(contours[0]) < 8:
        continue

    print('len(contours):', len(contours))
    print('Points', len(contours[0]))
    # print('contours:', contours)
    print('hierarchy', hierarchy)
    # 画绿色轮廓线
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    #  画红色轮廓最小外接圆
    (x, y), radius = cv2.minEnclosingCircle(contours[0])
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(frame, center, radius, (0, 0, 255), 1)
    draw_mark_X(frame, int(x), int(y))

    #  画白色最优拟合椭圆
    ellipse = cv2.fitEllipse(contours[0])  # 最优拟合椭圆
    cv2.ellipse(frame, ellipse, (255, 255, 255), 1)

    #  计算最小外接圆面积
    area = math.pi * radius * radius

    #  显示圆心X Y 坐标，半径 R， 和 圆面积
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_info = 'X:' + str(x * 10 // 1 / 10) + '  Y:' + str(y * 10 // 1 / 10)
    cv2.putText(frame, text_info, (10, 30), font, 1, (0, 255, 0), 1)
    text_info = 'R:' + str(radius * 10 // 1 / 10) + "    Area:" + str(area * 100 // 1 / 100)
    cv2.putText(frame, text_info, (10, 60), font, 1, (0, 255, 0), 1)

    #  显示图像帧
    cv2.imshow('PingPangTrace', frame)
    c = cv2.waitKey(int(1000 / fps))
    # c = cv2.waitKey(200)
    #  按ESC键退出
    if c == 27:  # ESC
        break
cap.release()
cv2.destroyAllWindows()
print('Exit video read.')
