import cv2 as cv
import turtle as t
import os
from PIL import Image
from pdf2image import convert_from_path
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets

from PyQt5 import QtGui
import threading
from PyQt5 import QtCore

global file
file = 0
global cnt
cnt = 0
global path_name
path_name = None

opening_ = 'opening.ui'
form_1, base_1 = uic.loadUiType(opening_)

file_upload_ = 'fileupload.ui'
form_2, base_2 = uic.loadUiType(file_upload_)

note_ = 'takingnote2.ui'
form_3, base_3 = uic.loadUiType(note_)

askingsave_ = 'askingsave.ui'
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
            img_r.save('./img/' + str(i) + '_.png')
            cnt += 1
        cnt -= 1
        print("done")

    def del_eps(self):
        global cnt
        for index in range(0, cnt + 1):
            del_file_name = './img/' + str(index) + '.eps'
            if os.path.isfile(del_file_name):
                os.remove(del_file_name)

    def del_png(self):
        global cnt
        for index in range(0, cnt + 1):
            del_file_name1 = './img/' + str(index) + '.png'
            del_file_name2 = './img/' + str(index) + '_.png'
            if os.path.isfile(del_file_name1):
                os.remove(del_file_name1)
            if os.path.isfile(del_file_name2):
                os.remove(del_file_name2)

    def png_to_pdf(self):
        global cnt
        pdf_path = './convertedPDF/'
        img_list = []
        k = 0
        for i in range(0, cnt):
            img = Image.open('./' + str(k) + '_.png')
            img_1 = img.convert('RGB')
            if k != 0:
                img_list.append(img_1)
            k += 1
        img1 = Image.open('./0_.png')
        img1.save(pdf_path + '\\ConvertedToPdf.pdf', save_all=True, append_images=img_list)
        print("완료")
        self.del_eps()


class take_note():
    def __init__(self):
        super().__init__()

    def draw_ball_location(self, img_color, locations):
        for i in range(len(locations) - 1):
            if locations[0] is None or locations[1] is None:
                continue

            cv.line(img_color, tuple(locations[i]), tuple(locations[i + 1]), (0, 255, 255), 3)

        return img_color

    def save_pen(self, name):
        note_page.pointer.ht()
        note_page.screen.tracer(False)
        canvas = note_page.screen.getcanvas()
        canvas.postscript(file=name + '.eps', width=note_page.wt, height=note_page.ht)
        img = Image.open(name + '.eps')
        img.save('./img/' + name + '_.png')
        note_page.screen.tracer(True)
        note_page.pointer.st()

    def move_page(self, index):
        t = "./img/" + str(index) + '.png'
        self.clear()
        note_page.win.bgpic(t)
        note_page.win.update()

    # def clear(self):
    #     note_page.list_ball_location.clear()
    #     note_page.history_ball_locations.clear()
    #     note_page.t1.clear()
    #     note_page.pointer.clear()


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
        self.main = note_page()
        self.main.show()
        self.close()
        cv = convert_file()
        cv.pdf_to_png()


class note_page(base_3, form_3):
    def __init__(self):
        super(base_3, self).__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.home)
        self.pushButton_2.clicked.connect(self.prev)
        # self.pushButton.clicked.connect(self.change)
        self.pushButton.clicked.connect(self.changeColor)
        self.pushButton.clicked.connect(self.start)
        self.pushButton.setCheckable(True)
        self.pushButton.setStyleSheet("background-color : lightblue")
        self.update()
        self.show()
        self.pushButton_4.clicked.connect(self.next)
        self.pushButton_5.clicked.connect(self.end)
        # self.label.setText("※ v : 누르면서 필기하세요 ")



    def runa(self):

        print("runa")
        image1 = Image.open('./img/0.png')
        wt = image1.size[0]
        ht = image1.size[1]

        win = t.Screen()
        screen = t.Screen()
        win.setup(wt, ht)
        screen.setup(wt, ht)
        win.bgpic("./img/0.png")
        list_ball_location = []
        history_ball_locations = []


        cap = cv.VideoCapture(0)


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

        global x
        global y
        global s
        global end
        global file
        x = y = s = end = file = 0
        win.update()

        while True:
            t_n = take_note()
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
                gcx = (wt / 640) * center_x
                gcy = (ht / 480) * center_y
                cv.circle(img_color, (center_x, center_y), 5, (0, 255, 0), -1)
                pointer.goto(gcx - (wt / 2), (ht - gcy) - (ht / 2))

                if isDraw:
                    list_ball_location.append((center_x, center_y))
                    t1.goto(gcx - (wt / 2), (ht - gcy) - (ht / 2))
                    t1.pendown()
                else:
                    history_ball_locations.append(list_ball_location.copy())
                    list_ball_location.clear()
                    t1.penup()

            img_color = t_n.draw_ball_location(img_color, list_ball_location)

            for ball_locations in history_ball_locations:
                img_color = t_n.draw_ball_location(img_color, ball_locations)

            cv.imshow('Result', img_color)

            key = cv.waitKey(1) & 0xFF
            if key == 32:  # space bar 누르면 모두 지우기
                #t_n.clear()
                list_ball_location.clear()
                history_ball_locations.clear()
                t1.clear()
                pointer.clear()
            elif key == ord('v'):  # v 누르면 필기 시작 / 필기 중지
                isDraw = not isDraw



    def start(self):
        global running
        running = True
        th = threading.Thread(target=self.runa)
        th.start()
        print("started..")

    def changeColor(self):
        if self.pushButton.isChecked():
            self.pushButton.setStyleSheet("background-color : #ff557f")
            self.pushButton.setText("필기 중단")
            # self.change()
        else:
            self.pushButton.styleSheet("background-color : lightblue")

    def home(self):
        global file
        file = 0
        print(file)

    def prev(self):
        global file
        if file >= 1:
            file -= 1

        take_note.move_page(file)
        # t = "./img/" + str(index) + '.png'
        # self.clear()
        # note_page.win.bgpic(t)
        # note_page.win.update()
        print(file)

    def next(self):
        global file, cnt
        if file <= cnt - 1:
            file += 1
        take_note.move_page(file)
        print(file)

    def end(self):
        global file, cnt
        file = cnt
        print(file)

    def change(self):
        self.main = askingsave_page()
        self.main.show()
        self.close()


class askingsave_page(base_4, form_4):
    def __init__(self):
        super(base_4, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.yes)
        self.pushButton_2.clicked.connect(self.no)

    def yes(self):
        yes_save = convert_file()
        yes_save.del_eps()
        yes_save.png_to_pdf()
        yes_save.del_png()
        self.close()

    def no(self):
        no_save = convert_file()
        no_save.del_eps()
        no_save.del_png()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    op = opening_page()
    op.show()
    # sys.exit(app.exec_())
    app.exec_()







note_page.cap.release()
cv.destroyAllWindows()

note_page.win.mainloop()
