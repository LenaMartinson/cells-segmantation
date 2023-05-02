import numpy as np
import cv2 as cv


def contourIntersect(contour1, contour2):
    contours = [contour1, contour2]

    blank = np.zeros((256, 256))

    image1 = cv.drawContours(blank.copy(), [contours[0]], 0, 1, thickness=cv.FILLED)
    image2 = cv.drawContours(blank.copy(), [contours[1]], 0, 1, thickness=cv.FILLED)
    
    intersection = np.logical_and(image1, image2)
    
    return intersection.any()


def make_contours(path, name):    
    sample_image = cv.imread(path + name)
    img = cv.cvtColor(sample_image, cv.COLOR_BGR2RGB)
    
    gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)

    canny = cv.Canny(gray, 20, 150, L2gradient=False)
    canny_dilate = cv.dilate(canny, None)

    new_img = cv.addWeighted(gray, 1, canny_dilate, 1, 0)

    new_img_2 = new_img.copy()

    gray = new_img_2.copy()
    _,thresh = cv.threshold(gray, 80, 255, cv.THRESH_BINARY_INV)

    cnt_all = sorted(cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[-2], key=cv.contourArea)
    
    with open(path + name[:-4] + ".svg", "w+") as f:
        f.write(f'<svg width="{256}" height="{256}" xmlns="http://www.w3.org/2000/svg" fill-opacity="0" stroke="black" stroke-width="3" >')

        hull_list = []
        for i in range(-1, -len(cnt_all) - 1, -1):
            cnt = cnt_all[i]
            mask = np.zeros((256,256), np.uint8)
            masked = cv.drawContours(mask, [cnt], -1, 255, -1)

            contours, _ = cv.findContours(image=masked, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)

            image_copy = new_img_2.copy()
            cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 0, 0), thickness=2, lineType=cv.LINE_AA)

            too_small = False
            for i in range(len(contours)):
                hull = cv.convexHull(contours[i])
                hull_list.append(hull)
                if cv.contourArea(contours[i]) < 500:
                    too_small = True
                    break
            if too_small:
                hull_list.pop()
                continue
            
            for i in range(0, len(hull_list) - 1):
                if contourIntersect(hull_list[i], hull_list[-1]):
                    hull_list.pop()
                    break


        for c in hull_list:
            f.write('<path d="M')
            for i in range(len(c)):
                x, y = c[i][0]
                f.write(f"{x} {y} ")
            for i in range(len(c)):
                x, y = c[i][0]
                f.write(f"{x} {y} ")
                break
            f.write('"/>')
        f.write("</svg>")
