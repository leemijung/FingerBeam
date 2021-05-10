import cv2 as cv
import turtle as t
import os
from PIL import Image
from pdf2image import convert_from_path
from PIL import ImageGrab
import cv2
import keyboard
import mouse
import numpy as np

cnt = 0
file_list = os.listdir("./source/")

for file_name in file_list:
    pages = convert_from_path("./source/" + file_name)
    for i, page in enumerate(pages):
        page.save("./img/"+str(i)+'.png', "PNG")
        img = Image.open('./img/'+str(i)+'.png')
        img_r = img.resize((int(img.size[0]*0.55), int(img.size[1]*0.55)))
        img_r.save('./img/'+str(i)+'.png')
        cnt += 1

# path = input("Path of image files: ")
path = './img/'
# ConvertedtoPdfPath = input("path of pdf: ")
ConvertedtoPdfPath = './source/'

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

def save_pen(name):
    pointer.ht()
    screen.tracer(False)
    canvas = screen.getcanvas()
    canvas.postscript(file=name + '.eps', width=wt, height=ht)
    img = Image.open(name + '.eps')
    img.save('./img/' + name + '.png')
    screen.tracer(True)
    pointer.st()

def move_page(index):
    t = "./img/" + str(index) + '.png'
    if os.path.isfile(t):
        win.bgpic(t)
        t1.clear()
        pointer.clear()
        win.update()
        return 1
    else:
        print("없다")
        return 0


cap = cv.VideoCapture(0)

list_ball_location = []
history_ball_locations = []
isDraw = True

t1 = t.Turtle()
pointer = t.Turtle()
pointer.shape('circle')

t1.ht()
pointer.st()
t1.penup()
pointer.penup()

t1.color('blue')
pointer.color('red')

t1.pensize(3)
pointer.shapesize(0.5)

t1.speed(0)
pointer.speed(0)

x = y = s = end = file = 0
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

    img_color = draw_ball_location(img_color, list_ball_location)

    for ball_locations in history_ball_locations:
        img_color = draw_ball_location(img_color, ball_locations)

    cv.imshow('Result', img_color)

    key = cv.waitKey(1) & 0xFF
    if key == 32:  # space bar 누르면 모두 지우기
        list_ball_location.clear()
        history_ball_locations.clear()
        t1.clear()
        pointer.clear()
    elif key == ord('v'):  # v 누르면 필기 시작 / 필기 중지
        isDraw = not isDraw
    elif key == 110:  # n 입력 -> 다음 페이지
        save_pen(str(file))
        file += 1
        if move_page(file) == 0:
            break
    elif key == 98:  # b 입력 -> 이전 페이지
        save_pen(str(file))
        file -= 1
        if move_page(file) == 0:
            break
    elif key == ord("k"):
        ROI_SET = False
        x1, y1, x2, y2 = 0, 0, 0, 0
        set_roi()
        pointer.ht()
        while True:
            image = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2))), cv2.COLOR_BGR2RGB)
            break
        cv2.imwrite('./img/'+str(file)+'.png', image)
        pointer.st()


# .eps 삭제
#for i in range(0, cnt):
#    del_file_name = './'+str(i)+'.ps'
#    if os.path.isfile(del_file_name):
#        os.remove(del_file_name)

file_list = os.listdir(path)
img_list = []
k = 0
for i in range(0, cnt):
    print(i)
    print("진행상황: "+str(k)+'/'+str(cnt))
    img = Image.open(path+'\\'+str(k)+'.png')
    #img = Image.open('./'+str(k)+'.ps')
    img_1 = img.convert('RGB')
    if k != 0:
        img_list.append(img)
    k += 1
img1 = Image.open('./img/0.png')
img1.save(ConvertedtoPdfPath+'\\ConvertedToPdf.pdf', save_all=True, append_images=img_list)
print("완료")

win.mainloop()