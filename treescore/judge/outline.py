"""
Detects the outline of the tree
"""

import numpy as np
import cv2


def outline(image):
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # edged = cv2.Canny(gray, 75, 200)
    cnt, _, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cnt

    cv2.drawContours(image, cnt, -1, (0, 255, 0), 5)
    return image


def color_ratio(image):
    color = 0
    total = 0
    for arr in image:
        for r in arr:
            if sum(r):
                color += 1
            total += 1
    return total/color


# Green ((0, 19, 0), (197, 250, 186))
# Red ((0, 0, 14), (116, 0, 252))
# Gold


def apply_mask(image, color_range):
    lower = np.array(color_range[0], dtype = 'uint8')
    upper = np.array(color_range[1], dtype = 'uint8')
    mask = cv2.inRange(image, lower, upper)
    return cv2.bitwise_and(image, image, mask=mask)


def apply_not_mask(image, color_range):
    lower = np.array(color_range[0], dtype = 'uint8')
    upper = np.array(color_range[1], dtype = 'uint8')
    mask = cv2.inRange(image, lower, upper)
    return cv2.bitwise_not(image, image, mask=mask)


def apply_hsv_mask(image, color=255):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = (50, 100, 100)
    upper = (70, 255, 255)
    mask = cv2.inRange(hsv_img, lower, upper)
    hsv_img = cv2.bitwise_and(hsv_img, hsv_img, mask=mask)
    return cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)


def main(image):
    green = ([25, 15, 15], [250, 100, 75])
    red = ([17, 15, 100], [50, 56, 200])
    alls = ([0,0,0],[255,255,255])
    lower = np.array(alls[0], dtype = "uint8")
    upper = np.array(alls[1], dtype = "uint8")

    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    return output

