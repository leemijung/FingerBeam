import cv2 as cv
import turtle as t
from PIL import Image
from pdf2image import convert_from_path
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import threading

# 터틀 화면에 배경을 설정하기 위한 변수
global file
file = 0
# pdf 파일의 페이지 수를 저장하기 위한 변수
global cnt
cnt = 0
# 사용자가 선택한 파일의 경로를 저장하기 위한 변수
global path_name
path_name = None

# 시작 페이지 ui
opening_ = 'opening.ui'
form_1, base_1 = uic.loadUiType(opening_)
# 파일 업로드 페이지 ui
file_upload_ = 'fileupload.ui'
form_2, base_2 = uic.loadUiType(file_upload_)
# 필기 조작 페이지 ui
note_ = 'takingnote2.ui'
form_3, base_3 = uic.loadUiType(note_)
# 필기 종료 후 파일을 저장할 것인지 물어보는 페이지 ui
askingsave_ = 'askingsave.ui'
form_4, base_4 = uic.loadUiType(askingsave_)


# 사용자가 파일 업로드 페이지에서 선택한 pdf 파일을 png 파일로 변환시킴
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


# 화면에 필기한 것을 저장하는 용도
class take_note():
    def __init__(self):
        super().__init__()

    def draw_ball_location(self, img_color, locations):
        for i in range(len(locations) - 1):
            if locations[0] is None or locations[1] is None:
                continue
            cv.line(img_color, tuple(locations[i]), tuple(locations[i + 1]), (0, 255, 255), 3)

        return img_color


# 첫 번째 페이지
class opening_page(base_1, form_1):
    def __init__(self):
        super(base_1, self).__init__()
        self.setupUi(self)
        self.start_btn.clicked.connect(self.change)
        self.exit_btn.clicked.connect(self.quit)

    # 사용자가 [시작] 버튼을 누르면 파일 업로드 페이지로 이동
    def change(self):
        self.main = upload_page()
        self.main.show()
        self.close()

    # 사용자가 [종료] 버튼을 누르면 프로그램 종료
    def quit(self):
        self.close()





