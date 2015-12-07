"""
Functionality to draw using OpenCV functionality.
"""

from collections import namedtuple
import itertools
import numpy as np
import cv2
from . import utils
from . import colors


def blank_canvas(shape, color):
    """Return a blank canvas of the specified shape and color"""
    blank = np.array([color] * shape[0] * shape[1], dtype=np.uint8)
    return blank.reshape(shape)


def contour(img_shape, contour):
    """Draw black contour on white image"""
    blank = blank_canvas(img_shape, colors.WHITE)
    cv2.drawContours(blank, [contour], 0, colors.BLACK, 3)
    return blank


def contour_overlay(img, contour):
    """Draw contour as overlay on grayscale image"""
    img = utils.to_gray(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(img, [contour], 0, colors.CYAN, 1)
    return img


def sketch(img, dots, corners):
    """Draw the lights and lines on the images"""
    for dot in dots:
        cv2.circle(img, dot, 2, colors.RED, -1)

    for corner in corners:
        cv2.circle(img, corner, 5, colors.BLUE, -1)

    for corner1, corner2 in itertools.combinations(corners, 2):
        cv2.line(img, corner1, corner2, colors.GREEN, thickness=2)
    cv2.line(img, corners.bottom_mid, corners.top, colors.GREEN, thickness=2)

    return img


def leds(img_shape, dots):
    """Draw dots on a white image"""
    blank = blank_canvas(img_shape, colors.WHITE)
    for (x, y) in dots:
       cv2.circle(blank, (x, y), 2, colors.BLUE, -1)
    return blank


def outline(img_shape, corners):
    """Draw the outline on the image"""
    blank = blank_canvas(img_shape, colors.WHITE)

    # Draw cirles for the corners and connect them with lines to create a
    # stylized tree
    for corner in corners:
        cv2.circle(blank, corner, 5, colors.BLACK, -1)

    for corner1, corner2 in itertools.combinations(corners, 2):
        cv2.line(blank, corner1, corner2, colors.BLACK, thickness=2)

    cv2.line(blank, corners.bottom_mid, corners.top, colors.BLACK, thickness=2)
    return blank


def crop_shape(img, corners, border=10):
    """Crop the image to fit the shape while making sure there is a border
    aorund the corners"""
    min_x, min_y = 0, 0
    max_y, max_x, _ = img.shape
    bottom_y = max(corners.bottom_left[1], corners.bottom_right[1])

    start_x = max(corners.bottom_left[0] - border, min_x)
    end_x = min(corners.bottom_right[0] + border, max_x)
    start_y = max(corners.top[1] - border, min_y)
    end_y = min(bottom_y + border, max_y)
    return img[start_y:end_y, start_x:end_x]


def twit_size(img):
    target_width = 440
    target_height = 220
    source_width = img.shape[0]
    source_height = img.shape[1]

    blank = np.array([(255,255,255)] * target_width * target_height,
                    dtype=np.uint8)
    blank.reshape((target_width, target_height))

    if source_height * 2 > source_width:
        # Images is relatively too tall
        img = utils.resize(img, width=target_width)
    elif source_width > source_height * 2:
        # Image is relatively too wide
        img = utils.resize(img, height=target_height)
    else:
        # Image is the correct ratio
        img = utils.resize(img, height=target_height)

