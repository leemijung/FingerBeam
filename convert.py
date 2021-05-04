''''#이미지로 저장
import os
file_list = os.listdir("./source/")
from pdf2image import convert_from_path
for file_name in file_list:
    pages = convert_from_path("./source/" + file_name)
    for i, page in enumerate(pages):
        page.save("./img/"+str(i), "GIF")

#이미지를 파일로 저장
from PIL import Image
import os
path=input("Path of image files: ")
ConvertedtoPdfPath=input("path of pdf: ")
file_list=os.listdir(path)
img_list=[]
k=0
for i in file_list:
    print(i)
    print("진행상황: "+str(k)+'/'+str(len(file_list)))
    img=Image.open(path+"\\"+str(i))
    img_1=img.convert('RGB')
    img_list.append(img_1)
    k += 1
img_1.save(ConvertedtoPdfPath+'\\ConvertedToPdf.pdf',save_all=True,append_images=img_list)
print("완료")
'''
'''import cv2 as cv
import turtle as t
import os.path
#이미지로 저장
import os
file_list = os.listdir("./source/")
from pdf2image import convert_from_path
for file_name in file_list:
    pages = convert_from_path("./source/" + file_name)
    for i, page in enumerate(pages):
        page.save("./img/"+str(i), "GIF")

def draw_ball_location(img_color, locations):
    for i in range(len(locations) - 1):

        if locations[0] is None or locations[1] is None:
            continue

        cv.line(img_color, tuple(locations[i]), tuple(locations[i + 1]), (0, 255, 255), 3)

    return img_color


cap = cv.VideoCapture(0)

list_ball_location = []
history_ball_locations = []
isDraw = True

win = t.Screen()
win.setup(640,480)
t1 = t.Turtle()
t1.shape('circle')
t1.ht()
t1.penup()
t1.color('blue')
t1.shapesize(3)
t1.speed(0)
win.onkey(t.bye, 'q')
win.listen()

win.bgpic("./img/0")
file=0
win.update()

while True:

    ret, img_color = cap.read()

    img_color = cv.flip(img_color, 1) # 영상의 좌우 반전

    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    hue_red = 5
    lower_red = (hue_red - 5, 200, 180)
    upper_red= (hue_red + 5, 255, 255)
    img_mask = cv.inRange(img_hsv, lower_red, upper_red)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations=3)

    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    max = -1
    max_index = -1

    for i in range(nlabels):

        if i < 1:
            continue

        area = stats[i, cv.CC_STAT_AREA]

        if area > max:
            max = area
            max_index = i

    if max_index != -1:

        center_x = int(centroids[max_index, 0])
        center_y = int(centroids[max_index, 1])
        left = stats[max_index, cv.CC_STAT_LEFT]
        top = stats[max_index, cv.CC_STAT_TOP]
        width = stats[max_index, cv.CC_STAT_WIDTH]
        height = stats[max_index, cv.CC_STAT_HEIGHT]

        # cv.rectangle(img_color, (left, top), (left + width, top + height), (0, 0, 255), 2)
        cv.circle(img_color, (center_x, center_y), 5, (0, 255, 0), -1)

        if isDraw:
            list_ball_location.append((center_x, center_y))
            t1.goto(center_x - 320, (480 - center_y) - 240)
            t1.pendown()

        else:
            history_ball_locations.append(list_ball_location.copy())
            list_ball_location.clear()
            t1.penup()

    img_color = draw_ball_location(img_color, list_ball_location)

    for ball_locations in history_ball_locations:  # 파란공 자취 그리기
        img_color = draw_ball_location(img_color, ball_locations)

    cv.imshow('Red', img_mask)
    cv.imshow('Result', img_color)

    key = cv.waitKey(1)
    if key == 27:  # esc
        break
    elif key == 32:  # space bar
        t1.clear()
        list_ball_location.clear()
        history_ball_locations.clear()

    elif key == ord('v'):
        isDraw = not isDraw

    elif key == 110: #n입력
        file+=1
        t= "./img/"+str(file)
        if os.path.isfile(t):
            win.bgpic(t)
            t1.clear()
            win.update()
        else:
            print("없다")
            break

    elif key == 98:  # b입력
        file -= 1
        t = "./img/"+str(file)
        if os.path.isfile(t):
            win.bgpic(t)
            t1.clear()
            win.update()
        else:
            print("없다")
            break
win.mainloop()
from PIL import Image
import os
path=input("Path of image files: ")
ConvertedtoPdfPath=input("path of pdf: ")
file_list=os.listdir(path)
img_list=[]
k=0
for i in file_list:
    print(i)
    print("진행상황: "+str(k)+'/'+str(len(file_list)))
    img=Image.open(path+"\\"+str(i))
    img_1=img.convert('RGB')
    img_list.append(img_1)
    k += 1
img_1.save(ConvertedtoPdfPath+'\\ConvertedToPdf.pdf',save_all=True,append_images=img_list)
print("완료")
'''
'''import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel

from PyQt5.QtGui import QPixmap

class QtGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Appia Qt GUI")

        # 라벨 생성

        label1 = QLabel(self)

        label1.move(10, 10)

        # 이미지 관련 클래스 생성 및 이미지 불러오기

        pixmap = QPixmap('.\img\0.gif')
        pixmap = pixmap.scaled(int(pixmap.width() / 2), int(pixmap.height() / 2))
        # 이미지 관련 클래스와 라벨 연결

        label1.setPixmap(pixmap)

        self.resize(pixmap.width() + 20, pixmap.height() + 20)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = QtGUI()

    app.exec_()
'''
'''import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel

from PyQt5.QtGui import QPixmap
import PyQt5 as Qt

class QtGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Appia Qt GUI")

        self.resize(700, 700)

        # 라벨 생성

        label1 = QLabel(self)

        label1.move(10, 10)

        # 이미지 관련 클래스 생성 및 이미지 불러오기

        pixmap = QPixmap('C:/Users/USER/PycharmProjects/blue/img/0')
        pixmap.scaledToWidth(100)
        pixmap.scaledToHeight(100)
        # 이미지 관련 클래스와 라벨 연결
        label1.setPixmap(pixmap)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = QtGUI()

    app.exec_()
'''

