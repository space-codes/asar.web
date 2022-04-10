import cv2
import numpy as np
from preprocessing import morphological_operation,gaus_thresh, resize
import os


def remove_dots(img):
    height = img.shape[0]
    width = img.shape[1]
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(
        img.astype(np.uint8), connectivity=8)
    new_img = np.zeros_like(img)

    for i in range(1, ret):
        cc_width = stats[i, cv2.CC_STAT_WIDTH]
        cc_height = stats[i, cv2.CC_STAT_HEIGHT]

        if cc_width >= 0.2 * width or cc_height >= 0.2 * height:
            new_img[labels == i] = 1

    return new_img


def words_extract(img):
    height = img.shape[0]
    width = img.shape[1]

    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bin_img = cv2.adaptiveThreshold(grey_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 20)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    final_thr = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
    final_thr = remove_dots(final_thr)
    final_thr = cv2.convertScaleAbs(final_thr, alpha=(255.0))

    letter_k = []
    contours, hierarchy = cv2.findContours(final_thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) >= 70:
            x, y, w, h = cv2.boundingRect(cnt)
            letter_k.append((x, y, w, h))

    letter = sorted(letter_k, key=lambda l: l[0])
    letter_index = len(letter)
    end = 0
    words = []
    for e in range(len(letter)):
        if (letter[e][0] + letter[e][2] - 5) < end:
            continue
        start = letter[e][0]
        if start < end:
            start = end
        end = letter[e][0] + letter[e][2]
        letter_index -= 1
        h1 = 0
        if letter[e][1] - 50 > 0:
            h1 = letter[e][1] - 50
        h2 = height - 1
        if h2 > letter[e][3] + letter[e][1] + 50:
            h2 = letter[e][3] + letter[e][1] + 50
        letter_img_tmp = img[h1:h2, start:end]
        words.append(letter_img_tmp)
    words.reverse()
    return words

def multi_line_ext(img):
    img = resize(img)
    thresh = gaus_thresh(img)
    dilation = morphological_operation(thresh)
    (contours, _) = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(contours)
    contours.reverse()
    height, width = img.shape[0], img.shape[1]

    lines = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 30000:
            x, y, w, h = cv2.boundingRect(cnt)
            y2 = y - 5
            if y2 < 0:
                y2 = 0
            h2 = y2 + h + 10
            if h2 > height - 1:
                h2 = height - 1
            line = img[y2:h2, x:x + w]
            # cv2.imwrite('lines/' + '_' + str(i) + '.png', line)
            # cv2.rectangle(imgcpy2, (x-1, y-5), (x + w, y + h), (randint(0, 255), randint(0, 255), randint(0, 255)), 5)
            #segment(line)
            lines.append(line)
    return lines
    #cv2.imwrite('data5/imgContoure.png', imgcpy2)


