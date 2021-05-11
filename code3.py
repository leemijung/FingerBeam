import cv2 as cv
import turtle as t
import os
from PIL import Image
from pdf2image import convert_from_path
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets


def draw_ball_location(img_color, locations):
    for i in range(len(locations) - 1):
        if locations[0] is None or locations[1] is None:
            continue

        cv.line(img_color, tuple(locations[i]), tuple(locations[i + 1]), (0, 255, 255), 3)

    return img_color


def save_pen(name):
    pointer.ht()
    screen.tracer(False)
    canvas = screen.getcanvas()
    canvas.postscript(file=name + '.eps', width=wt, height=ht)
    screen.tracer(True)
    pointer.st()


def move_page(index):
    t = "./img/" + str(index) + '.png'
    clear()
    win.bgpic(t)
    win.update()


def clear():
    list_ball_location.clear()
    history_ball_locations.clear()
    t1.clear()
    pointer.clear()



global file
file = 0
global cnt
cnt = 0
global path_name
path_name = None


opening_ = 'opening.ui'
form_1, base_1 = uic.loadUiType(opening_)

file_upload_ = 'fileupload2.ui'
form_2, base_2 = uic.loadUiType(file_upload_)

loading_ = 'loading1.ui'
form_3, base_3 = uic.loadUiType(loading_)

note_ = 'takingnote2.ui'
form_4, base_4 = uic.loadUiType(note_)


class convert_file():
    def __init__(self):
        super().__init__()

    def pdf_to_png(self):
        global cnt, path_name
        pages = convert_from_path(path_name)
        for i, page in enumerate(pages):
            page.save("./img/" + str(i) + '.png', "PNG")
            img = Image.open('./img/' + str(i) + '.png')
            img_r = img.resize((int(img.size[0] * 0.55), int(img.size[1] * 0.55)))
            img_r.save('./img/' + str(i) + '.png')
            cnt += 1
        cnt -= 1
        print("done")

    def del_eps(self):
        global cnt
        for index in range(0, cnt):
            del_file_name = './' + str(index) + '.eps'
            if os.path.isfile(del_file_name):
                os.remove(del_file_name)

    def png_to_pdf(self):
        global cnt
        pdf_path = './source/'
        img_list = []
        k = 0
        for i in range(0, cnt):
            img = Image.open('./'+str(k)+'.eps')
            img_1 = img.convert('RGB')
            if k != 0:
                img_list.append(img_1)
            k += 1
        img1 = Image.open('./img/0.eps')
        img1.save(pdf_path + '\\ConvertedToPdf.pdf', save_all=True, append_images=img_list)
        print("완료")
        self.del_eps()


class opening_page(base_1, form_1):
    def __init__(self):
        super(base_1, self).__init__()
        self.setupUi(self)
        self.start_btn.clicked.connect(self.change)
        self.exit_btn.clicked.connect(self.quit)

    def change(self):
        self.main = upload_page()
        self.main.show()
        self.close()

    def quit(self):
        self.close()


class upload_page(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.fileopen)

    def fileopen(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        global path_name
        path_name = filename[0]
        self.main = loading_page()
        self.main.show()
        self.close()


class loading_page(base_3, form_3):
    def __init__(self):
        super(base_3, self).__init__()
        self.setupUi(self)

    def close_page(self):
        self.main = note_page()
        self.main.show()
        self.close()


class note_page(base_4, form_4):
    def __init__(self):
        super(base_4, self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.home)
        self.pushButton_2.clicked.connect(self.prev)
        self.pushButton.clicked.connect(self.draw)
        self.pushButton_4.clicked.connect(self.next)
        self.pushButton_5.clicked.connect(self.end)

    def home(self):
        global file
        file = 0
        print(file)

    def prev(self):
        global file
        if file >= 1:
            file -= 1
        print(file)

    def draw(self):
        global  isDraw
        isDraw = not isDraw

    def next(self):
        global file, cnt
        if file <= cnt-1:
            file += 1
        print(file)

    def end(self):
        global file, cnt
        file = cnt
        print(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    op = opening_page()
    op.show()
    #sys.exit(app.exec_())
    app.exec_()


image1 = Image.open('./img/0.png')
wt = image1.size[0]
ht = image1.size[1]

win = t.Screen()
screen = t.Screen()
win.setup(wt, ht)
screen.setup(wt, ht)
win.bgpic("./img/0.png")


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
        center_x = int(centroids[max_index, 0])
        center_y = int(centroids[max_index, 1])
        gcx = (wt/640)*center_x
        gcy = (ht/480)*center_y
        cv.circle(img_color, (center_x, center_y), 5, (0, 255, 0), -1)
        pointer.goto(gcx - (wt/2), (ht - gcy) - (ht/2))

        if isDraw:
            list_ball_location.append((center_x, center_y))
            t1.goto(gcx - (wt/2), (ht - gcy) - (ht/2))
            t1.pendown()
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
        clear()




cap.release()
cv.destroyAllWindows()

win.mainloop()