# 그리기 + 지우기 + 포인터 + 밑줄 + 터틀 그래픽 화면 크기에 맞게 조절
# pdf -> png
# 이미지 크기 줄이고 터틀 그래픽 배경 설정
'''
import cv2 as cv
import turtle as t
import os
from PIL import Image
from PIL import ImageGrab
# 이미지로 저장, 사이즈 조절
file_list = os.listdir("./source/")
from pdf2image import convert_from_path
for file_name in file_list:
    pages = convert_from_path("./source/" + file_name)
    for i, page in enumerate(pages):
        page.save("./img/"+str(i)+'.png', "PNG")
        img = Image.open('./img/'+str(i)+'.png')
        img_r = img.resize((int(img.size[0]*0.55), int(img.size[1]*0.55)))
        img_r.save('./img/'+str(i)+'.png')

# 터틀 그래픽 사이즈 조절
image1 = Image.open('./img/0.png')
wt = image1.size[0]  # 터틀 그래픽 가로
ht = image1.size[1]  # 터틀 그래픽 세로
win = t.Screen()
win.setup(wt, ht)
win.bgpic("./img/0.png")


def draw_ball_location(img_color, locations):
    for i in range(len(locations) - 1):

        if locations[0] is None or locations[1] is None:
            continue

        cv.line(img_color, tuple(locations[i]), tuple(locations[i + 1]), (0, 255, 255), 3)

    return img_color


cap = cv.VideoCapture(0)

list_ball_location = []
history_ball_locations = []
isDraw = True

t1 = t.Turtle()
pointer = t.Turtle()
hl = t.Turtle()
pointer.shape('circle')

t1.ht()
pointer.st()
hl.ht()
t1.penup()
pointer.penup()
hl.penup()

t1.color('blue')
pointer.color('red')
hl.color('#f5f3b3')

t1.pensize(3)
pointer.shapesize(0.5)
hl.pensize(20)

t1.speed(0)
pointer.speed(0)
hl.speed(0)

x = 0
y = 0
s = 0
end = 0
file = 0
win.update()

while True:

    ret, img_color = cap.read()

    img_color = cv.flip(img_color, 1)

    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    hue_red = 5
    lower_red = (hue_red - 5, 100, 180)
    upper_red = (hue_red + 5, 255, 255)
    img_mask = cv.inRange(img_hsv, lower_red, upper_red)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations=3)

    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    max = -1
    max_index = -1

    for i in range(nlabels):

        if i < 1:
            continue

        area = stats[i, cv.CC_STAT_AREA]

        if area > max:
            max = area
            max_index = i

    if max_index != -1:

        # 카메라 화면 물체 중심
        center_x = int(centroids[max_index, 0])
        center_y = int(centroids[max_index, 1])
        # 터틀 그래픽 화면 중심
        gcx = (wt/640)*center_x
        gcy = (ht/480)*center_y
        # 카메라 화면에 초록색 원으로 중심 표시
        cv.circle(img_color, (center_x, center_y), 5, (0, 255, 0), -1)
        # 터틀 그래픽에 포인터 표시
        pointer.goto(gcx - (wt/2), (ht - gcy) - (ht/2))

        # 필기 가능 상태
        if isDraw:
            list_ball_location.append((center_x, center_y))
            t1.goto(gcx - (wt/2), (ht - gcy) - (ht/2))
            t1.pendown()

        # 필기 중지 상태
        else:
            history_ball_locations.append(list_ball_location.copy())
            list_ball_location.clear()
            t1.penup()

        # 밑줄 긋기
        if s == 1:
            hl.pendown()
            hl.goto(gcx - (wt / 2), y)

    img_color = draw_ball_location(img_color, list_ball_location)

    for ball_locations in history_ball_locations:
        img_color = draw_ball_location(img_color, ball_locations)

    cv.imshow('Result', img_color)

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # esc 누르면 모두 종료
        t.bye()
        break
    elif key == 32:  # space bar 누르면 모두 지우기
        list_ball_location.clear()
        history_ball_locations.clear()
        t1.clear()
        hl.clear()
    elif key == ord('v'):  # v 누르면 필기 시작 / 필기 중지
        isDraw = not isDraw

    elif key == ord('s'):  # s 누르면 밑줄 시작
            x = gcx - (wt/2)
            y = (ht - gcy) - (ht/2)
            s = 1
            hl.goto(x, y)
            print(x, y)
    elif key == ord('e'):  # v 누르면 밑줄 종료
        if s == 1:
            hl.penup()
            s = 0
    elif key == ord('m'):
        sim=ImageGrab.grab((5,35,900,1040))
        sim.save("./img/"+str(file)+'.png')
    elif key == 110: # n 입력 -> 다음 페이지
        file+=1
        t= "./img/"+str(file)+'.png'
        if os.path.isfile(t):
            win.bgpic(t)
            t1.clear()
            hl.clear()
            win.update()
        else:
            print("없다")
            break
    elif key == 98:  # b 입력 -> 이전 페이지
        file -= 1
        t = "./img/"+str(file)+'.png'
        if os.path.isfile(t):
            win.bgpic(t)
            t1.clear()
            hl.clear()
            win.update()
        else:
            print("없다")
            break


path=input("Path of image files: ")
ConvertedtoPdfPath=input("path of pdf: ")
file_list=os.listdir(path)
img_list=[]
k=0
for i in file_list:
    print(i)
    print("진행상황: "+str(k)+'/'+str(len(file_list)))
    img=Image.open(path+"\\"+str(i))
    img_1=img.convert('RGB')
    img_list.append(img_1)
    k += 1
img_1.save(ConvertedtoPdfPath+'\\ConvertedToPdf.pdf',save_all=True,append_images=img_list)
print("완료")
win.mainloop()
'''

