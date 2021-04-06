import cv2 as cv
import turtle as t



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
win.setup(640, 480)
t1 = t.Turtle()
t1.shape('circle')
t1.ht()
t1.penup()
t1.color('blue')
t1.shapesize(3)
t1.speed(0)
win.onkey(t.bye, 'q')
win.listen()

win.bgpic("ss.gif")
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

win.mainloop()