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
        y=int(centroids[i][1])
        if (y > 0.35 * height and y < 0.8 * height and cc_height >= 0.20 * height) or \
                (cc_height >= 0.4 * height) or \
                (cc_height >= 0.3 * height and y > 0.35 * height):
          new_img[labels == i] = 255

    return new_img


def words_extract(img):
    height = img.shape[0]
    width = img.shape[1]

    # preprocessing for word segmentation
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, bin_img = cv2.threshold(grey_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    final_thr = remove_dots(bin_img)

    # finding words contours
    letter_k = []
    contours, hierarchy = cv2.findContours(final_thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # selecting important contours
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) >= 70 or 2 * w <= h:
            letter_k.append((x, y, w, h, (-x - w)))

    # sorting contours positions from left to right
    letter = sorted(letter_k, key=lambda sort_by: sort_by[0])

    letter_index = len(letter)
    end = 0
    words = []
    for e in range(len(letter)):
        ok = 1
        # if this word considered before neglect it
        if (letter[e][0] + letter[e][2]) < end:
            continue
        # if the difference between ends less than 5 and it doesn't alef ,neglect it
        if ((letter[e][0] + letter[e][2]) - end) < 5 and 2 * letter[e][2] > letter[e][3]:
            ok = 0
        if ((letter[e][0] + letter[e][2]) - end) < 0.25 * (letter[e][2]):
            ok = 0

        start = letter[e][0]
        if start < end:
            start = end
        end = letter[e][0] + letter[e][2]

        if ok == 0:
            continue

        letter_index -= 1
        h1 = 0
        if letter[e][1] - 50 > 0:
            h1 = letter[e][1] - 50
        h2 = height - 1
        if h2 > letter[e][3] + letter[e][1] + 50:
            h2 = letter[e][3] + letter[e][1] + 50

        w1 = start - 5
        if w1 < 0:
            w1 = 0
        w2 = end + 2
        if w2 >= width:
            w2 = width - 1

        if (w2 - w1) <= 5:
            continue

        letter_img_tmp = img[h1:h2, w1:w2]
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
            h2 = y2 + h + 15
            if h2 > height - 1:
                h2 = height - 1
            line = img[y2:h2, x:x + w]
            # cv2.imwrite('lines/' + '_' + str(i) + '.png', line)
            # cv2.rectangle(imgcpy2, (x-1, y-5), (x + w, y + h), (randint(0, 255), randint(0, 255), randint(0, 255)), 5)
            #segment(line)
            lines.append(line)
    return lines
    #cv2.imwrite('data5/imgContoure.png', imgcpy2)