# 그리기 + 지우기 + 포인터 + 밑줄 + 터틀 그래픽 화면 크기에 맞게 조절
# pdf -> png
# 이미지 크기 줄이고 터틀 그래픽 배경 설정
# 그림 그린것 저장

import cv2 as cv
import turtle as t
import os
from PIL import Image
# 이미지로 저장, 사이즈 조절
cnt=0
file_list = os.listdir("./source/")
from pdf2image import convert_from_path
for file_name in file_list:
    pages = convert_from_path("./source/" + file_name)
    for i, page in enumerate(pages):
        page.save("./img/"+str(i)+'.png', "PNG")
        img = Image.open('./img/'+str(i)+'.png')
        img_r = img.resize((int(img.size[0]*0.55), int(img.size[1]*0.55)))
        img_r.save('./img/'+str(i)+'.png')
        cnt += 1

# 터틀 그래픽 사이즈 조절
image1 = Image.open('./img/0.png')
wt = image1.size[0]  # 터틀 그래픽 가로
ht = image1.size[1]  # 터틀 그래픽 세로
win = t.Screen()
screen = t.Screen()
win.setup(wt, ht)
screen.setup(wt, ht)
win.bgpic("./img/0.png")


def draw_ball_location(img_color, locations):
    for i in range(len(locations) - 1):

        if locations[0] is None or locations[1] is None:
            continue

        cv.line(img_color, tuple(locations[i]), tuple(locations[i + 1]), (0, 255, 255), 3)

    return img_color


from PIL import ImageGrab
import cv2
import keyboard
import mouse
import numpy as np

def set_roi():
    global ROI_SET, x1, y1, x2, y2
    ROI_SET = False
    print("Select your ROI using mouse drag.")
    while (mouse.is_pressed() == False):
        x1, y1 = mouse.get_position()
        while (mouse.is_pressed() == True):
            x2, y2 = mouse.get_position()
            while (mouse.is_pressed() == False):
                print("Your ROI : {0}, {1}, {2}, {3}".format(x1, y1, x2, y2))
                ROI_SET = True
                return

cap = cv.VideoCapture(0)

list_ball_location = []
history_ball_locations = []
isDraw = True

