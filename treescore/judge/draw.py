"""
Functions to draw an outline of the tree based on the corners detected. Will
ensure the produced image is cropped so that the tree is centered.

"""

# Notes:
# img.shape = (height, width, depth)
# image coordinates (0, 0) = top left
# image coordinates (width, height) = bottom right


from collections import namedtuple
import itertools
import numpy as np
import cv2
from . import utils


def contour(img_shape, contour):
    """Draw black contour on white image"""
    blank = np.array([(255,255,255)] * img_shape[0] * img_shape[1],
                    dtype=np.uint8)
    blank = blank.reshape(img_shape)

    black = (0, 0, 0)
    cv2.drawContours(blank, [contour], 0, black, 3)
    return blank


def sketch(img, dots, corners):
    """Draws the lights and lines on the img"""
    red = (0, 0, 255)
    for dot in dots:
        cv2.circle(img, dot, 2, red, -1)

    blue = (255, 0, 0)
    for corner in corners:
        cv2.circle(img, corner, 8, blue, -1)

    green = (127, 255, 0)
    for corner1, corner2 in itertools.combinations(corners, 2):
        cv2.line(img, corner1, corner2, green, thickness=2)
    cv2.line(img, corners.bottom_mid, corners.top, green, thickness=2)

    return img


def leds(img_shape, dots):
    """Draw red dots on a white image"""
    # Create an empty white image of the same size as the orginal image
    color = (0, 0, 0)
    blank = np.array([(255,255,255)] * img_shape[0] * img_shape[1],
                    dtype=np.uint8)
    blank = blank.reshape(img_shape)

    for (x, y) in dots:
       cv2.circle(blank, (x, y), 2, color, -1)
    return blank


def outline(img_shape, corners):
    """Draws the outline on the image"""
    # Create an empty white image of the same size as the orginal image
    color = (0, 0, 0)
    blank = np.array([(255,255,255)] * img_shape[0] * img_shape[1],
                    dtype=np.uint8)
    blank = blank.reshape(img_shape)

    # Draw cirles for the corners and connect them with lines to create a
    # stylized tree
    for corner in corners:
        cv2.circle(blank, corner, 5, color, -1)

    for corner1, corner2 in itertools.combinations(corners, 2):
        cv2.line(blank, corner1, corner2, color, thickness=2)

    cv2.line(blank, corners.bottom_mid, corners.top, color, thickness=2)
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

