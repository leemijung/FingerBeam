# 그리기 + 지우기 + 포인터 + 밑줄 + 터틀 그래픽 화면 크기에 맞게 조절
# pdf -> png
# 이미지 크기 줄이고 터틀 그래픽 배경 설정
# 그림 그린것 저장

import cv2 as cv
import turtle as t
import os
from PIL import Image
# 이미지로 저장, 사이즈 조절
file_list = os.listdir("./loc/")
from pdf2image import convert_from_path
for file_name in file_list:
    pages = convert_from_path("./loc/" + file_name)
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

def savePen(name):
    #screen.tracer(False)
    #screen.tracer(True)
    canvas = screen.getcanvas()
    canvas.postscript(file=name + '.eps', width=wt, height=ht)
    img = Image.open(name + '.eps')
    img.save('./img/' + name + '.png')

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
        savePen(str(file))
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
        savePen(str(file))
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