t1 = t.Turtle()
pointer = t.Turtle()
hl = t.Turtle()
pointer.shape('circle')

t1.ht()
pointer.st()
hl.ht()
t1.penup()
pointer.penup()
hl.penup()

t1.color('blue')
pointer.color('red')
hl.color('#f5f3b3')

t1.pensize(3)
pointer.shapesize(0.5)
hl.pensize(20)

t1.speed(0)
pointer.speed(0)
hl.speed(0)

x = 0
y = 0
s = 0
end = 0
file = 0
win.update()

while True:

    ret, img_color = cap.read()

    img_color = cv.flip(img_color, 1)

    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    hue_red = 5
    lower_red = (hue_red - 5, 95, 165)
    upper_red = (hue_red + 5, 255, 255)
    img_mask = cv.inRange(img_hsv, lower_red, upper_red)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations=3)

    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    max = -1
    max_index = -1

    for i in range(nlabels):

        if i < 1:
            continue

        area = stats[i, cv.CC_STAT_AREA]

        if area > max:
            max = area
            max_index = i

    if max_index != -1:

        # 카메라 화면 물체 중심
        center_x = int(centroids[max_index, 0])
        center_y = int(centroids[max_index, 1])
        # 터틀 그래픽 화면 중심
        gcx = (wt/640)*center_x
        gcy = (ht/480)*center_y
        # 카메라 화면에 초록색 원으로 중심 표시
        cv.circle(img_color, (center_x, center_y), 5, (0, 255, 0), -1)
        # 터틀 그래픽에 포인터 표시
        pointer.goto(gcx - (wt/2), (ht - gcy) - (ht/2))

        # 필기 가능 상태
        if isDraw:
            list_ball_location.append((center_x, center_y))
            t1.goto(gcx - (wt/2), (ht - gcy) - (ht/2))
            t1.pendown()

        # 필기 중지 상태
        else:
            history_ball_locations.append(list_ball_location.copy())
            list_ball_location.clear()
            t1.penup()

        # 밑줄 긋기
        if s == 1:
            hl.pendown()
            hl.goto(gcx - (wt / 2), y)

    img_color = draw_ball_location(img_color, list_ball_location)

    for ball_locations in history_ball_locations:
        img_color = draw_ball_location(img_color, ball_locations)

    cv.imshow('Result', img_color)

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # esc 누르면 모두 종료
        t.bye()
        break
    elif key == 32:  # space bar 누르면 모두 지우기
        list_ball_location.clear()
        history_ball_locations.clear()
        t1.clear()
        hl.clear()
    elif key == ord('v'):  # v 누르면 필기 시작 / 필기 중지
        isDraw = not isDraw

    elif key == ord('s'):  # s 누르면 밑줄 시작
            x = gcx - (wt/2)
            y = (ht - gcy) - (ht/2)
            s = 1
            hl.goto(x, y)
            print(x, y)
    elif key == ord('e'):  # v 누르면 밑줄 종료
        if s == 1:
            hl.penup()
            s = 0

    elif key == 110: # n 입력 -> 다음 페이지
        pointer.ht()
        pointer.st()
        file += 1
        t= "./img/"+str(file)+'.png'
        if os.path.isfile(t):
            win.bgpic(t)
            t1.clear()
            hl.clear()
            win.update()
        else:
            print("없다")
            break
    elif key == 98:  # b 입력 -> 이전 페이지
        pointer.ht()
        pointer.st()
        file -= 1
        t = "./img/"+str(file)+'.png'
        if os.path.isfile(t):
            win.bgpic(t)
            t1.clear()
            hl.clear()
            win.update()
        else:
            print("없다")
            break
    elif key==ord("k"):
        ROI_SET = False
        x1, y1, x2, y2 = 0, 0, 0, 0
        set_roi()
        while True:
            image = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_BGR2RGB)
            key = cv2.waitKey(100)
            if key == ord("q"):
                print("Quit")
                break
        cv2.imwrite('./img/'+str(file)+'.png', image)


for i in range(0, cnt):
    del_file_name='./'+str(i)+'.eps'
    if os.path.isfile(del_file_name):
        os.remove(del_file_name)

path = input("Path of image files: ")
ConvertedtoPdfPath = input("path of pdf: ")
file_list = os.listdir(path)
img_list = []
k = 0
for i in range(0, cnt):
    print(i)
    print("진행상황: "+str(k)+'/'+str(cnt))
    img = Image.open(path+'\\'+str(k)+'.png')
    img_1 = img.convert('RGB')
    if k != 0:
        img_list.append(img)
    k += 1
img1 = Image.open('./img/0.png')
img1.save(ConvertedtoPdfPath+'\\ConvertedToPdf.pdf',save_all=True,append_images=img_list)
print("완료")

win.mainloop()