# 두 번째 페이지
class upload_page(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.fileopen)

    # 사용자가 파일을 오픈하고 pdf 파일을 png 파일로 변환
    def fileopen(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        global path_name
        path_name = filename[0]
        self.main = note_page()
        self.main.show()
        self.close()
        cv = convert_file()
        cv.pdf_to_png()





# 세 번째 페이지
class note_page(base_3, form_3):
    def __init__(self):
        super(base_3, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.changeColor)
        self.pushButton.setCheckable(True)
        self.pushButton.setStyleSheet("background-color : lightblue")
        self.update()
        self.show()

    # 프로그램의 메인 부분
    def runa(self):
        # turtle 그래픽의 배경과 배경의 크기 설정
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

        # 터틀 화면에 필기할 펜과 포인터 생성
        t1 = t.Turtle()
        pointer = t.Turtle()
        pointer.shape('circle')
        t1.ht()
        pointer.st()
        t1.penup()
        pointer.penup()

        # 펜과 포인터의 색상과 크기, 속도 설정
        t1.color('blue')
        pointer.color('red')
        t1.pensize(3)
        pointer.shapesize(0.5)
        t1.speed(0)
        pointer.speed(0)

        global file
        global check
        global check2
        global check3
        global check4
        global cnt
        file = 0
        check = False
        check2 = False
        check3 = False
        check4 = False
        win.update()

        while True:
            t_n = take_note()
            ret, img_color = cap.read()
            img_color = cv.flip(img_color, 1)
            img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
            # 빨간색을 인식
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
                pointer.goto(gcx - (wt / 2), (ht - gcy) - (ht / 2))  # 카메라 화면과 터틀 그래픽의 사이즈에 맞게 크기 조절

                if isDraw:  # 필기를 한다면
                    list_ball_location.append((center_x, center_y))
                    t1.goto(gcx - (wt / 2), (ht - gcy) - (ht / 2))  # 카메라 화면과 터틀 그래픽의 사이즈에 맞게 크기 조절
                    t1.pendown()
                else:  # 필기를 하지 않는다면
                    history_ball_locations.append(list_ball_location.copy())
                    list_ball_location.clear()
                    t1.penup()

            img_color = t_n.draw_ball_location(img_color, list_ball_location)

            for ball_locations in history_ball_locations:
                img_color = t_n.draw_ball_location(img_color, ball_locations)
            cv.imshow('Result', img_color)

            key = cv.waitKey(1) & 0xFF
            if key == 32:  # space bar 누르면 모두 지우기
                list_ball_location.clear()
                history_ball_locations.clear()
                t1.clear()
                pointer.clear()
            elif key == ord('v'):  # v 누르면 필기 시작 / 필기 중지
                isDraw = not isDraw



            self.pushButton_4.clicked.connect(self.checking)
            self.pushButton_2.clicked.connect(self.checking2)
            self.pushButton_3.clicked.connect(self.checking3)
            self.pushButton_5.clicked.connect(self.checking4)

            # [next] 버튼 누르면
            if check == True:
                # 터틀 화면 저장
                pointer.ht()
                screen.tracer(False)
                canvas = screen.getcanvas()
                canvas.postscript(file=str(file) + '.eps', width=wt, height=ht)
                img = Image.open(str(file) + '.eps')
                img.save('./img/' + str(file) + '_.png')
                screen.tracer(True)
                pointer.st()
                # 터틀 화면이 마지막 페이지가 아니라면, 다음 페이지를 보여줌
                if file <= cnt - 1:
                    file += 1
                    a = "./img/" + str(file) + '.png'
                    win.clear()
                    win.bgpic(a)
                    win.update()
                check = False
                print(file)



            # [prev] 버튼 누르면
            if check2 == True:
                # 터틀 화면 저장
                pointer.ht()
                screen.tracer(False)
                canvas = screen.getcanvas()
                canvas.postscript(file=str(file) + '.eps', width=wt, height=ht)
                img = Image.open(str(file) + '.eps')
                img.save('./img/' + str(file) + '_.png')
                screen.tracer(True)
                pointer.st()
                # 터틀 화면이 첫 페이지가 아니라면, 이전 페이지를 보여줌
                if file >= 1:
                    file -= 1
                    a = "./img/" + str(file) + '.png'
                    win.clear()
                    win.bgpic(a)
                    win.update()
                check2 = False
                print(file)



            # [home] 버튼 누르면
            if check3 == True:
                # 터틀 화면 저장
                pointer.ht()
                screen.tracer(False)
                canvas = screen.getcanvas()
                canvas.postscript(file=str(file) + '.eps', width=wt, height=ht)
                img = Image.open(str(file) + '.eps')
                img.save('./img/' + str(file) + '_.png')
                screen.tracer(True)
                pointer.st()
                # 터틀 화면이 첫 페이지가 아니라면, 첫 페이지를 보여줌
                if file != 0:
                    file = 0
                    a = "./img/" + str(file) + '.png'
                    win.clear()
                    win.bgpic(a)
                    win.update()
                check3 = False
                print(file)



            # [end] 버튼 누르면
            if check4 == True:
                # 터틀 화면 저장
                pointer.ht()
                screen.tracer(False)
                canvas = screen.getcanvas()
                canvas.postscript(file=str(file) + '.eps', width=wt, height=ht)
                img = Image.open(str(file) + '.eps')
                img.save('./img/' + str(file) + '_.png')
                screen.tracer(True)
                pointer.st()
                # 터틀 화면이 마지막 페이지가 아니라면, 마지막 페이지를 보여줌
                if file != cnt:
                    file = cnt
                    a = "./img/" + str(file) + '.png'
                    win.clear()
                    win.bgpic(a)
                    win.update()
                check4 = False
                print(file)



    # 버튼을 누르면 True로 바꾸어 if문을 수행하도록 함
    def checking(self):
        global check
        check = True

    def checking2(self):
        global check2
        check2 = True

    def checking3(self):
        global check3
        check3 = True

    def checking4(self):
        global check4
        check4 = True

    def changeColor(self):
        global change
        # [필기 시작] 버튼을 누르면 [필기 중단]으로 바뀌고, 버튼을 다시 누를 수 있는 상태로 바뀜
        if self.pushButton.isChecked():
            self.pushButton.setStyleSheet("background-color : #ff557f")
            self.pushButton.setText("필기 중단")
            self.pushButton.setCheckable(False)
            # 필기에 관한 함수인 runa 실행
            th = threading.Thread(target=self.runa)
            th.start()
            print("started..")
        # [필기 중단] 버튼을 누르면 저장을 물어보는 페이지로 이동
        else:
            self.main = askingsave_page()
            self.main.show()
            self.close()




class askingsave_page(base_4, form_4):
    def __init__(self):
        super(base_4, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.yes)
        self.pushButton_2.clicked.connect(self.no)

    # [ok] 버튼을 누르면 필기했던 페이지들을 pdf 파일로 변환
    def yes(self):
        global cnt

        pdf_path = './convertedPdf/'
        img_list = []
        k = 0
        for i in range(0, cnt + 1):
            img = Image.open('./img/' + str(k) + '_' + '.png')
            img_1 = img.convert('RGB')
            if k != 0:
                img_list.append(img_1)
            k += 1

        img1 = Image.open('./img/0_.png')
        img1.save(pdf_path + '\\ConvertedToPdf.pdf', save_all=True, append_images=img_list)
        print("png 완료")
        self.close()

    # [cancel] 버튼을 누르면 종료
    def no(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    op = opening_page()
    op.show()
    sys.exit(app.exec_())

note_page.cap.release()
cv.destroyAllWindows()

note_page.win.mainloop()